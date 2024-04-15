import requests
import json
import os

def download_companycam_photos(webhook_url, project_id, api_key, download_dir):
    """
    Downloads photos uploaded to the specified CompanyCam project using webhooks.

    Args:
        webhook_url (str): URL of the CompanyCam webhook endpoint.
        project_id (str): ID of the project to monitor for photo uploads.
        api_key (str): Your CompanyCam API key for authentication.
        download_dir (str): Local directory to save downloaded photos.
    """

    def handle_webhook(data):
        """
        Processes incoming webhook data to identify photo uploads.

        Args:
            data (dict): Dictionary containing webhook payload.

        Returns:
            bool: True if a photo upload was detected, False otherwise.
        """

        # Implement logic to check if the payload indicates a photo upload
        # for the specified project based on CompanyCam's webhook structure.
        # This might involve checking for keys like "project_id", "item_type", etc.

        if photo_upload_detected(data, project_id):
            photo_url = extract_photo_url(data)
            download_photo(photo_url, download_dir)
            return True
        else:
            return False

    def download_photo(photo_url, download_dir):
        """
        Downloads a photo from the given URL to the specified directory.

        Args:
            photo_url (str): URL of the photo to download.
            download_dir (str): Local directory to save the downloaded photo.
        """

        response = requests.get(photo_url, stream=True)
        response.raise_for_status()

        filename = os.path.basename(photo_url)
        filepath = os.path.join(download_dir, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Downloaded photo: {filename}")

    def photo_upload_detected(data, project_id):
        # Replace with your logic to check for photo upload in the webhook payload
        # based on CompanyCam's documentation
        return data.get("project_id") == project_id and data.get("item_type") == "photo"

    def extract_photo_url(data):
        # Replace with your logic to extract the photo URL from the webhook payload
        # based on CompanyCam's documentation
        return data.get("url")

    # Set up webhook listener (implementation depends on your environment)
    # You'll need to establish a mechanism to listen for incoming webhooks
    # at the provided URL. This might involve using a web framework like Flask
    # or a dedicated library for handling webhooks.

    while True:  # Continuously listen for webhooks
        try:
            # Replace with code to receive and parse webhook data
            data = receive_webhook_data()
            handle_webhook(data)
        except requests.exceptions.RequestException as e:
            print(f"Error processing webhook: {e}")

if __name__ == "__main__":
    # Replace with your actual values from CompanyCam
    webhook_url = "https://your-companycam-webhook-url.com"
    project_id = "your_project_id"
    api_key = "your_companycam_api_key"
    download_dir = "/path/to/download/directory"

    download_companycam_photos(webhook_url, project_id, api_key, download_dir)
