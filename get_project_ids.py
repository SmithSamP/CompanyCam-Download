import requests

url = "https://api.companycam.com/v2/projects"

headers = {
    "accept": "application/json",
    "authorization": "Bearer 3l9yTx2hpThgklu2kWM9cdhNT39QPM5sHSyGJ3R_PQ0"
}



response = requests.get(url, headers=headers)
response.raise_for_status()
projects_data = response.json()

for project in projects_data:
    print(project["name"], project["id"])