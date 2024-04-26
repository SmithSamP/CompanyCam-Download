import project
import pandas as pd
import datetime
import datetime
import time

# Read token from file
with open('token.txt', 'r') as file:
    token = file.read().strip()

# Assign token to variable
project_id = '53678019'

# Create a project object
readable_date = lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')

# importing datetime module
def date_to_timestamp(date):
    return int(datetime.datetime.timestamp(date))

start_date = date_to_timestamp(datetime.datetime(2024, 4, 15))
end_date = date_to_timestamp(datetime.datetime(2024, 4, 16))

my_project = project.CompanyCamProject(token)

# Get project details
# my_project.get_project(project_id)

# Get project photos as Pandas dataFrame
photos = my_project.get_project_photos(project_id)
print(photos)

