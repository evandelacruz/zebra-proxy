import unittest
from main import app
import json
from unittest.mock import patch

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("usb_handler.get_printers", return_value=[{"id": "usb-0A5F-1234-1-3"}])
    def test_get_printers(self, mock_get_printers):
        """Test that /printers API correctly lists available printers"""
        response = self.client.get("/printers")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], "usb-0A5F-1234-1-3")

    @patch("usb_handler.send_zpl", return_value=True)
    def test_print_success(self, mock_send_zpl):
        """Test that /print sends a valid ZPL command"""
        response = self.client.post("/print", json={"zpl": "^XA^FO50,50^FDTest^FS^XZ"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "sent")

    @patch("usb_handler.send_zpl", return_value=False)
    def test_print_failure(self, mock_send_zpl):
        """Test that /print handles print failures correctly"""
        response = self.client.post("/print", json={"zpl": "^XA^FO50,50^FDTest^FS^XZ"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["status"], "failed")

if __name__ == "__main__":
    unittest.main()
