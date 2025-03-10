import nfc
import nfc.ndef

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())

    # Überprüfe, ob das Tag NDEF unterstützt
    if tag.ndef is None:
        print("Das Tag unterstützt kein NDEF-Format oder muss formatiert werden.")
        return True  # Verbindung beibehalten, aber keine Schreibaktion

    # Falls das Tag nicht schreibgeschützt ist, fortfahren
    if tag.ndef.is_writeable:
        new_text = input("Gib den Text ein, den du auf das Tag schreiben möchtest: ")
        try:
            new_record = nfc.ndef.TextRecord(new_text)
            tag.ndef.records = [new_record]
            print("Text erfolgreich auf das Tag geschrieben!")
        except Exception as e:
            print("Fehler beim Schreiben auf das Tag:", e)
    else:
        print("Das Tag ist schreibgeschützt und kann nicht beschrieben werden.")

    return True  # Verbindung beibehalten

def main():
    clf = nfc.ContactlessFrontend('usb')  # Port anpassen, falls notwendig
    try:
        print("Warte auf NFC-Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == "__main__":
    main()
