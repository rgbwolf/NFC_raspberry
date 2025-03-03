import board
import busio
from adafruit_pn532 import PN532_I2C

# I2C initialisieren
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c)

# PN532 initialisieren
pn532.SAM_configuration()

print("Warte auf ein NFC-Tag...")
while True:
    uid = pn532.read_passive_target()
    if uid is not None:
        print("Tag gefunden! UID:", [hex(i) for i in uid])
