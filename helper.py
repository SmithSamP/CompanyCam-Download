import datetime
def date_to_unix(date):
    only_date = date.split(' ')[0]
    month, day, year = only_date.split(r'/')
    try:
        return int(datetime.datetime(int(year), int(month), int(day)).timestamp())
    except ValueError:
        print('Invalid date format. Please provide a date in the format MM/DD/YYYY.')
        return None