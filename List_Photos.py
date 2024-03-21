import requests
import json
import datetime
import time
import os

# Update with your CompanyCam API Key
API_KEY = "3l9yTx2hpThgklu2kWM9cdhNT39QPM5sHSyGJ3R_PQ0"

# Define time frame for photos (YYYY-MM-DD format)
start_time = "2024-03-13 00:00:00"
end_time = "2024-03-13 23:59:59"

# Convert start time to Unix timestamp
start_datetime = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
start_timestamp = int(start_datetime.timestamp())

# Convert end time to Unix timestamp
end_datetime = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
end_timestamp = int(end_datetime.timestamp())


def get_photos(start, end, page=1):
    url = f"https://api.companycam.com/v2/photos?start_date={start}&end_date={end}&per_page=100&page={page}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    for photo in data:
        download_photo(photo["uris"][3]["uri"], photo["id"])

    # Check for next page
    page += 1
    data = response.json()
    if len(data) > 0:
        get_photos(start_timestamp, end_timestamp, page)

def download_photo(photo_url, filename):
    response = requests.get(photo_url, stream=True)

    if response.status_code == 200:
        with open(f"D:/CompanyCam Photos/{filename}.jpg", 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded photo: {filename}.jpg")
    else:
        print(f"Failed to download photo: {filename}")

def count_files(folder_path):
    file_count = 0

    # Iterate over all the files in the folder
    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count

# Time the script
start_time = time.time()
get_photos(start_timestamp, end_timestamp, 1)
end_time = time.time()
execution_time = end_time - start_time
print(f"Script execution time: {execution_time} seconds. Downloaded {count_files(r'D:\CompanyCam Photos')} photos.")

