import win32print
import win32con

exclude_printers = ['OneNote for Windows 10', 'OneNote (Desktop)', 'Microsoft XPS Document Writer',
                    'Microsoft Print to PDF', 'Fax', 'Adobe PDF']

# to add a printer use this cmd:
# RUNDLL32 PRINTUI.DLL,PrintUIEntry /if /b "PrinterName" /f %windir%\inf\ntprint.inf /r "192.168.1.142" /m "Generic / Text Only"

def get_printer_info():
    printer_info = []

    try:
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers = win32print.EnumPrinters(flags, None, 4)

        for printer in printers:
            printer_name = printer.get('pPrinterName')
            if printer_name in exclude_printers:
                continue
            print_handler = win32print.OpenPrinter(printer_name)
            properties = win32print.GetPrinter(print_handler, 2)
            port_name = properties['pPortName']
            driver_name = properties['pDriverName']

            ip_address = None
            for prop in port_name.split(","):
                if prop.strip().startswith("IP_"):
                    ip_address = prop.strip()
                    break

            printer_info.append({
                'Printer Name': printer_name,
                'Port Name': port_name,
                'Driver Name': driver_name
            })

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return printer_info

if __name__ == "__main__":
    printers = get_printer_info()

    if printers:
        with open("printer_info.txt", "w") as file:
            for idx, printer in enumerate(printers, start=1):
                file.write(f"Printer {idx}:\n")
                file.write(f"  Printer Name: {printer['Printer Name']}\n")
                file.write(f"  Port Name: {printer['Port Name']}\n")
                file.write(f"  Driver Name: {printer['Driver Name']}\n\n")
        print("Printer information saved to 'printer_info.txt'.")
    else:
        print("No printers found.")
