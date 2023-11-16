from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


# Configuration

app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = ""
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = ""
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Routes

# have homepage route to /people by default for convenience, 
# generally this will be your home route with its own template
@app.route('/')
def home():
    return redirect("/players")

# route for players page
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
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, birthdate, captain))
                mysql.connection.commit()

            elif team == "0":
                query = "INSERT INTO Players (name, username, birthdate, captain, gameID) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, birthdate, captain, game))
                mysql.connection.commit()

            elif game == "0":
                query = "INSERT INTO Players (name, username, birthdate, captain, teamID) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, birthdate, captain, team))
                mysql.connection.commit()

            else:
                query = "INSERT INTO Players (name, username, birthdate, captain, teamID, gameID) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, birthdate, captain, team, game))
                mysql.connection.commit()

            # redirect back to player page
            return redirect("/players")

    if request.method == "GET":
        # mySQL query to grab all the players
        query = "SELECT Players.playerID, Players.name, Players.username, Players.birthdate, Players.captain, IFNULL(Teams.teamName, '*No Team*') as Team, IFNULL(Games.title, '*No Game*') as Game FROM Players LEFT JOIN Teams ON Teams.teamID=Players.teamID LEFT JOIN Games ON Games.gameID=Players.gameID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab team id/name data for our dropdown
        query2 = "SELECT teamID, teamName FROM Teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        teams_data = cur.fetchall()

        # mySQL query to grab game id/name data for our dropdown
        query3 = "SELECT gameID, title FROM Games"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        games_data = cur.fetchall()

        # send data to populate drop down boxes
        return render_template("players.j2", data=data, teams=teams_data, games=games_data)
    

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_player/<int:id>")
def delete_player(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Players WHERE playerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/players")

# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_player/<int:id>", methods=["POST", "GET"])
def edit_player(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Players.playerID, Players.name, Players.username, Players.birthdate, Players.captain, IFNULL(Teams.teamName, '*No Team*') as team, IFNULL(Games.title, '*No Game*') as game FROM Players LEFT JOIN Teams ON Teams.teamID=Players.teamID LEFT JOIN Games ON Games.gameID=Players.gameID WHERE playerID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab team id/name data for our dropdown
        query2 = "SELECT teamID, teamName FROM Teams"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        teams_data = cur.fetchall()

        #mysql query to grab game id/name data for dropdown
        query3 = "SELECT gameID, title FROM Games"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        games_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_player.j2", data=data, teams=teams_data, games=games_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
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
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, captain, id))
                mysql.connection.commit()

            # account for null team
            elif team == "0":
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = NULL, Players.gameID = %s WHERE Players.playerID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, captain, game, id))
                mysql.connection.commit()

            # account for null game
            elif game == "" or game == "None" or game == 0:
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = %s, Players.gameID = NULL WHERE Players.playerID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, captain, team, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Players SET Players.name = %s, Players.username = %s, Players.captain = %s, Players.teamID = %s, Players.gameID = %s WHERE Players.playerID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, username, captain, team, game, id))
                mysql.connection.commit()

            # redirect back to players page after we execute the update query
            return redirect("/players")


# Listener
if __name__ == "__main__":
    app.run(port=3000, debug=True)
