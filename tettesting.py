# -*- coding: utf-8 -*-

import nfc

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())

    # Prüfen, ob das Tag NDEF-kompatibel ist
    if tag.ndef is not None:
        print("Tag ist NDEF-kompatibel.")
        
        # Prüfen, ob es beschreibbar ist
        if tag.ndef.is_writeable:
            print("Tag ist beschreibbar.")
        else:
            print("Tag ist schreibgeschützt.")

        # (Optional) NDEF-Daten auslesen
        if tag.ndef.records:
            print("Gefundene NDEF-Records:")
            for record in tag.ndef.records:
                print(" -", record)
        else:
            print("Keine Records auf dem Tag.")
    else:
        print("Tag ist nicht NDEF-kompatibel oder nicht formatiert.")

    return True  # Verbindung beibehalten

def main():
    # Passe den Gerätenamen an, z. B. 'pn532_uart:/dev/ttyS0' bei PN532-UART-Modulen
    device_path = 'tty:S0'

    try:
        clf = nfc.ContactlessFrontend(device_path)
    except Exception as e:
        print("Konnte NFC-Leser nicht öffnen:", e)
        return

    print("Warte auf NFC-Tag...")
    try:
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == '__main__':
    main()
