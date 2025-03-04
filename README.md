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
	 or
   ```sh
   ./start.bat
   ```

## API Endpoints

- `GET /printers` - List available USB Zebra printers
- `GET /printers/default` - Get the default printer
- `POST /printers/default` - Set the default printer
- `POST /print` - Send raw ZPL to the printer
- `GET /status` - Check printer status

## Client Installation & Usage

To integrate with the Zebra Print Proxy from a web application, use the provided **`ZebraProxySdk`** JavaScript client.

### Include the SDK

Include the SDK in your project:

```html
<script src="zebra_proxy_sdk.js"></script>
```

Or, if using ES modules:

```js
import { ZebraProxySdk } from './zebra_proxy_sdk.js';
```

### Usage

#### Initialize the SDK
```js
const sdk = new ZebraProxySdk("http://127.0.0.1:5000");
```

#### List Available Printers
```js
sdk.listPrinters().then(console.log);
```

#### Get Default Printer
```js
sdk.getDefaultPrinter().then(console.log);
```

#### Set Default Printer
```js
sdk.setDefaultPrinter("usb-0xA5F-0x1234-1-3").then(console.log);
```

#### Print ZPL
```js
const zpl = "^XA^FO50,50^A0N50,50^FDHello World^FS^XZ";
sdk.printZPL(zpl).then(console.log);
```

#### Check Printer Status
```js
sdk.getStatus().then(console.log);
```


## Notes
- Uses `libusb` via `pyusb` to bypass OS print spoolers.
- Default printer is persisted in `config.json`.
- For Windows there is an install bat file which attempts to install libusb using vcpkg. I also include the libusb binary. I am not sure which one is the one being used. But in any case, I had to include the following in main to make it work:
import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]
