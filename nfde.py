import nfc

def on_connect(tag):
    # Prüfen, ob das Tag NDEF-kompatibel ist
    if tag.ndef is not None:
        print("Tag ist NDEF-kompatibel.")
        # Prüfen, ob das Tag beschreibbar ist
        if tag.ndef.is_writeable:
            print("Tag ist beschreibbar.")
        else:
            print("Tag ist schreibgeschützt.")
    else:
        print("Tag ist nicht NDEF-kompatibel oder nicht formatiert.")
    # True zurückgeben, damit die Verbindung (rdwr) offen bleibt
    return True

def main():
    # 'usb' ggf. anpassen, z.B. 'tty:S0' oder 'COM3', je nach System und Reader
    try:
        clf = nfc.ContactlessFrontend('usb')
        print("Warte auf NFC-Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
    except Exception as e:
        print("Fehler bei der NFC-Verbindung:", e)
    finally:
        try:
            clf.close()
        except:
            pass

if __name__ == '__main__':
    main()
