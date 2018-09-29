import pyodbc

def getConnection():
    return pyodbc.connect('Driver={SQL Server};Server=den1.mssql6.gear.host;Database=crossnerd;UID=crossnerd;PWD=powerj@@;')

# cursor = connection.cursor()
# cursor.execute("INSERT INTO datUsers(DiscordID, DiscordName) VALUES (1, 'test');")
# connection.commit()

