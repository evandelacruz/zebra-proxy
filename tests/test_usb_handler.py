import unittest
from unittest.mock import patch, MagicMock
import usb_handler

# Mock USB device for testing
class MockUSBDevice:
    def __init__(self, vendor_id, product_id, bus, address):
        self.idVendor = vendor_id
        self.idProduct = product_id
        self.bus = bus
        self.address = address

    def set_configuration(self):
        pass

    def write(self, endpoint, data):
        pass

mock_device = MockUSBDevice(0x0A5F, 0x1234, 1, 3)

class TestUSBHandler(unittest.TestCase):

    @patch('usb.core.find')
    def test_get_printers(self, mock_find):
        """Test that get_printers correctly lists available Zebra printers"""
        mock_find.return_value = [mock_device]
        printers = usb_handler.get_printers()
        self.assertEqual(len(printers), 1)
        self.assertIn("id", printers[0])
        self.assertEqual(printers[0]["vendor_id"], "0xa5f")

    @patch('usb.core.find')
    def test_get_status_connected(self, mock_find):
        """Test that get_status correctly identifies a connected printer"""
        mock_find.return_value = [mock_device]
        printer_id = f"usb-{mock_device.idVendor}-{mock_device.idProduct}-{mock_device.bus}-{mock_device.address}"
        status = usb_handler.get_status(printer_id)
        self.assertTrue(status["connected"])
        self.assertEqual(status["status"], "ready")

    @patch('usb.core.find')
    def test_get_status_disconnected(self, mock_find):
        """Test that get_status correctly identifies a disconnected printer"""
        mock_find.return_value = []
        status = usb_handler.get_status("usb-unknown")
        self.assertFalse(status["connected"])
        self.assertEqual(status["status"], "disconnected")

    @patch('usb.core.find')
    def test_send_zpl_success(self, mock_find):
        """Test that send_zpl successfully writes data to a connected printer"""
        mock_find.return_value = [mock_device]
        printer_id = f"usb-{mock_device.idVendor}-{mock_device.idProduct}-{mock_device.bus}-{mock_device.address}"
        with patch.object(mock_device, "write", return_value=True) as mock_write:
            success = usb_handler.send_zpl(printer_id, "^XA^FO50,50^A0N50,50^FDTest^FS^XZ")
            self.assertTrue(success)
            mock_write.assert_called_once()

    @patch('usb.core.find')
    def test_send_zpl_failure(self, mock_find):
        """Test that send_zpl fails when the printer is disconnected"""
        mock_find.return_value = []
        success = usb_handler.send_zpl("usb-unknown", "^XA^FO50,50^A0N50,50^FDTest^FS^XZ")
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
