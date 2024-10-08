from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

# Configuration

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static') 

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = ""
# app.config["MYSQL_PASSWORD"] = ""
# app.config["MYSQL_DB"] = ""
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# mysql = MySQL(app)

app.config["MYSQL_HOST"] = os.getenv("db_url")
app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_DB"] = os.getenv("db_name")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


timeout = 10
mysql = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db=app.config["MYSQL_DB"],
  host=app.config["MYSQL_HOST"],
  password=app.config["MYSQL_PASSWORD"],
  read_timeout=timeout,
  port=16478,
  user=app.config["MYSQL_USER"],
  write_timeout=timeout,
)


# Routes
@app.route('/index')
def home():
    return render_template("home.j2")

@app.route('/')
def index():
    return render_template("home.j2")


####################################
##    TOURNAMENTS FUNCTIONS       ##
####################################
# route for tournaments page
# Citation for the following function
# Adapted from cs340-flask-starter-app
# Modified variables and queries to fit requirements needed for our Tournaments table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/tournaments", methods=["GET", "POST"])
def tournaments():
    if request.method == "POST" and "tournamentName" in request.form:
        # grab inputs from form
        name = request.form["tournamentName"]
        location = request.form["location"]
        startDate = request.form["startDate"]
        endDate = request.form["endDate"]

        # query to insert form values into database
        query = "INSERT INTO Tournaments (tournamentName, location, startDate, endDate) VALUES (%s, %s, %s, %s)"
        cur = mysql.cursor()
        cur.execute(query, (name, location, startDate, endDate))
        mysql.commit()

        # redirect back to tournament page
        return redirect("/tournaments")
    
    elif request.method == "POST" and "tournamentID" in request.form:
        # grab inputs from form
        tournament = request.form["tournamentID"]
        game = request.form["gameID"]

        # query to insert form values
        query = "INSERT into Tournaments_has_Games (tournamentID, gameID) VALUES (%s, %s)"
        cur = mysql.cursor()
        cur.execute(query, (tournament, game))
        mysql.commit()

        # redirect back to tournament page
        return redirect("/tournaments")

    if request.method == "GET":
        # mySQL query to grab all the tournaments
        query = "SELECT Tournaments.tournamentID, Tournaments.tournamentName, Tournaments.location, Tournaments.startDate, Tournaments.endDate from Tournaments;"
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab all the games
        query = "SELECT Games.gameID, Games.title FROM Games;"
        cur = mysql.cursor()
        cur.execute(query)
        games = cur.fetchall()

        # mySQL query to grab all the tournaments and their games
        query = "SELECT Tournaments.tournamentID, Tournaments.tournamentName as 'Name', Games.gameID, Games.title as 'Title' FROM Tournaments INNER JOIN Tournaments_has_Games ON Tournaments.tournamentID = Tournaments_has_Games.tournamentID INNER JOIN Games ON Games.gameID = Tournaments_has_Games.gameID ORDER BY Tournaments.tournamentID ASC;"
        cur = mysql.cursor()
        cur.execute(query)
        intersection = cur.fetchall()

        return render_template("tournaments.j2", data=data, intersection=intersection, games=games)

# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for Tournaments table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_tournament/<int:id>")
def delete_tournament(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Tournaments WHERE tournamentID = '%s';"
    cur = mysql.cursor()
    cur.execute(query, (id,))
    mysql.commit()

    # redirect back to people page
    return redirect("/tournaments")


# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from Tournaments database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_tournament/<int:id>", methods=["POST", "GET"])
def edit_tournament(id):
    if request.method == "GET":
        # mySQL query to grab the info of the player with passed id
        query = "SELECT Tournaments.tournamentID, Tournaments.tournamentName, Tournaments.location, Tournaments.startDate, Tournaments.endDate FROM Tournaments where tournamentID = %s" % (id)
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_tournament page passing our query data, teams data, and games data to the edit_tournament template
        return render_template("edit_tournament.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Tournament' button
        if request.form.get("Edit_Tournament"):
            # grab user form inputs
            id = request.form["tournamentID"]
            name = request.form["tournamentName"]
            location = request.form["location"]
            startDate = request.form["startDate"]
            endDate = request.form["endDate"]
            

            # no null inputs allowed in Tournaments
            query = "UPDATE Tournaments SET Tournaments.tournamentName = %s, Tournaments.location = %s, Tournaments.startDate = %s, Tournaments.endDate = %s WHERE Tournaments.tournamentID = %s"
            cur = mysql.cursor()
            cur.execute(query, (name, location, startDate, endDate, id))
            mysql.commit()

            # redirect back to players page after we execute the update query
            return redirect("/tournaments")
        
# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for interesection table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_tournament_game", methods=["POST"])
def delete_tournament_game():

    # grab hidden inputs
    gameID = request.form["gameID"]
    tournamentID = request.form["tournamentID"]

    # mySQL query to delete the tournament-game with our passed id
    query = "DELETE FROM Tournaments_has_Games WHERE Tournaments_has_Games.gameID = %s AND Tournaments_has_Games.tournamentID = %s;"
    cur = mysql.cursor()
    cur.execute(query, (gameID, tournamentID))
    mysql.commit()

    # redirect back to tournaments page
    return redirect("/tournaments")


# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from intersection database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_tournament_game/<int:id><int:id2>", methods=["POST", "GET"])
def edit_tournament_game(id, id2):
    if request.method == "GET":
        # mySQL query to grab the info of the tournament-game with passed id
        cur = mysql.cursor()
        query = "SELECT Tournaments.tournamentID, Tournaments.tournamentName, Games.gameID, Games.title FROM Tournaments INNER JOIN Tournaments_has_Games ON Tournaments.tournamentID = Tournaments_has_Games.tournamentID INNER JOIN Games ON Games.gameID = Tournaments_has_Games.gameID WHERE Tournaments_has_Games.gameID = %s AND Tournaments_has_Games.tournamentID = %s"
        cur.execute(query, (id, id2))
        data = cur.fetchall()

        ## mySQL query to grab game id/title data for our dropdown
        query2 = "SELECT gameID, title FROM Games"
        cur = mysql.cursor()
        cur.execute(query2)
        games_data = cur.fetchall()

        #mysql query to grab tournament id/name data for dropdown
        query3 = "SELECT tournamentID, tournamentName FROM Tournaments"
        cur = mysql.cursor()
        cur.execute(query3)
        tournaments_data = cur.fetchall()

        # render edit_tournament_game page passing our query data, teams data, and games data to the edit_tournament_game template
        return render_template("edit_tournament_game.j2", data=data, games=games_data, tournaments=tournaments_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Tournament Game' button
        if request.form.get("Edit_Tournament_Game"):
            # grab user form inputs
            tournamentID = request.form["tournamentID"]
            gameID = request.form["gameID"]

            query = "UPDATE Tournaments_has_Games SET tournamentID = %s, gameID = %s WHERE tournamentID = %s and gameID = %s"
            cur = mysql.cursor()
            cur.execute(query, (tournamentID, gameID, id2, id))
            mysql.commit()

            # redirect back to tournaments page after we execute the update query
            return redirect("/tournaments")

####################################
##        GAMES FUNCTIONS         ##
####################################
# route for games page
# Citation for the following function
# Adapted from cs340-flask-starter-app
# Modified variables and queries to fit requirements needed for our Games table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/games", methods=["GET", "POST"])
def games():
    if request.method == "POST":
        # grab inputs from form
        title = request.form["title"]
        genre = request.form["genre"]
        platform = request.form["platform"]

        # query to insert form values into database
        query = "INSERT INTO Games (title, genre, platform) VALUES (%s, %s, %s)"
        cur = mysql.cursor()
        cur.execute(query, (title, genre, platform))
        mysql.commit()

        # redirect back to tournament page
        return redirect("/games")

    if request.method == "GET":
        # mySQL query to grab all the games
        query = "SELECT Games.gameID, Games.title, Games.genre, Games.platform FROM Games;"
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("games.j2", data=data)

# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for Games table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_game/<int:id>")
def delete_game(id):
    # mySQL query to delete the game with our passed id
    query = "DELETE FROM Games WHERE gameID = '%s';"
    cur = mysql.cursor()
    cur.execute(query, (id,))
    mysql.commit()

    # redirect back to people page
    return redirect("/games")

# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from Games database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_game/<int:id>", methods=["POST", "GET"])
def edit_game(id):
    if request.method == "GET":
        # mySQL query to grab the info of the game with passed id
        query = "SELECT Games.gameID, Games.title, Games.genre, Games.platform FROM Games where gameID = %s" % (id)
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_game page passing our query data, teams data, and games data to the edit_game template
        return render_template("edit_game.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Game' button
        if request.form.get("Edit_Game"):
            # grab user form inputs
            id = request.form["gameID"]
            title = request.form["title"]
            genre = request.form["genre"]
            platform = request.form["platform"]
            

            # no null inputs allowed in Games
            query = "UPDATE Games SET Games.title = %s, Games.genre = %s, Games.platform = %s WHERE Games.gameID = %s"
            cur = mysql.cursor()
            cur.execute(query, (title, genre, platform, id))
            mysql.commit()

            # redirect back to games page after we execute the update query
            return redirect("/games")


####################################
##         TEAMS FUNCTIONS        ##
####################################
# route for teams page
# Citation for the following function
# Adapted from cs340-flask-starter-app
# Modified variables and queries to fit requirements needed for our Teams table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/teams", methods=["GET", 'POST'])
def teams():
    if request.method == "POST":
        # grab inputs from form
        if request.form.get("addTeam"):
            teamName = request.form["teamName"]
            location = request.form["location"]
            sponsor = request.form["sponsor"]
            tournament = request.form["tournament"]
            description = request.form["description"]

            # account for combinations of null sponsor or null tournament
            if sponsor == "0" and tournament == "0":
                query = "INSERT INTO Teams (teamName, location, description) VALUES (%s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, description))
                mysql.commit()

            elif sponsor == "0":
                query = "INSERT INTO Teams (teamName, location, tournamentID, description) VALUES (%s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, tournament, description))
                mysql.commit()

            elif tournament == "0":
                query = "INSERT INTO Teams (teamName, location, sponsorID, description) VALUES (%s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, description))
                mysql.commit()

            else:
                query = "INSERT INTO Teams (teamName, location, sponsorID, tournamentID, description) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, tournament, description))
                mysql.commit()

            # redirect back to teams page
            return redirect("/teams")
        
    if request.method == "GET":
        # mySQL query to grab all the teams
        query = "SELECT Teams.teamID, Teams.teamName, Teams.location, IFNULL(Sponsors.sponsorName, '*No Sponsor*') as sponsor, IFNULL(Tournaments.tournamentName, '*No Tournament*') as tournament, Teams.description FROM Teams LEFT JOIN Sponsors ON Sponsors.sponsorID = Teams.sponsorID LEFT JOIN Tournaments ON Tournaments.tournamentID = Teams.tournamentID;"
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab sponsor id/name data for our dropdown
        query2 = "SELECT sponsorID, sponsorName FROM Sponsors"
        cur = mysql.cursor()
        cur.execute(query2)
        sponsors_data = cur.fetchall()

        # mySQL query to grab tournament id/name data for our dropdown
        query3 = "SELECT tournamentID, tournamentName FROM Tournaments"
        cur = mysql.cursor()
        cur.execute(query3)
        tournaments_data = cur.fetchall()

        # send data to populate drop down boxes
        return render_template("teams.j2", data=data, sponsors=sponsors_data, tournaments=tournaments_data)

# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for Teams table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_team/<int:id>")
def delete_team(id):
    # mySQL query to delete the team with our passed id
    query = "DELETE FROM Teams WHERE teamID = '%s';"
    cur = mysql.cursor()
    cur.execute(query, (id,))
    mysql.commit()

    # redirect back to teams page
    return redirect("/teams")

# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from Teams database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_team/<int:id>", methods=["POST", "GET"])
def edit_team(id):
    if request.method == "GET":
        # mySQL query to grab the info of the teams with passed id
        query = "SELECT Teams.teamID, Teams.teamName, Teams.location, IFNULL(Sponsors.sponsorName, '*No Sponsor*') as sponsor, IFNULL(Tournaments.tournamentName, '*No Tournament*') as tournament, Teams.description FROM Teams LEFT JOIN Sponsors ON Sponsors.sponsorID=Teams.sponsorID LEFT JOIN Tournaments ON Tournaments.tournamentID=Teams.tournamentID WHERE teamID = %s" % (id)
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab sponsor id/name data for our dropdown
        query2 = "SELECT sponsorID, sponsorName FROM Sponsors"
        cur = mysql.cursor()
        cur.execute(query2)
        sponsors_data = cur.fetchall()

        #mysql query to grab tournament id/name data for dropdown
        query3 = "SELECT tournamentID, tournamentName FROM Tournaments"
        cur = mysql.cursor()
        cur.execute(query3)
        tournaments_data = cur.fetchall()

        # render edit_team page passing our query data, sponsors data, and tournaments data to the edit_team template
        return render_template("edit_team.j2", data=data, sponsors=sponsors_data, tournaments=tournaments_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Player' button
        if request.form.get("Edit_Team"):
            # grab user form inputs
            id = request.form["teamID"]
            teamName = request.form["teamName"]
            location = request.form["location"]
            sponsor = request.form["sponsor"]
            tournament = request.form["tournament"]
            description = request.form["description"]

            # account for null sponsor, tournament, and description
            if (sponsor == "0") and (tournament == "0") and (description == "0"):
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = NULL, Teams.tournamentID = NULL, Teams.description = NULL  WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, id))
                mysql.commit()

            # account for null tournament and description
            elif (tournament == "0") and (description == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = %s, Teams.tournamentID = NULL, Teams.description = NULL WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, id))
                mysql.commit()

            # account for null sponsor and description
            elif (sponsor == "0") and (description == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = NULL, Teams.tournamentID = %s, Teams.description = NULL WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, tournament, id))
                mysql.commit()


            # account for null sponsor and tournament
            elif (sponsor == "0") and (tournament == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = NULL, Teams.tournamentID = NULL, Teams.description = %s WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, description, id))
                mysql.commit()


            # account for null tournament
            elif (tournament == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = %s, Teams.tournamentID = NULL, Teams.description = %s WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, description, id))
                mysql.commit()


            # account for null sponsor
            elif (sponsor == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = NULL, Teams.tournamentID = %s, Teams.description = %s WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, tournament, description, id))
                mysql.commit()


            # account for null description
            elif (description == "0"):
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = %s, Teams.tournamentID = %s, Teams.description = NULL WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, tournament, id))
                mysql.commit()

            # no null inputs
            else:
                query = "UPDATE Teams SET Teams.teamName = %s, Teams.location = %s, Teams.sponsorID = %s, Teams.tournamentID = %s, Teams.description = %s WHERE Teams.teamID = %s"
                cur = mysql.cursor()
                cur.execute(query, (teamName, location, sponsor, tournament, description, id))
                mysql.commit()

            # redirect back to teams page after we execute the update query
            return redirect("/teams")


####################################
##       PLAYERS FUNCTIONS        ##
####################################
# route for players page
# Citation for the following function
# Adapted from cs340-flask-starter-app
# Modified variables and queries to fit requirements needed for our Players table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/players", methods=["GET", "POST"])
def players():
    if request.method == "POST":
        # grab inputs from form
        if request.form.get("addPlayer"):
            name = request.form["name"]
            username = request.form["username"]
            birthdate = request.form["birthdate"]
            captain = request.form["captain"]
            team = request.form["team"]
            game = request.form["game"]

            # account for combinations of null team or null game
            if team == "0" and game == "0":
                query = "INSERT INTO Players (name, username, birthdate, captain) VALUES (%s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (name, username, birthdate, captain))
                mysql.commit()

            elif team == "0":
                query = "INSERT INTO Players (name, username, birthdate, captain, gameID) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (name, username, birthdate, captain, game))
                mysql.commit()

            elif game == "0":
                query = "INSERT INTO Players (name, username, birthdate, captain, teamID) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (name, username, birthdate, captain, team))
                mysql.commit()

            else:
                query = "INSERT INTO Players (name, username, birthdate, captain, teamID, gameID) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.cursor()
                cur.execute(query, (name, username, birthdate, captain, team, game))
                mysql.commit()

            # redirect back to player page
            return redirect("/players")

    if request.method == "GET":
        # mySQL query to grab all the players
        query = "SELECT Players.playerID, Players.name, Players.username, Players.birthdate, Players.captain, IFNULL(Teams.teamName, '*No Team*') as team, IFNULL(Games.title, '*No Game*') as game FROM Players LEFT JOIN Teams ON Teams.teamID=Players.teamID LEFT JOIN Games ON Games.gameID=Players.gameID;"
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab team id/name data for our dropdown
        query2 = "SELECT teamID, teamName FROM Teams"
        cur = mysql.cursor()
        cur.execute(query2)
        teams_data = cur.fetchall()

        # mySQL query to grab game id/name data for our dropdown
        query3 = "SELECT gameID, title FROM Games"
        cur = mysql.cursor()
        cur.execute(query3)
        games_data = cur.fetchall()

        # send data to populate drop down boxes
        return render_template("players.j2", data=data, teams=teams_data, games=games_data)
    
# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for Players database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_player/<int:id>")
def delete_player(id):
    # mySQL query to delete the player with our passed id
    query = "DELETE FROM Players WHERE playerID = '%s';"
    cur = mysql.cursor()
    cur.execute(query, (id,))
    mysql.commit()

    # redirect back to players page
    return redirect("/players")

# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from Players database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_player/<int:id>", methods=["POST", "GET"])
def edit_player(id):
    if request.method == "GET":
        # mySQL query to grab the info of the player with passed id
        query = "SELECT Players.playerID, Players.name, Players.username, Players.birthdate, Players.captain, IFNULL(Teams.teamName, '*No Team*') as team, IFNULL(Games.title, '*No Game*') as game FROM Players LEFT JOIN Teams ON Teams.teamID=Players.teamID LEFT JOIN Games ON Games.gameID=Players.gameID WHERE playerID = %s" % (id)
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab team id/name data for our dropdown
        query2 = "SELECT teamID, teamName FROM Teams"
        cur = mysql.cursor()
        cur.execute(query2)
        teams_data = cur.fetchall()

        #mysql query to grab game id/name data for dropdown
        query3 = "SELECT gameID, title FROM Games"
        cur = mysql.cursor()
        cur.execute(query3)
        games_data = cur.fetchall()

        # render edit_player page passing our query data, teams data, and games data to the edit_player template
        return render_template("edit_player.j2", data=data, teams=teams_data, games=games_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Player' button
        if request.form.get("Edit_Player"):
            # grab user form inputs
            id = request.form["playerID"]
            name = request.form["name"]
            username = request.form["username"]
            captain = request.form["captain"]
            team = request.form["team"]
            game = request.form["game"]

            # account for null game AND team
            if (game == "0") and team == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = NULL, Players.gameID = NULL WHERE Players.playerID = %s"
                cur = mysql.cursor()
                cur.execute(query, (name, username, captain, id))
                mysql.commit()

            # account for null team
            elif team == "0":
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = NULL, Players.gameID = %s WHERE Players.playerID = %s"
                cur = mysql.cursor()
                cur.execute(query, (name, username, captain, game, id))
                mysql.commit()

            # account for null game
            elif game == "" or game == "None" or game == 0:
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = %s, Players.gameID = NULL WHERE Players.playerID = %s"
                cur = mysql.cursor()
                cur.execute(query, (name, username, captain, team, id))
                mysql.commit()

            # no null inputs
            else:
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = %s, Players.gameID = %s WHERE Players.playerID = %s"
                cur = mysql.cursor()
                cur.execute(query, (name, username, captain, team, game, id))
                mysql.commit()

            # redirect back to players page after we execute the update query
            return redirect("/players")
        

####################################
##       SPONSORS FUNCTIONS       ##
####################################
# route for sponsors page
# Citation for the following function
# Adapted from cs340-flask-starter-app
# Modified variables and queries to fit requirements needed for our Sponsors table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/sponsors", methods=["GET", "POST"])
def sponsors():
    if request.method == "POST":
        # grab inputs from form
        sponsor = request.form["sponsorName"]
        contactPerson = request.form["contactPerson"]
        contactEmail = request.form["contactEmail"]

        # query to insert form values into database
        query = "INSERT INTO Sponsors (sponsorName, contactPerson, contactEmail) VALUES (%s, %s, %s)"
        cur = mysql.cursor()
        cur.execute(query, (sponsor, contactPerson, contactEmail))
        mysql.commit()

        # redirect back to sponsors page
        return redirect("/sponsors")

    if request.method == "GET":
        # mySQL query to grab all the sponsors
        query = "SELECT Sponsors.sponsorID, Sponsors.sponsorName, Sponsors.contactPerson, Sponsors.contactEmail from Sponsors;"
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("sponsors.j2", data=data)

# route for delete functionality
# Citation for the following function
# Adapted from flask-starter-app > bsg_people code
# Modified variables and queries to fit requirements needed for Sponsors table
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/delete_sponsor/<int:id>")
def delete_sponsor(id):
    # mySQL query to delete the sponsor with our passed id
    query = "DELETE FROM Sponsors WHERE sponsorID = '%s';"
    cur = mysql.cursor()
    cur.execute(query, (id,))
    mysql.commit()

    # redirect back to sponsors page
    return redirect("/sponsors")


# route for edit functionality
# Citation for the following function
# Adapted from flask-starter-app code
# Modified variables and queries to select desired data from Sponsors database
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
@app.route("/edit_sponsor/<int:id>", methods=["POST", "GET"])
def edit_sponsor(id):
    if request.method == "GET":
        # mySQL query to grab the info of the sponsor with passed id
        query = "SELECT Sponsors.sponsorID, Sponsors.sponsorName, Sponsors.contactPerson, Sponsors.contactEmail FROM Sponsors where sponsorID = %s" % (id)
        cur = mysql.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_sponsor page passing our query data, teams data, and games data to the edit_sponsor template
        return render_template("edit_sponsor.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Sponsor' button
        if request.form.get("Edit_Sponsor"):
            # grab user form inputs
            id = request.form["sponsorID"]
            name = request.form["sponsorName"]
            contactPerson = request.form["contactPerson"]
            email = request.form["contactEmail"]
            

            # no null inputs allowed in Sponsors
            query = "UPDATE Sponsors SET Sponsors.sponsorName = %s, Sponsors.contactPerson = %s, Sponsors.contactEmail = %s WHERE Sponsors.sponsorID = %s"
            cur = mysql.cursor()
            cur.execute(query, (name, contactPerson, email, id))
            mysql.commit()

            # redirect back to sponsors page after we execute the update query
            return redirect("/sponsors")
        
# Listener
if __name__ == "__main__":
    app.run(port=3000, debug=True)
