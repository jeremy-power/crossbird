use crossnerd;
GO

CREATE PROCEDURE [dbo].[spGetWordleAverages] AS 
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
    SELECT DiscordName AS Name, ROUND(AVG(CAST(Score AS FLOAT)),2) AS Average, Count(Score) As Count FROM WordleScores
    LEFT JOIN datUsers ON WordleScores.UserID = datUsers.UserID GROUP BY DiscordName ORDER BY Average
END
ALTER PROCEDURE [dbo].[spGetWordleScores] @WordleDay datetime
AS 
BEGIN
	SET NOCOUNT ON
	
	SELECT datUsers.DiscordName as Name, WordleScores.Score as Score FROM WordleScores
	LEFT JOIN datUsers ON WordleScores.UserID = datUsers.UserID
	WHERE Day = @WordleDay
	ORDER BY Score ASC;
END
GO