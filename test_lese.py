import time
import serial
from adafruit_pn532.pn532 import PN532

# Initialize serial connection
uart = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

# Create PN532 instance
pn532 = PN532(uart)

# Initialize the PN532
pn532.SAM_configuration()

print("Waiting for an NFC card...")

while True:
    # Check for an NFC card
    uid = pn532.read_passive_target()
    
    if uid is not None:
        print("Found an NFC card!")
        print("UID:", [hex(i) for i in uid])
        
        # Write data to the NFC tag
        try:
            # The data you want to write
            data_to_write = "Hello, NFC!"
            print("Writing data to the NFC tag...")
            pn532.ntag2xx_WriteNDEF(data_to_write.encode('utf-8'))
            print("Data written successfully!")
        except Exception as e:
            print("Error writing to NFC tag:", e)
        
        time.sleep(1)  # Wait a bit before looking for another card
