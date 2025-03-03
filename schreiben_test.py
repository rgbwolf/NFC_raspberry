import serial
import time

# Konfiguration der seriellen Verbindung
SERIAL_PORT = '/dev/ttyS0'  # Ersetze dies mit dem richtigen Port
BAUD_RATE = 115200

def write_nfc_tag(data):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print("Warte auf NFC-Tag zum Schreiben...")
        while True:
            # Sende den Befehl zum Warten auf ein NFC-Tag
            ser.write(b'\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00')  # Beispielbefehl, anpassen je nach Protokoll
            time.sleep(0.5)  # Warte auf Antwort

            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting)
                print("Tag gefunden:", response.hex())

                # Sende den Befehl zum Schreiben auf das Tag
                write_command = b'\xFF\x00\x00\x00' + data.encode()  # Beispielbefehl, anpassen je nach Protokoll
                ser.write(write_command)
                print("Daten geschrieben:", data)
                break

if __name__ == "__main__":
    data_to_write = "Hallo, NFC!"  # Der Text, den du schreiben möchtest
    write_nfc_tag(data_to_write)
