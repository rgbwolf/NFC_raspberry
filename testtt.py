# -*- coding: utf-8 -*-

import nfc

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())
    if hasattr(tag, 'text'):
        print("Text:", tag.text)
    return True  # Verbindung beibehalten

def main():
    # WICHTIG: Passe den Gerätenamen an, z.B. 'pn532_uart:/dev/ttyS0' oder 'tty:S0'
    # je nachdem, wie dein NFC-Modul angebunden ist.
    clf = nfc.ContactlessFrontend('tty:S0')

    try:
        print("Warte auf NFC-Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == '__main__':
    main()
