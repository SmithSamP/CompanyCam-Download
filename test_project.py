import unittest
from unittest.mock import patch
from project import CompanyCamProject
import requests

class TestCompanyCamProject(unittest.TestCase):

    def setUp(self):
        self.access_token = "3l9yTx2hpThgklu2kWM9cdhNT39QPM5sHSyGJ3R_PQ0"
        self.project_id = "123"
        self.ccproject = CompanyCamProject(self.access_token)

    @patch('requests.get')
    def test_get_project_success(self, mock_get):
        # Mock the API response
        mock_response = {
            "name": "Test Project",
            "id": "123",
            "project_number": "T123"
        }
        mock_get.return_value.json.return_value = mock_response
        # Call the method
        project_data = self.ccproject.get_project(self.project_id)
        # Assert the results
        self.assertEqual(project_data, mock_response)
        self.assertEqual(self.ccproject.name, "Test Project")
        self.assertEqual(self.ccproject.id, "123")
        self.assertEqual(self.ccproject.project_number, "T123")

    @patch('requests.get')
    def test_get_project_failure(self, mock_get):
        # Mock the API response with an error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Invalid project ID")
        # Call the method
        project_data = self.ccproject.get_project(self.project_id)
        # Assert the results
        self.assertIsNone(project_data)
        self.assertIsNone(self.ccproject.name)
        self.assertIsNone(self.ccproject.id)
        self.assertIsNone(self.ccproject.project_number)

    @patch('requests.get')
    def test_get_project_photos_success(self, mock_get):
        # Mock the API response
        mock_response = [
            {
                "id": "1",
                "uris": [{"uri": "https://example.com/photo1.jpg"}],
                "captured_at": "2022-01-01",
                "creator_name": "John Doe",
                "coordinates": {"lat": 123, "lon": 456}
            },
            {
                "id": "2",
                "uris": [{"uri": "https://example.com/photo2.jpg"}],
                "captured_at": "2022-01-02",
                "creator_name": "Jane Smith",
                "coordinates": {"lat": 789, "lon": 12}
            }
        ]
        mock_get.return_value.json.return_value = mock_response
        # Call the method
        photos_dataFrame = self.ccproject.get_project_photos(self.project_id)
        # Assert the results
        self.assertEqual(len(photos_dataFrame), 2)
        self.assertEqual(photos_dataFrame['id'][0], "1")
        self.assertEqual(photos_dataFrame['url'][0], "https://example.com/photo1.jpg")
        self.assertEqual(photos_dataFrame['date'][0], "2022-01-01")
        self.assertEqual(photos_dataFrame['user'][0], "John Doe")
        self.assertEqual(photos_dataFrame['lat'][0], 123)
        self.assertEqual(photos_dataFrame['lon'][0], 456)

    @patch('requests.get')
    def test_get_project_photos_failure(self, mock_get):
        # Mock the API response with an error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Invalid project ID")
        # Call the method
        photos_dataFrame = self.ccproject.get_project_photos(self.project_id)
        # Assert the results
        self.assertIsNone(photos_dataFrame)

if __name__ == "__main__":
    unittest.main()