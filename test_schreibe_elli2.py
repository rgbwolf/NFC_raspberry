import nfc

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())
    
    # Lese den Text, falls vorhanden
    try:
        if isinstance(tag.ndef, nfc.ndef.Record):
            print("Text auf dem Tag:", tag.ndef.text)
    except AttributeError:
        print("Kein lesbarer Text gefunden.")
    
    # Schreibe neuen Text auf das Tag
    new_text = input("Gib den Text ein, den du auf das Tag schreiben möchtest: ")
    if tag.ndef is not None and tag.ndef.is_writeable:
        try:
            new_record = nfc.ndef.TextRecord(new_text)
            tag.ndef.records = [new_record]
            print("Text erfolgreich auf das Tag geschrieben!")
        except Exception as e:
            print("Fehler beim Schreiben auf das Tag:", e)
    else:
        print("Das Tag unterstützt das Schreiben nicht oder ist schreibgeschützt.")
    
    return True  # Verbindung beibehalten

def main():
    clf = nfc.ContactlessFrontend('tty:S0')  # Ersetze 'tty:S0' mit dem richtigen Port
    try:
        print("Warte auf NFC-Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == "__main__":
    main()
