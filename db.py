import pyodbc
import datetime
def getConnection():
    return pyodbc.connect('Driver={SQL Server};Server=den1.mssql6.gear.host;Database=crossnerd;UID=crossnerd;PWD=powerj@@;')

def build_dict(cursor):
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns,row)))
    return results

def select_all_users():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM datUsers")
    return build_dict(cursor)

def select_user_by_id(discord_id):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM datUsers WHERE DiscordID=" + str(discord_id))
    return build_dict(cursor)

def update_name(discord_id, discord_name):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("UPDATE datUsers SET DiscordName = '" + discord_name + "' WHERE DiscordID = " + str(discord_id))
    cursor.commit()

def create_score(discord_id, score, date, isArchive):
    user = select_user_by_id(discord_id)
    user_id = user[0]['UserID']
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO datScores(Score, UserID, Day, DateRecorded, isArchive) VALUES (?, ?, ?, ?, ?)",
                  (score, user_id, date, datetime.datetime.now(), int(isArchive)))
    cursor.commit()
create_score(1, 10, datetime.datetime.now(), True)