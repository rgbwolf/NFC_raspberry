# check_tag.py

import nfc

def on_connect(tag):
    # Ueberpruefen, ob das Tag NDEF-kompatibel ist
    if tag.ndef is not None:
        print("Tag ist NDEF-kompatibel.")
        # Ueberpruefen, ob das Tag beschreibbar ist
        if tag.ndef.is_writeable:
            print("Tag ist beschreibbar.")
        else:
            print("Tag ist schreibgeschuetzt.")
    else:
        print("Tag ist nicht NDEF-kompatibel oder nicht formatiert.")
    return True

def main():
    # Passe 'usb' ggf. an: 'tty:S0', 'COM3' usw. je nach System/Reader
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
