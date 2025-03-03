import nfc

def on_connect(tag):
    print("Tag gefunden!")
    # Schreibe Text auf das Tag
    text_to_write = "Hallo, NFC!"
    tag.ndef.records = [nfc.ndef.TextRecord(text_to_write)]
    print("Daten geschrieben:", text_to_write)
    return True  # Verbindung beibehalten

def main():
    clf = nfc.ContactlessFrontend('tty:S0')  # Ersetze 'tty:S0' mit dem richtigen Port
    try:
        print("Warte auf NFC-Tag zum Schreiben...")
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == "__main__":
    main()
