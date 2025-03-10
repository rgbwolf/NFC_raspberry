import nfc
import nfc.ndef

"""
Dieser Code demonstriert die grundlegenden Schritte:
1. NFC-Leser öffnen.
2. Auf Tag warten.
3. Tag erkennen.
4. (Optional) Tag formatieren, falls nicht NDEF-kompatibel.
5. Text von Tag lesen.
6. Text auf Tag schreiben.

Stelle sicher, dass du:
- nfcpy installiert hast (pip install nfcpy)
- pyserial (insbesondere unter Windows)
- den richtigen Port (z.B. 'usb' oder 'tty:S0') verwendest.

Falls dein Tag nicht NDEF-kompatibel ist oder bereits schreibgeschützt ist,
dann kann es nicht beschrieben werden.
"""

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())

    # Versuche, den NDEF-Bereich zu initialisieren
    try:
        if tag.ndef is None:
            print("Das Tag ist nicht NDEF-formatiert oder unterstützt kein NDEF.")

            # Versuche, das Tag zu formatieren (funktioniert nur bei manchen Typen, z.B. Type2Tag)
            if hasattr(tag, "format"):
                try:
                    dummy_record = nfc.ndef.TextRecord("Hello!")
                    dummy_message = nfc.ndef.Message(dummy_record)
                    tag.format(dummy_message)
                    print("Tag wurde erfolgreich formatiert.")
                except Exception as e:
                    print("Fehler beim Formatieren:", e)
                    return True
            else:
                print("Das Tag kann nicht formatiert werden.")
                return True

        # Nach einer erfolgreichen Formatierung sollte tag.ndef nun verfügbar sein.
        if tag.ndef is None:
            print("Tag unterstützt immer noch kein NDEF. Abbruch.")
            return True

        # Lese vorhandene NDEF-Daten
        if tag.ndef.records:
            print("Aktuelle NDEF-Daten:")
            for record in tag.ndef.records:
                # Prüfe, ob der Record ein TextRecord ist.
                if isinstance(record, nfc.ndef.TextRecord):
                    print(" - TextRecord: ", record.text)
                else:
                    print(" - Anderer Record: ", record)
        else:
            print("Keine vorhandenen Records auf dem Tag.")

        # Prüfe, ob das Tag beschreibbar ist
        if not tag.ndef.is_writeable:
            print("Das Tag ist schreibgeschützt und kann nicht beschrieben werden.")
            return True

        # Jetzt Text schreiben
        new_text = input("Gib den neuen Text ein, der auf dem Tag gespeichert werden soll: ")
        new_record = nfc.ndef.TextRecord(new_text)
        new_message = nfc.ndef.Message(new_record)
        try:
            tag.ndef.records = new_message
            print("Text wurde erfolgreich auf das Tag geschrieben!")
        except Exception as e:
            print("Fehler beim Schreiben der NDEF-Daten:", e)

    except Exception as err:
        print("Allgemeiner Fehler beim Zugriff auf das Tag:", err)

    # Gibt True zurück, damit die Verbindung aufrechterhalten bleibt
    # wenn das Gerät mehrere Tags hintereinander lesen soll.
    return True

def main():
    # Verwende hier den passenden Port (z.B. 'usb', 'tty:S0', 'com3', etc.)
    READER_PORT = 'usb'  # Anpassen!

    print(f"Versuche, NFC-Leser über {READER_PORT} zu öffnen...")
    try:
        clf = nfc.ContactlessFrontend(READER_PORT)
    except Exception as e:
        print("Konnte NFC-Leser nicht öffnen:", e)
        return

    try:
        print("NFC-Leser geöffnet. Warte auf NFC-Tag...")
        clf.connect(rdwr={
            'on-connect': on_connect,
            'beep-on-connect': True  # Falls dein Leser das unterstützt
        })
    except Exception as e:
        print("Fehler bei der NFC-Verbindung:", e)
    finally:
        print("Beende NFC-Sitzung.")
        clf.close()

if __name__ == "__main__":
    main()
