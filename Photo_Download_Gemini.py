import requests
import json
import datetime

# Update with your CompanyCam API Key
API_KEY = "3l9yTx2hpThgklu2kWM9cdhNT39QPM5sHSyGJ3R_PQ0"

# Define time frame for photos (YYYY-MM-DD format)


start_time = "2024-03-15 00:00:00"
end_time = "2024-03-15 23:59:59"

# Convert start time to Unix timestamp
start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
start_timestamp = int(start_datetime.timestamp())

# Convert end time to Unix timestamp
end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
end_timestamp = int(end_datetime.timestamp())


# Optional: Specify project IDs (leave empty list [] for all projects)
project_ids = []




def get_photos(project_id, page=1):
    url = f"https://api.companycam.com/v2/projects/{project_id}/photos?pageSize=100&page={page}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Write data to a text file


    for photo in data:
        if start_timestamp <= photo["created_at"] <= end_timestamp:
            download_photo(photo["uris"][3]["uri"], photo["id"])

    # Check for next page
    page += 1
    data = response.json()
    if len(data) > 0:
        get_photos(project_id, page)


def download_photo(photo_url, filename):
    response = requests.get(photo_url, stream=True)

    if response.status_code == 200:
        with open(f"photos/{filename}.jpg", 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded photo: {filename}.jpg")
    else:
        print(f"Failed to download photo: {filename}")


# Get list of projects
url = "https://api.companycam.com/v2/projects"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
projects = response.json()

# Process each project
for project in projects:
    if not project_ids or project["id"] in project_ids:
        print(f"Downloading photos from project: {project['name']}")
        get_photos(project["id"])

print("Download complete!")
