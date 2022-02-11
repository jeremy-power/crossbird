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
	Score int NOT NULL,
	CONSTRAINT WordleScores_FK FOREIGN KEY (UserID) REFERENCES crossnerd.dbo.datUsers(UserID)
);
CREATE PROCEDURE dbo.spGetWordleScores @WordleDay datetime
AS 
BEGIN
	SET NOCOUNT ON
	
	SELECT datUsers.DiscordName as Name, WordleScores.Score as Score FROM WordleScores
	LEFT JOIN datUsers ON WordleScores.UserID = datUsers.UserID
	WHERE Day = @WordleDay
END
GO