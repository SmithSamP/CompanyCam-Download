import project
import pandas as pd
import datetime
import helper
from progress.bar import Bar
import os
from configparser import ConfigParser


while True:
    try:
        start_date = helper.date_to_unix(
            input("Enter the start date in the format MM/DD/YYYY: ")
        )
        print("-------------------------------------------")
        break
    except ValueError:
        print("Invalid date format. Please provide a date in the format MM/DD/YYYY.")
        continue

end_date = start_date + 86400

configur = ConfigParser()
configur.read("config.ini")

token = configur.get("companycam", "token")
download_path = configur.get("companycam", "download_path")

date_str = datetime.datetime.fromtimestamp(int(start_date)).strftime("%Y%m%d")
base_folder = download_path + "\\" + date_str + "_CC_photos"


os.makedirs(base_folder, exist_ok=True)

ccam = project.CompanyCam(token)

groups = ccam.get_groups()


for index, row in groups.iterrows():
    id = row["id"]
    name = row["name"]
    group_path = base_folder + "\\" + name
    os.makedirs(group_path, exist_ok=True)
    photos = ccam.get_group_photos(id, start_date, end_date)
    if photos.empty:
        print(f"No photos found for {name}.")
        continue

    grouped_photos = photos.groupby("project_id")

    with Bar(
        f"Processing {name}...", suffix="%(percent)d%%- %(eta)ds", max=len(photos)
    ) as bar:
        for project_id, project_photos in grouped_photos:
            ccam.get_project(project_id)
            project_name = ccam.name.strip()
            project_path = group_path + "\\" + project_name
            os.makedirs(project_path, exist_ok=True)

            for index, row in project_photos.iterrows():
                filename = project_path + "\\" + f"{date_str}_photo_{row['id']}.jpg"
                ccam.download_photo(row["uris"][3]["uri"], filename)
                bar.next()
