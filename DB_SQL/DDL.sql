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
  tournamentID int AUTO_INCREMENT NOT NULL UNIQUE,
  tournamentName varchar(45) NOT NULL UNIQUE,
  location varchar(45) NOT NULL,
  startDate date NOT NULL,
  endDate date NOT NULL,
  PRIMARY KEY (tournamentID)
);

--
-- Table structure for table `Games`
--

CREATE OR REPLACE TABLE Games (
  gameID int AUTO_INCREMENT NOT NULL UNIQUE,
  title varchar(45) NOT NULL UNIQUE,
  genre varchar(45) NOT NULL,
  platform varchar(45) NOT NULL,
  PRIMARY KEY (gameID)
);

--
-- Table structure for table `Sponsors`
--

CREATE OR REPLACE TABLE Sponsors (
  sponsorID int AUTO_INCREMENT NOT NULL UNIQUE,
  sponsorName varchar(45) NOT NULL UNIQUE,
  contactPerson varchar(45) NOT NULL,
  contactEmail varchar(45) NOT NULL,
  PRIMARY KEY (sponsorID)
);

--
-- Table structure for table `Teams`
--

CREATE OR REPLACE TABLE Teams (
  teamID int AUTO_INCREMENT NOT NULL UNIQUE,
  teamName varchar(50) NOT NULL UNIQUE,
  location varchar(45) NOT NULL,
  sponsorID int,
  tournamentID int,
  description varchar(500) DEFAULT NULL,
  PRIMARY KEY (teamID),
  FOREIGN KEY (sponsorID) REFERENCES Sponsors(sponsorID)
    ON DELETE SET NULL,
  FOREIGN KEY (tournamentID) REFERENCES Tournaments(tournamentID)
    ON DELETE SET NULL
);

--
-- Table structure for table 'Players'
--

CREATE OR REPLACE TABLE Players (
  playerID int AUTO_INCREMENT NOT NULL UNIQUE,
  name varchar(50) NOT NULL,
  username varchar(50) NOT NULL UNIQUE,
  birthdate date NOT NULL,
  captain boolean DEFAULT FALSE,
  teamID int,
  gameID int,
  PRIMARY KEY (playerID),
  FOREIGN KEY (gameID) REFERENCES Games(gameID)
    ON DELETE SET NULL,
  FOREIGN KEY (teamID) REFERENCES Teams(teamID)
    ON DELETE SET NULL
);

--
-- Table structure for table `Tournaments_has_Games`
--

CREATE OR REPLACE TABLE Tournaments_has_Games (
  gameID int NOT NULL,
  tournamentID int NOT NULL,
  PRIMARY KEY (gameID, tournamentID),
  FOREIGN KEY (gameID) REFERENCES Games(gameID)
    ON DELETE CASCADE,
  FOREIGN KEY (tournamentID) REFERENCES Tournaments(tournamentID) 
    ON DELETE CASCADE
);


--
-- Insert into 'Games'
INSERT INTO Games (title, genre, platform) VALUES
('League of Legends', 'MOBA', 'PC'),
('Valorant', 'Shooter', 'PC'),
('Super Smash Bros', 'Fighting', 'Nintendo Switch'),
('Yu-Gi-Oh', 'Card', 'Tabletop');

--
-- Insert into `Tournaments`
--
INSERT INTO Tournaments (tournamentName, location, startDate, endDate) VALUES
('Momocon', 'Atlanta', '2023-01-01', '2023-01-03'),
('DreamHack', 'Chicago', '2023-01-01', '2023-01-03'),
('E3', 'New York', '2023-01-01', '2023-01-03'),
('DragonCon', 'Atlanta', '2023-09-09', '2023-09-12');

--
-- Insert into `Tournaments_has_Games`
--

INSERT INTO Tournaments_has_Games (gameID, tournamentID) VALUES
(1, 3),
(2, 2),
(3, 3),
(4, 2);

--
-- Insert into 'Sponsors'
--
INSERT INTO Sponsors (sponsorName, contactPerson, contactEmail) VALUES
('Red Bull', 'John Doe', 'johndoe@gmail.com'),
('Honda', 'Jane Doe', 'janedoe@gmail.com'),
('Coca-Cola', 'Jack Doe', 'jackdoe@gmail.com'),
('Chipotle', 'Mary Doe', 'marydoe@gmail.com');

--
-- Insert into 'Teams'
--
INSERT INTO Teams (teamName, location, sponsorID, tournamentID, description) VALUES
('TSM',  'USA ', NULL, 3, 'Hello from TSM'),
('C9', 'Germany', 4, NULL, 'Hello from C9'),
('Faze',  'Mexico', 2, 2, 'Hello from Faze'),
('T1',  'South Korea', 1, 3, 'Hello from T1');

--
-- Insert into 'Players'
--
INSERT INTO Players (name, username, birthdate, captain, teamID, gameID) VALUES
('John Doe', 'team1user1', '2000-01-01', TRUE, NULL, 3),
('Jane Doe', 'team1user2', '1999-02-02', FALSE, 1, NULL),
('Jack Doe', 'team2user1', '1997-03-07', TRUE, 2, 4),
('Mary Doe', 'team4user1', '2000-03-09', FALSE, 4, 2);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;