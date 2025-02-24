#!/usr/bin/env python3

from pn532pi import Pn532Spi
from pn532pi import Pn532
import ndef

# SPI-Konfiguration
pn532 = Pn532Spi(spi_dev="/dev/spidev0.0")
pn532.begin()
pn532.SAM_configuration()

print("PN532 Version:", pn532.get_firmware_version())

try:
    print("Halte NFC-Tag an den Reader...")
    while True:
        uid = pn532.read_passive_target()
        if not uid:
            continue
        
        print(f"\nTag UID: {[hex(x) for x in uid]}")

        # NDEF-Nachricht erstellen
        records = [
            ndef.TextRecord("Hello Ubuntu on Pi!"),
            ndef.UriRecord("https://ubuntu.com")
        ]
        
        # Nachricht schreiben
        if pn532.ntag2xx_write_ndef(records):
            print("Erfolgreich geschrieben!")
        else:
            print("Fehler beim Schreiben!")
        
        break

except Exception as e:
    print("Fehler:", str(e))
finally:
    pn532.close()
