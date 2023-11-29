-- Group 73 Project Step 3
-- Steven Vu and Kevin Le

--
-- Database: `cs340_vust`
-- Database: 'cs340_lekevinp
--


----- SELECTS -----
-- get all Tournaments information
SELECT Tournaments.tournamentID, Tournaments.tournamentName, Tournaments.location, Tournaments.startDate, Tournaments.endDate 
from Tournaments;

-- get all Players information
SELECT Players.playerID, Players.name, Players.username, Players.birthdate, Players.captain, IFNULL(Teams.teamName, "*No Team*") as Team, IFNULL(Games.title, "*No Game*") as Game 
FROM Players
LEFT JOIN Teams ON Teams.teamID=Players.teamID
LEFT JOIN Games ON Games.gameID=Players.gameID;

-- get all Teams information
SELECT Teams.teamID, Teams.teamName, Teams.location, IFNULL(Sponsors.sponsorName, "*No Sponsor*") as Sponsor, IFNULL(Tournaments.tournamentName, "*No Tournament*") as Tournament, Teams.description 
FROM Teams
LEFT JOIN Sponsors ON Sponsors.sponsorID=Teams.sponsorID
LEFT JOIN Tournaments ON Tournaments.tournamentID=Teams.tournamentID;

-- get all Games information
SELECT Games.gameID, Games.title, Games.genre, Games.platform from Games;

-- get all Sponsors information
SELECT Sponsors.sponsorID, Sponsors.sponsorName, Sponsors.contactPerson, Sponsors.contactEmail from Sponsors;

-- get all Tournaments_Has_Games information
SELECT Tournaments.tournamentName, Games.title 
FROM Tournaments 
INNER JOIN Tournaments_has_Games ON Tournaments.tournamentID = Tournaments_has_Games.tournamentID
INNER JOIN Games ON Games.gameID = Tournaments_has_Games.gameID
ORDER BY Tournaments.tournamentName ASC;


----- INSERTS -----
-- add a new Tournament
INSERT INTO Tournaments (tournamentName, location, startDate, endDate)
VALUES (:tournamentNameInput, :locationInput, :startDateInput, :endDateInput);

-- add a new Player
INSERT INTO Players (name, username, birthdate, captain, teamID, gameID)
VALUES (:nameInput, :usernameInput, :birthdateInput, :captainInput, :teamID_from_dropdown_Input, :gameID_from_dropdown_Input);

-- add a new Team
INSERT INTO Teams (teamName, location, sponsorID, tournamentID, description)
VALUES (:teamNameInput, :locationInput, :sponsorID_from_dropdown_Input, :tournamentID_from_dropdown_Input, :descriptionInput);

-- add a new Game
INSERT INTO Games (title, genre, platform)
VALUES (:titleInput, :genreInput, :platformInput);

-- add a new Sponsor
INSERT INTO Sponsors (sponsorName, contactPerson, contactEmail)
VALUES (:sponsorNameInput, :contactPersonInput, :contactEmailInput);

-- add Game to Tournament (M-M Relationship)
INSERT INTO Tournaments_has_Games (gameID, tournamentID)
VALUES (:gameID_from_dropdown_Input, :tournamentID_from_dropdown_Input);


----- Update -----
-- update Player information
UPDATE Players SET name = :nameInput, username = :usernameInput, birthdate = :birthdateInput, captain = :captainInput, teamID = :teamID_from_dropdown_Input, gameID = :gameID_from_dropdown_Input WHERE playerID = :playerID_from_dropdown_Input;

-- update Tournaments_has_Games information
UPDATE Tournaments_has_Games SET gameID = :gameID_from_dropdown_Input WHERE tournamentID = :tournamentID_from_dropdown_Input;

----- Delete -----
-- delete a Player
DELETE FROM Players WHERE playerID = :playerID_selected_from_browse_player_page;

-- disassociate a Game from a Tournament
DELETE FROM Tournaments_has_Games WHERE gameID = :gameID_selected_from_game_and_tournament_list AND tournamentID = :tournamentID_selected_from_game_and_tournament_list;