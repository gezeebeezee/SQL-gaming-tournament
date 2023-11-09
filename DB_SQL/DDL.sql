-- Group 73 Project Step 2
-- Steven Vu and Kevin Le

--
--

-- --------------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

--
-- Table structure for table `Tournaments`
--

CREATE OR REPLACE TABLE Tournaments (
  TournamentID int AUTO_INCREMENT NOT NULL UNIQUE,
  TournamentName varchar(45) NOT NULL,
  Location varchar(45) NOT NULL,
  StartDate date NOT NULL,
  EndDate date NOT NULL,
  PRIMARY KEY (TournamentID)
);

--
-- Table structure for table `Games`
--

CREATE OR REPLACE TABLE Games (
  GameID int AUTO_INCREMENT NOT NULL UNIQUE,
  Title varchar(45) NOT NULL UNIQUE,
  Genre varchar(45) NOT NULL,
  Platform varchar(45) NOT NULL,
  PRIMARY KEY (GameID)
);

--
-- Table structure for table `Sponsors`
--

CREATE OR REPLACE TABLE Sponsors (
  SponsorID int AUTO_INCREMENT NOT NULL UNIQUE,
  SponsorName varchar(45) NOT NULL UNIQUE,
  ContactPerson varchar(45) NOT NULL,
  ContactEmail varchar(45) NOT NULL,
  PRIMARY KEY (SponsorID)
);

--
-- Table structure for table `Teams`
--

CREATE OR REPLACE TABLE Teams (
  TeamID int AUTO_INCREMENT NOT NULL UNIQUE,
  TeamName varchar(50) NOT NULL UNIQUE,
  Location varchar(45) NOT NULL,
  SponsorID int,
  TournamentID int,
  Description varchar(100) DEFAULT NULL,
  PRIMARY KEY (TeamID),
  FOREIGN KEY (SponsorID) REFERENCES Sponsors(SponsorID)
    ON DELETE SET NULL,
  FOREIGN KEY (TournamentID) REFERENCES Tournaments(TournamentID)
    ON DELETE SET NULL
);

--
-- Table structure for table 'Players'
--

CREATE OR REPLACE TABLE Players (
  PlayerID int AUTO_INCREMENT NOT NULL UNIQUE,
  Name varchar(50) NOT NULL,
  Username varchar(50) NOT NULL UNIQUE,
  Birthdate date NOT NULL,
  Captain boolean DEFAULT FALSE,
  TeamID int,
  GameID int,
  PRIMARY KEY (PlayerID),
  FOREIGN KEY (GameID) REFERENCES Games(GameID)
    ON DELETE SET NULL,
  FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
    ON DELETE SET NULL
);

--
-- Table structure for table `Tournaments_has_Games`
--

CREATE OR REPLACE TABLE Tournaments_has_Games (
  GameID int NOT NULL,
  TournamentID int NOT NULL,
  PRIMARY KEY (GameID, TournamentID),
  FOREIGN KEY (GameID) REFERENCES Games(GameID)
    ON DELETE CASCADE,
  FOREIGN KEY (TournamentID) REFERENCES Tournaments(TournamentID) 
    ON DELETE CASCADE
);


--
-- Insert into 'Games'
INSERT INTO Games (Title, Genre, Platform) VALUES
('League of Legends', 'MOBA', 'PC'),
('Valorant', 'Shooter', 'PC'),
('Super Smash Bros', 'Fighting', 'Nintendo Switch'),
('Yu-Gi-Oh', 'Card', 'Tabletop');

--
-- Insert into `Tournaments`
--
INSERT INTO Tournaments (TournamentName, Location, StartDate, EndDate) VALUES
('Momocon', 'Atlanta', '2023-01-01', '2023-01-03'),
('DreamHack', 'Chicago', '2023-01-01', '2023-01-03'),
('E3', 'New York', '2023-01-01', '2023-01-03'),
('DragonCon', 'Atlanta', '2023-09-09', '2023-09-12');

--
-- Insert into `Tournaments_has_Games`
--

INSERT INTO Tournaments_has_Games (GameID, TournamentID) VALUES
(1, 3),
(2, 2),
(3, 3),
(4, 2);

--
-- Insert into 'Sponsors'
--
INSERT INTO Sponsors (SponsorName, ContactPerson, ContactEmail) VALUES
('Red Bull', 'John Doe', 'johndoe@gmail.com'),
('Honda', 'Jane Doe', 'janedoe@gmail.com'),
('Coca-Cola', 'Jack Doe', 'jackdoe@gmail.com'),
('Chipotle', 'Mary Doe', 'marydoe@gmail.com');

--
-- Insert into 'Teams'
--
INSERT INTO Teams (TeamName, Location, SponsorID, TournamentID, Description) VALUES
('TSM',  'USA ', NULL, 3, 'Hello from TSM'),
('C9', 'Germany', 4, NULL, 'Hello from C9'),
('Faze',  'Mexico', 2, 2, 'Hello from Faze'),
('T1',  'South Korea', 1, 3, 'Hello from T1');

--
-- Insert into 'Players'
--
INSERT INTO Players (Name, Username, Birthdate, Captain, TeamID, GameID) VALUES
('John Doe', 'team1user1', '2000-01-01', TRUE, NULL, 3),
('Jane Doe', 'team1user2', '1999-02-02', FALSE, 1, NULL),
('Jack Doe', 'team2user1', '1997-03-07', TRUE, 2, 4),
('Mary Doe', 'team4user1', '2000-03-09', FALSE, 4, 2);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;