import os
import sys

# Get the directory of the script
app_dir = os.path.dirname(os.path.abspath(__file__))

# Add the DLL directory to PATH
os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]

import usb.backend.libusb1
backend = usb.backend.libusb1.get_backend()

print("Backend found:", backend is not None)
