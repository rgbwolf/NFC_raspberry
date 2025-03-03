import serial
import time

# Konfiguration der seriellen Verbindung
SERIAL_PORT = '/dev/ttyS0'  # Ersetze dies mit dem richtigen Port
BAUD_RATE = 115200

def read_nfc_tag():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Warte auf NFC-Tag...")
        while True:
            # Sende den Befehl zum Lesen eines NFC-Tags
            ser.write(b'\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00')  # Beispielbefehl, anpassen je nach Protokoll
            time.sleep(0.5)  # Warte auf Antwort

            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print("Antwort vom Tag:", response.hex())
                break

if __name__ == "__main__":
    read_nfc_tag()
