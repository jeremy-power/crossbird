import datetime

date_today = datetime.datetime.today()
midnight_today = datetime.datetime(date_today.year, date_today.month, date_today.day, 0, 0, 0)

print(midnight_today)