ALTER TABLE crossnerd.dbo.datUsers
ADD WordleStreak int NOT NULL
DEFAULT 1;
ALTER TABLE crossnerd.dbo.datUsers
ADD LastWordle DATETIME NOT NULL
DEFAULT '1900-01-01 00:00:00';
CREATE TABLE crossnerd.dbo.WordleScores (
	WordleScoreID int IDENTITY(0,1) NOT NULL,
	UserID int NOT NULL,
	[Day] datetime DEFAULT getdate() NOT NULL,
	DateRecorded datetime DEFAULT getdate() NOT NULL,
	CONSTRAINT WordleScores_FK FOREIGN KEY (UserID) REFERENCES crossnerd.dbo.datUsers(UserID)
);
GO