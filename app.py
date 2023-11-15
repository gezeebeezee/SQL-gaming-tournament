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
app.config["MYSQL_USER"] = "cs340_vust"
app.config["MYSQL_PASSWORD"] = "x62ZkepfILY7"
app.config["MYSQL_DB"] = "cs340_vust"
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


# Listener
if __name__ == "__main__":
    app.run(port=3000, debug=True)
