# Zebra Print Proxy

A lightweight HTTP-to-USB proxy for sending raw ZPL commands to Zebra printers.

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
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
