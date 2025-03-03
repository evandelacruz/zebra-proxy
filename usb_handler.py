import usb.core
import usb.util

ZEBRA_VENDOR_IDS = {0x0A5F, 0x05E0} # Known Zebra Vendor IDs

def get_printers():
    printers = []
    for dev in usb.core.find(find_all=True):
        try:
            vendor = dev.idVendor
            product = dev.idProduct
            bus = dev.bus
            address = dev.address
        except Exception:
            continue
        if vendor in ZEBRA_VENDOR_IDS:
            printers.append({
                "id": f"usb-{vendor}-{product}-{bus}-{address}",
                "vendor_id": hex(vendor),
                "product_id": hex(product)
            })
    return printers

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
