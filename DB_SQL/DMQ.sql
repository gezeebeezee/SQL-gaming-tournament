-- Group 73 Project Step 3
-- Steven Vu and Kevin Le

--
-- Database: `cs340_vust`
-- Database: 'cs340_lekevinp
--


----- SELECTS -----
-- get all Tournaments information
SELECT Tournaments.TournamentID, Tournaments.TournamentName, Tournaments.Location, Tournaments.StartDate, Tournaments.EndDate 
from Tournaments;

-- get all Players information
SELECT Players.PlayerID, Players.Name, Players.Username, Players.Birthdate, Players.Captain, IFNULL(Teams.TeamName, "*No Team*") as Team, IFNULL(Games.Title, "*No Game*") as Game 
FROM Players
LEFT JOIN Teams ON Teams.TeamID=Players.TeamID
LEFT JOIN Games ON Games.GameID=Players.GameID;

-- get all Teams information
SELECT Teams.TeamID, Teams.TeamName, Teams.Location, IFNULL(Sponsors.SponsorName, "*No Sponsor*") as Sponsor, IFNULL(Tournaments.TournamentName, "*No Tournament*") as Tournament, Teams.Description 
FROM Teams
LEFT JOIN Sponsors ON Sponsors.SponsorID=Teams.SponsorID
LEFT JOIN Tournaments ON Tournaments.TournamentID=Teams.TournamentID;

-- get all Games information
SELECT Games.GameID, Games.Title, Games.Genre, Games.Platform from Games;

-- get all Sponsors information
SELECT Sponsors.SponsorID, Sponsors.SponsorName, Sponsors.ContactPerson, Sponsors.ContactEmail from Sponsors;


----- INSERTS -----
-- add a new Tournament
INSERT INTO Tournaments (TournamentName, Location, StartDate, EndDate)
VALUES (:TournamentNameInput, :LocationInput, :StartDateInput, :EndDateInput);

-- add a new Player
INSERT INTO Players (Name, Username, Birthdate, Captain, TeamID, GameID)
VALUES (:NameInput, :UsernameInput, :BirthdateInput, :CaptainInput, :TeamID_from_dropdown_Input, :GameID_from_dropdown_Input);

-- add a new Team
INSERT INTO Teams (TeamName, Location, SponsorID, TournamentID, Description)
VALUES (:TeamNameInput, :LocationInput, :SponsorID_from_dropdown_Input, :TournamentID_from_dropdown_Input, :DescriptionInput);

-- add a new Game
INSERT INTO Games (Title, Genre, Platform)
VALUES (:TitleInput, :GenreInput, :PlatformInput);

-- add a new Sponsor
INSERT INTO Sponsors (SponsorName, ContactPerson, ContactEmail)
VALUES (:SponsorNameInput, :ContactPersonInput, :ContactEmailInput);

-- add Game to Tournament (M-M Relationship)
INSERT INTO Tournaments_has_Games (GameID, TournamentID)
VALUES (:GameID_from_dropdown_Input, :TournamentID_from_dropdown_Input);


----- Update -----
-- update Player information
UPDATE Players SET Name = :NameInput, Username = :UsernameInput, Birthdate = :BirthdateInput, Captain = :CaptainInput, TeamID = :TeamID_from_dropdown_Input, GameID = :GameID_from_dropdown_Input WHERE PlayerID = :PlayerID_from_dropdown_Input;

-- update Tournaments_has_Games information
UPDATE Tournaments_has_Games SET GameID = :GameID_from_dropdown_Input WHERE TournamentID = :TournamentID_from_dropdown_Input;

----- Delete -----
-- delete a Player
DELETE FROM Players WHERE PlayerID = :PlayerID_selected_from_browse_player_page;

-- disassociate a Game from a Tournament
DELETE FROM Tournaments_has_Games WHERE GameID = :GameID_selected_from_game_and_tournament_list AND TournamentID = :TournamentID_selected_from_game_and_tournament_list;