import requests
import json
import pandas as pd
import datetime
import piexif
from progress.bar import Bar

class CompanyCamProject:
    """
    A class representing a CompanyCam project with methods for CRUD operations.
    Requires a valid CompanyCam API access token for authentication.
    """

    def __init__(self, api_token, base_url="https://api.companycam.com/v2"):
        """
        Initializes a CompanyCamProject object.

        Args:
            api_token (str): Your CompanyCam API access token.
            base_url (str, optional): Base URL for the CompanyCam API (defaults to "https://api.companycam.com/v2").
        """

        self.api_token = api_token
        self.base_url = base_url
        self.name = None
        self.id = None
        self.project_number = None

        # Set headers with authorization for API calls
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def __str__(self):
        if self.name != None and self.id != None:
            return f"CompanyCam Project: {self.name}, ID: {self.id}"
        
        return "CompanyCam Project not defined. Run get_project() to retrieve project details."


    def get_project(self, project_id):
        """
        Gets details of a specific CompanyCam project.

        Args:
            project_id (str): ID of the project to retrieve.

        Returns:
            dict: Dictionary containing project details if successful,
                  raises an exception on failure.
        """
        # construct the URL for the API call
        url = f"{self.base_url}/projects/{project_id}"
        # make the API call
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f'Invalid project ID. Please provide a valid project ID. Error: {err}')
            return None
        except requests.exceptions.ConnectionError as err:
            print(f'Could not connect. Error: {err}')
            return None
        # parse the response data 
        project_data = response.json()
        # store the project details in the object attributes
        self.name = project_data["name"]
        self.id = project_data["id"]
        self.project_number = project_data["name"].split(" ")[0]
        # return the project details
        return project_data
    
    def get_project_photos(self, project_id, start_date=None, end_date=None):
        """
        Gets photos for a specific CompanyCam project.

        Args:
            project_id (str): ID of the project to retrieve photos for.

        Returns:
            Pandas dataFrame containing photo details if successful,
                  raises an exception on failure.
        """
        # initialize an empty dataFrame to store photos data
        photos_dataFrame = pd.DataFrame(columns=['id', 'url', 'date', 'user', 'project', 'lat', 'lon'])

        # loop through pages of photos data
        for index in range(1,10000):
            # construct the URL for the API call
            url = f"{self.base_url}/projects/{project_id}/photos?page={index}&per_page=1000"

            if start_date != None:
                url += f"&start_date={start_date}"

            if end_date != None:
                url += f"&end_date={end_date}"
            # make the API call
            page_data = self.make_api_call(url)
            # convert the dictionary to a pandas dataFrame
            if page_data is None:
                break
            # if the dataFrame is empty, assign the current page data to it otherwise concatenate the data
            if photos_dataFrame.empty:
                photos_dataFrame = page_data
                continue
            photos_dataFrame = pd.concat([photos_dataFrame, page_data], ignore_index=True)
            print(f"Retrieved page {index} of photos")
        # return the photos dataFrame
        return photos_dataFrame
    
    def get_group_photos(self, group_id, start_date=None, end_date=None):
        """
        Gets photos for a specific CompanyCam group.

        Args:
            group_id (str): ID of the group to retrieve photos for.

        Returns:
            Pandas dataFrame containing photo details if successful,
                  raises an exception on failure.
        """
        # initialize an empty dataFrame to store photos data
        photos_dataFrame = pd.DataFrame(columns=['id', 'url', 'date', 'user', 'project', 'lat', 'lon'])

        # loop through pages of photos data
        for index in range(1,10000):
            # construct the URL for the API call
            url = f"{self.base_url}/photos?page={index}&per_page=1000&group_ids={group_id}"

            if start_date != None:
                url += f"&start_date={start_date}"

            if end_date != None:
                url += f"&end_date={end_date}"

            # make the API call
            page_data = self.make_api_call(url)
            # convert the dictionary to a pandas dataFrame
            print(f"Retrieved page {index} of photos")
            if page_data is None:
                break
            # if the dataFrame is empty, assign the current page data to it otherwise concatenate the data
            if photos_dataFrame.empty:
                photos_dataFrame = page_data
                continue
            photos_dataFrame = pd.concat([photos_dataFrame, page_data], ignore_index=True)

        # return the photos dataFrame
        return photos_dataFrame
    
    def make_api_call(self,url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f'Invalid project ID. Please provide a valid project ID. Error: {err}')
            return None
        except requests.exceptions.ConnectionError as err:
            print(f'Could not connect. Error: {err}')
            return None
        
        photos_data = response.json()
        # break the loop if no more photos are available on current page
        if photos_data == []:
            return None
        # Initialize a dictionary to store data for the current page
        page_data = {'id': [], 'url': [], 'date': [], 'user': [], 'project': [], 'lat': [], 'lon': []}
        # function to convert timestamp to readable date

        # loop through photos data and store relevant information in the dictionary
        for photo in photos_data:
            page_data['id'].append(photo['id'])
            page_data['url'].append(photo['uris'][3]['uri'])
            # convert the timestamp to readable date
            page_data['date'].append(photo['captured_at'])
            page_data['user'].append(photo['creator_name'])
            page_data['project'].append(photo['project_id'])
            page_data['lat'].append(photo['coordinates']['lat'])
            page_data['lon'].append(photo['coordinates']['lon'])
        return pd.DataFrame(page_data)
    
    def download_photo(self, photo_url, filename):
        """
        Downloads a photo from a given URL and saves it to a file.

        Args:
            photo_url (str): URL of the photo to download.
            filename (str): Name of the file to save the photo to.

        Returns:
            bool: True if successful, False otherwise.
        """
        # make the API call to download the photo
        response = requests.get(photo_url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)

            exif_dict = piexif.load(filename)  # Load EXIF data
            # ... You can also modify EXIF data here if needed ... 
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, filename)
            return True
        else:
            return False



if __name__ == "__main__":
    start_time = 1713423600
    end_time = 1713510000
    #     # Define your CompanyCam API access token
    with open('token.txt', 'r') as file:
        token = file.read().strip()

    # Assign token to variable
    project_id = '62018691'
    ccproject = CompanyCamProject(token)
    ccproject.get_project(project_id)
    # photos = ccproject.get_project_photos(project_id, start_time, end_time)
    group_id = '11083'
    photos = ccproject.get_group_photos(group_id, start_time, end_time)
    with Bar('Processing...',suffix='%(percent)d%%- %(eta)ds',max=len(photos)) as bar:
        for index, row in photos.iterrows():
            filename = 'D:\\Photos\\'+f"photo_{row['id']}.jpg"
            ccproject.download_photo(row['url'], filename)
            bar.next()
    print(f"Downloaded {len(photos)} photos.")



