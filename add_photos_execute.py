import project
import pandas as pd

# Read token from file
with open('token.txt', 'r') as file:
    token = file.read().strip()

# Assign token to variable
project_id = '62535134'

# Create a project object

my_project = project.CompanyCamProject(token)

# Get project details
# my_project.get_project(project_id)

# Get project photos as Pandas dataFrame
photos = my_project.get_project_photos(project_id)

# Write photos to CSV
photos.to_csv('photos.csv', index=False)

