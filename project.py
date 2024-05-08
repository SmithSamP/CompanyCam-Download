import requests
import json
import pandas as pd
import datetime

# import piexif
from progress.bar import Bar


class CompanyCam:
    def __init__(self, api_token, base_url="https://api.companycam.com/v2"):
        self.api_token = api_token
        self.base_url = base_url
        self.name = None
        self.id = None
        self.project_number = None
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def __str__(self):
        if self.name != None and self.id != None:
            return f"CompanyCam Project: {self.name}, ID: {self.id}"

        return "CompanyCam Project not defined. Run get_project() to retrieve project details."

    def get_project(self, project_id):
        url = f"{self.base_url}/projects/{project_id}"
        response = self.get_response(url)
        project_data = response.json()
        self.name = project_data["name"]
        self.id = project_data["id"]
        self.project_number = project_data["name"].split(" ")[0]
        return project_data

    def get_groups(self):
        url = f"{self.base_url}/groups?per_page=1000"
        response = self.get_response(url)
        groups_data = response.json()
        groups_df = pd.DataFrame(groups_data)
        return groups_df

    def get_photos(self, start_date=None, end_date=None):
        url = f"{self.base_url}/photos?page=***&per_page=1000"
        photos_dataFrame = self.build_dataframe(url, start_date, end_date)
        return photos_dataFrame

    def get_project_photos(self, project_id, start_date=None, end_date=None):
        url = f"{self.base_url}/projects/{project_id}/photos?page=***&per_page=1000"
        photos_dataFrame = self.build_dataframe(url, start_date, end_date)
        return photos_dataFrame

    def get_group_photos(self, group_id, start_date=None, end_date=None):
        url = f"{self.base_url}/photos?page=***&per_page=1000&group_ids={group_id}"
        photos_dataFrame = self.build_dataframe(url, start_date, end_date)
        return photos_dataFrame

    def get_response(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            print(
                f"Invalid project ID. Please provide a valid project ID. Error: {err}"
            )
            return None
        except requests.exceptions.ConnectionError as err:
            print(f"Could not connect. Error: {err}")
            return None

    def make_api_call(self, url):
        response = self.get_response(url)
        photos_data = response.json()
        if photos_data == []:
            return None
        page_df = pd.DataFrame(photos_data)
        return page_df

    def build_dataframe(self, url, start_date=None, end_date=None):
        photos_dataFrame = pd.DataFrame()
        if start_date != None:
            url += f"&start_date={start_date}"

        if end_date != None:
            url += f"&end_date={end_date}"

        for index in range(1, 10000):
            indexed_url = url.replace("***", str(index))
            page_data = self.make_api_call(indexed_url)
            print(f"Retrieved page {index} of photos")
            if page_data is None:
                break
            if photos_dataFrame.empty:
                photos_dataFrame = page_data
                continue
            photos_dataFrame = pd.concat(
                [photos_dataFrame, page_data], ignore_index=True
            )
        return photos_dataFrame

    def download_photo(self, photo_url, filename):
        response = requests.get(photo_url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            return True
        else:
            return False
