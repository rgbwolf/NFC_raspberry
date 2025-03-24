import nfc
import sqlite3

def on_connect(tag):
    print("Tag gefunden!")
    print("Tag-ID:", tag.identifier.hex())
    
    chip_id = tag.identifier.hex()
    
    # Überprüfen, ob der Benutzer genug Geld hat
    if check_balance(chip_id):
        print("Sie haben genug Geld, um einen Kauf zu tätigen.")
        # Hier kannst du den Kaufprozess implementieren
        # Zum Beispiel: purchase_item(chip_id, amount)
    else:
        print("Nicht genug Geld auf dem Konto.")
    
    return True  # Verbindung beibehalten

def check_balance(chip_id):
    conn = sqlite3.connect('kasse.db')  # Verbindung zur Datenbank 'kasse'
    cursor = conn.cursor()
    
    cursor.execute("SELECT kontostand FROM Geldbetrag WHERE chip_id = ?", (chip_id,))
    result = cursor.fetchone()
    
    if result:
        balance = result[0]
        print(f"Aktueller Kontostand: {balance}")
        return balance > 0  # Hier kannst du die Bedingung anpassen
    else:
        print("Chip-ID nicht gefunden.")
        return False
    
    conn.close()

def increase_balance(chip_id, amount):
    conn = sqlite3.connect('kasse.db')  # Verbindung zur Datenbank 'kasse'
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Geldbetrag SET kontostand = kontostand + ? WHERE chip_id = ?", (amount, chip_id))
    conn.commit()
    print(f"Kontostand für Chip-ID {chip_id} um {amount} erhöht.")
    
    conn.close()

def main():
    clf = nfc.ContactlessFrontend('tty:S0')  # Ersetze 'tty:S0' mit dem richtigen Port
    try:
        print("Warte auf NFC-Tag...")
        clf.connect(rdwr={'on-connect': on_connect})
    finally:
        clf.close()

if __name__ == "__main__":
    main()
