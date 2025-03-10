import nfc

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())
    
    # Wenn Tag NDEF-kompatibel ist, NDEF auslesen
    if tag.ndef:
        # Alle Records durchgehen
        for record in tag.ndef.records:
            # Prüfen, ob es sich um einen Text-Record handelt
            if record.type == "urn:nfc:wkt:T":
                print("Text:", record.text)
    else:
        print("Keine NDEF-Daten gefunden oder Tag ist nicht NDEF-kompatibel.")

    # True zurückgeben, damit bei Bedarf mehrere Tags gelesen werden können
    return True

def main():
    # ACHTUNG: device_path anpassen, falls der UART anders heißt oder du /dev/ttyAMA0 /dev/serial0 nutzt
    device_path = 'pn532_uart:/dev/ttyS0'
    try:
        # Versuchen, den Reader über pn532_uart zu öffnen
        clf = nfc.ContactlessFrontend(device_path)
    except Exception as e:
        print("Konnte NFC-Leser nicht öffnen:", e)
        return
    
    print(f"Warte auf NFC-Tag über {device_path} ...")
    try:
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == "__main__":
    main()
