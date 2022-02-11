import pyodbc
import datetime
import os

def get_db_string():
    script_path = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_path = "db.txt"
    full_file_path = os.path.join(script_path, file_path)
    with open(full_file_path) as f:
        read_data = f.read()
    f.closed
    return read_data

def get_connection():
    return pyodbc.connect(get_db_string(), autocommit=True)

connection = get_connection()

def build_dict(cursor):
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns,row)))
    return results

def select_all_users():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM datUsers")
    return build_dict(cursor)

def select_user_by_id(discord_id):
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM datUsers WHERE DiscordID=" + str(discord_id))
    return build_dict(cursor)

def update_name(discord_id, discord_name):
    cursor = connection.cursor()
    cursor.execute("UPDATE datUsers SET DiscordName = '" + discord_name + "' WHERE DiscordID = " + str(discord_id))
    cursor.commit()

def create_score(discord_id, score, date, isArchive):
    user = select_user_by_id(discord_id)
    user_id = user[0]['UserID']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO datScores(Score, UserID, Day, DateRecorded, isArchive) VALUES (?, ?, ?, ?, ?)",
                  (score, user_id, date, datetime.datetime.now(), int(isArchive)))
    cursor.commit()
    update_date_to_now(discord_id, isArchive)

def create_wordle_score(discord_id, score, date):
    user = select_user_by_id(discord_id)
    user_id = user[0]['UserID']
    cursor = connection.cursor()
    cursor.execute("INSERT INTO datScores(Score, UserID, Day, DateRecorded) VALUES (?, ?, ?, ?)",
                  (score, user_id, date, datetime.datetime.now()))
    cursor.commit()
    update_wordle_date_to_now(discord_id)
    
def create_user(discord_id, discord_name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO datUsers(DiscordID, DiscordName) VALUES (" + discord_id + ", '" + discord_name +"');")
    connection.commit()

def update_date_to_now(discord_id, isArchive):
    cursor = connection.cursor()
    if(isArchive):
        cursor.execute("UPDATE datUsers SET LastArchive = ? WHERE DiscordID = ?", (datetime.datetime.now(), discord_id))
    else:
        cursor.execute("UPDATE datUsers SET LastCrossword = ? WHERE DiscordID = ?", (datetime.datetime.now(), discord_id))
    connection.commit()

def update_wordle_date_to_now(discord_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE datUsers SET LastWordle = ? WHERE DiscordID = ?", (datetime.datetime.now(), discord_id))
    connection.commit()

def get_last_date(discord_id, isArchive):
    user = select_user_by_id(discord_id)
    user_id = user[0]['UserID']
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM datScores WHERE userID = ? AND isArchive = ? ORDER BY datScores.Day DESC", user_id, int(isArchive))
    results = build_dict(cursor)
    if len(results) == 0:
        return datetime.datetime(1900,1,1)
    else:
        return results[0]['Day']

def get_last_wordle_date(discord_id):
    user = select_user_by_id(discord_id)
    user_id = user[0]['UserID']
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 LastWordle FROM datUsers WHERE UserID = ?", user_id)
    results = build_dict(cursor)
    if len(results) == 0:
        return datetime.datetime(1900,1,1)
    else:
        return results[0]['LastWordle']

def date_compare(date1, date2):
    if(date1.date() == date2.date()):
        return True
    else:
        return False

def update_streak(discord_id, isContinued):
    cursor = connection.cursor()
    if isContinued:
        cursor.execute("UPDATE datUsers SET Streak = Streak + 1 WHERE DiscordID = ?", discord_id)
    else:
        cursor.execute("UPDATE datUsers SET Streak = 1 WHERE DiscordID = ?", discord_id)

def update_wordle_streak(discord_id, isContinued):
    cursor = connection.cursor()
    if isContinued:
        cursor.execute("UPDATE datUsers SET WordleStreak = WordleStreakStreak + 1 WHERE DiscordID = ?", discord_id)
    else:
        cursor.execute("UPDATE datUsers SET WordleStreak = 1 WHERE DiscordID = ?", discord_id)

def get_streak(discord_id):
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM datUsers WHERE DiscordID = ?", discord_id)
    results = build_dict(cursor)
    user_streak = results[0]['Streak']
    return user_streak

def get_wordle_streak(discord_id):
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM datUsers WHERE DiscordID = ?", discord_id)
    results = build_dict(cursor)
    user_streak = results[0]['WordleStreak']
    return user_streak

def get_scores_for_day(date):
    cursor = connection.cursor()
    cursor.execute("exec sp_BuildDateView ?", date)
    results = build_dict(cursor)
    return results

def get_streaks():
    cursor = connection.cursor()
    cursor.execute("SELECT DiscordName, Streak FROM datUsers WHERE Streak > 1 ORDER BY Streak DESC")
    results = build_dict(cursor)
    return results

def update_joel_date(date):
    cursor = connection.cursor()
    cursor.execute("exec spRefreshCurrentJoelDay ?", date)

def get_last_joel_date():
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM tmpCurrentJoelDay")
    results = build_dict(cursor)
    return results[0]["CurrentDay"]

def insert_refresh_time():
    cursor = connection.cursor()
    cursor.execute("INSERT INTO datRefreshTime(RefreshTime) VALUES (?)", datetime.datetime.now())

def get_averages():
    cursor = connection.cursor()
    cursor.execute("exec spGetAveragesByUser")
    results = build_dict(cursor)
    return results
    
def get_top_scores():
    cursor = connection.cursor()
    cursor.execute("exec spGetTopScores")
    results = build_dict(cursor)
    return results

def get_best_score_by_user(userID):
    cursor = connection.cursor()
    cursor.execute("exec spGetTopScoreByUser ?", userID)
    results = build_dict(cursor)
    return results

def get_average_by_day(date):
    cursor = connection.cursor()
    cursor.execute("exec spGetAverageByDay ?", date)
    results = build_dict(cursor)
    return results