__author__ = "Jeremy Power and Logan Groves"

import os
import logging
from db import *
from messages import *

def get_token():
    script_path = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_path = "token.txt"
    full_file_path = os.path.join(script_path, file_path)
    with open(full_file_path) as f:
        read_data = f.read()
    f.closed
    return read_data

def date_scrape():
    import datetime
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        'https://www.nytimes.com/crosswords/game/mini'
    )
    r = str(r.data)
    r = r.split('<title data-react-helmet="true">',1)
    r = r[1]
    r = r.split(' Daily Mini Crossword Puzzle',1)
    r = r[0]

    #The following is done to convert to a datetime object
    r = r.split(' ')
    r[1] = r[1].replace(",", "")
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = r[0].strip()[:3].lower()
    r[0] = m[s]
    r = datetime.datetime(int(r[2]),int(r[0]),int(r[1]))

    return(r)

def time_to_number(time):
    time = time.split(':')
    time_len = len(time)
    if time_len == 1:
        time = int(time[0])
    elif time_len == 2:
        time = int(time[0])*60+int(time[1])
    elif time_len == 3:
        time = int(time[0])*3600+int(time[1])*60+int(time[2])
    else:
        time = -1
    return(time)


def enter_score(discord_id, discord_name, score, date, isArchive):
    #find the user by their discord ID
    current_crossword_date = date_scrape()
    user = select_user_by_id(discord_id)
    #if user doesn't exist yet, create one
    if len(user) == 0:
        create_user(discord_id, discord_name)
    #otherwise if their name has changed, update it
    elif user[0]['DiscordName'] != discord_name:
        update_name(discord_id, discord_name)
    #make sure user exists now
    user = select_user_by_id(discord_id)
    if len(user) != 0:
        #if it does, add the score
        if(isArchive):
            if not (date_compare(get_last_date(discord_id, isArchive), current_crossword_date)):
                create_score(discord_id, score, date, isArchive)
                return 1
            else:
                return 0
        else:
            if not (date_compare(get_last_date(discord_id, isArchive), current_crossword_date)):
                check_streak(discord_id, current_crossword_date)
                create_score(discord_id, score, date, isArchive)
                return 1
            else:
                return 0
    else:
        return 0

def check_streak(discord_id, current_crossword_date):
    last_date = get_last_date(discord_id, False)
    if (last_date.date() == (current_crossword_date - datetime.timedelta(days=1)).date()):
        update_streak(discord_id, True)
    else:
        update_streak(discord_id, False)

def seconds_to_minutes(seconds):
    minutes = divmod(seconds, 60)
    if minutes[1] < 10:
        response = str(minutes[0]) + ":0" + str(minutes[1])
    else:
        response = str(minutes[0]) + ":" + str(minutes[1])
    return response

async def build_streak_string(client, message):
    streak_dict = get_streaks()
    output_string = ""
    if streak_dict:
        output_string += """```
  Name         |  Streak
--------------------------"""
        for streak in streak_dict:
            output_string += "\n "
            output_string += '{:13}'.format(streak['DiscordName'][:13])
            output_string += " |"
            output_string += '{:>5}'.format(str(streak['Streak']))
        output_string += "```"
    return output_string


async def build_score_string(client, message, date):
    score_dict = get_scores_for_day(date)
    cscore_list = []
    ascore_list = []
    if not score_dict:
        await no_scores(client, message)
    else:
        output_string = """```
  Name         |  Crossword |   Archive
----------------------------------------"""
        for score in score_dict:
            output_string += "\n "
            output_string += '{:13}'.format(score['Name'][:13])
            output_string += " |"
            if score['CScore'] is not None:
                output_string += seconds_to_minutes(score['CScore']).center(12, ' ')
                cscore_list.append(score['CScore'])
            else:
                output_string += '{:12}'.format(" ")
            output_string += "|" 
            if score['AScore'] is not None:
                output_string += '{:>8}'.format(seconds_to_minutes(score['AScore']))
                ascore_list.append(score['AScore'])
            else:
                output_string += '{:>8}'.format(" ")
        if((len(cscore_list) > 1) or (len(ascore_list) > 1)):
            output_string += """ 
----------------------------------------\n"""
            output_string += '{:14}'.format(" Average")
            output_string += " |"

            if cscore_list:
                cscore_average = int(round(sum(cscore_list)/len(cscore_list)))
                output_string += seconds_to_minutes(cscore_average).center(12, ' ')
            else:
                output_string += '{:12}'.format(" ")
            output_string += "|" 
            if ascore_list:
                ascore_average = int(round(sum(ascore_list)/len(ascore_list)))
                output_string += '{:>8}'.format(seconds_to_minutes(ascore_average))
            else:
                output_string += '{:>8}'.format(" ")
            output_string += "```"
    if len(output_string) > 2000:
        output_string = output_string[:1997]
        output_string += "```"
    return output_string