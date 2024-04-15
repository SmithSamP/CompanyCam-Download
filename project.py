import requests
import json
import pandas as pd
import datetime

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
    
    def get_project_photos(self, project_id):
        """
        Gets photos for a specific CompanyCam project.

        Args:
            project_id (str): ID of the project to retrieve photos for.

        Returns:
            Pandas dataFrame containing photo details if successful,
                  raises an exception on failure.
        """
        # initialize an empty dataFrame to store photos data
        photos_dataFrame = pd.DataFrame(columns=['id', 'url', 'date', 'user', 'lat', 'lon'])

        # loop through pages of photos data
        for index in range(10000):
            # construct the URL for the API call
            url = f"{self.base_url}/projects/{project_id}/photos?page={index}&per_page=1000"
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
            
            photos_data = response.json()
            # break the loop if no more photos are available on current page
            if photos_data == []:
                break
            # Initialize a dictionary to store data for the current page
            page_data = {'id': [], 'url': [], 'date': [], 'user': [], 'lat': [], 'lon': []}
            # function to convert timestamp to readable date
            readable_date = lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
            # loop through photos data and store relevant information in the dictionary
            for photo in photos_data:
                page_data['id'].append(photo['id'])
                page_data['url'].append(photo['uris'][3]['uri'])
                # convert the timestamp to readable date
                page_data['date'].append(readable_date(photo['captured_at']))
                page_data['user'].append(photo['creator_name'])
                page_data['lat'].append(photo['coordinates']['lat'])
                page_data['lon'].append(photo['coordinates']['lon'])
            # convert the dictionary to a pandas dataFrame
            page_data = pd.DataFrame(page_data)
            # if the dataFrame is empty, assign the current page data to it otherwise concatenate the data
            if photos_dataFrame.empty:
                photos_dataFrame = page_data
                continue
            photos_dataFrame = pd.concat([photos_dataFrame, page_data], ignore_index=True)
            print(f"Retrieved page {index} of photos")
        # return the photos dataFrame
        return photos_dataFrame




# if __name__ == "__main__":
#     # Define your CompanyCam API access token
#     access_token = ""
#     project_id = "123"
#     ccproject = CompanyCamProject(access_token)
#     ccproject.get_project(project_id)
#     photos = ccproject.get_project_photos(project_id)
#     print(photos)



