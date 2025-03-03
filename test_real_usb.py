import usb_handler

TEST_ZPL = "^XA^FO50,50^A0N50,50^FDTest Print^FS^XZ"

printers = usb_handler.get_printers()
if not printers:
    print("No printers found!")
else:
    printer_id = printers[0]["id"]
    print(f"Found printer: {printer_id}, sending test print...")
    result = usb_handler.send_zpl(printer_id, TEST_ZPL)
    print("Print result:", result)
