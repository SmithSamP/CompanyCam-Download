import project
import pandas as pd
import datetime
import helper
from progress.bar import Bar


while True:
    try:
        start_date = helper.date_to_unix(input('Enter the start date in the format MM/DD/YYYY: '))
        print('-------------------------------------------')
        break
    except ValueError:
        print('Invalid date format. Please provide a date in the format MM/DD/YYYY.')
        continue
    
end_date = start_date + 86400

with open('token.txt', 'r') as file:
    token = file.read().strip()


ccproject = project.CompanyCamProject(token)


group_id = '11083'
photos = ccproject.get_group_photos(group_id, start_date, end_date)
with Bar('Processing...',suffix='%(percent)d%%- %(eta)ds',max=len(photos)) as bar:
    for index, row in photos.iterrows():
        filename = 'D:\\Photos\\'+f"photo_{row['id']}.jpg"
        # ccproject.download_photo(row['url'], filename)
        bar.next()
