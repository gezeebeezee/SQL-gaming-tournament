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


@app.route("/players", methods=["GET"])
def players():
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
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
        query2 = "SELECT gameID, title FROM Games"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        games_data = cur.fetchall()

        # render edit_player page passing our query data and team/gane data to the edit_player template
        return render_template("main.j2", data=data, teams=teams_data, games=games_data)


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=3000, debug=True)
