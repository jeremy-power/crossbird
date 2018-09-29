def date_scrape():
    import urllib3
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
