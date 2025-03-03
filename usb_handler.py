import os
import sys
app_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = app_dir + os.pathsep + os.environ["PATH"]

import usb.core
import usb.util

ZEBRA_VENDOR_IDS = {0x0A5F, 0x05E0} # Known Zebra Vendor IDs

def get_printers():
    printers = []
    try:
        for dev in usb.core.find(find_all=True):
            try:
                vendor = dev.idVendor
                product = dev.idProduct
                bus = dev.bus
                address = dev.address
            except AttributeError:
                continue  # Skip devices missing attributes

            if vendor in ZEBRA_VENDOR_IDS:
                printers.append({
                    "id": f"usb-{vendor}-{product}-{bus}-{address}",
                    "vendor_id": hex(vendor),
                    "product_id": hex(product)
                })
        return printers

    except usb.core.USBError as e:
        return {"error": f"USB communication error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_status(printer_id):
    for dev in usb.core.find(find_all=True):
        if printer_id == f"usb-{dev.idVendor}-{dev.idProduct}-{dev.bus}-{dev.address}":
            return {"connected": True, "status": "ready"}
    return {"connected": False, "status": "disconnected"}

def send_zpl(printer_id, zpl):
    for dev in usb.core.find(find_all=True):
        if printer_id == f"usb-{dev.idVendor}-{dev.idProduct}-{dev.bus}-{dev.address}":
            try:
                dev.set_configuration()
                endpoint = dev[0][(0,0)][0]  # Get first endpoint
                dev.write(endpoint.bEndpointAddress, zpl.encode("utf-8"))
                return True
            except usb.core.USBError as e:
                return {"error": f"USB communication failed: {e}"}
            except Exception as e:
                return {"error": f"Unexpected error: {e}"}
    return {"error": "Printer not found"}
