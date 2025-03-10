import nfc

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())
    
    # Lese den Text, falls vorhanden
    if hasattr(tag, 'text'):
        print("Text:", tag.text)
    
    # Schreibe neuen Text auf das Tag
    new_text = input("Gib den Text ein, den du auf das Tag schreiben möchtest: ")
    if hasattr(tag, 'write'):
        try:
            tag.write(new_text)
            print("Text erfolgreich auf das Tag geschrieben!")
        except Exception as e:
            print("Fehler beim Schreiben auf das Tag:", e)
    else:
        print("Das Tag unterstützt das Schreiben nicht.")
    
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
