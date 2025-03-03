# Zebra Print Proxy

A lightweight HTTP-to-USB proxy for sending raw ZPL commands to Zebra printers.

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   And install libusb using OS package manager. 
   
   For Windows you can try using the included install.bat. Might need to mess around to get libusb proper setup on windows.
   
2. Run the proxy:
   ```sh
   python main.py
   ```

## API Endpoints

- `GET /printers` - List available USB Zebra printers
- `GET /printers/default` - Get the default printer
- `POST /printers/default` - Set the default printer
- `POST /print` - Send raw ZPL to the printer
- `GET /status` - Check printer status

## Notes
- Uses `libusb` via `pyusb` to bypass OS print spoolers.
- Default printer is persisted in `config.json`.
- For Windows there is an install bat file which attempts to install libusb using vcpkg. I also include the libusb binary. I am not sure which one is the one being used. But in any case, I had to include the following in main to make it work:
import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]
