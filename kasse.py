import nfc
import sqlite3

def on_connect(tag):
    chip_id = tag.identifier.hex()
    
    while True:
        print(f"\nTag gefunden! Chip-ID: {chip_id}")
        print("Wählen Sie eine Option:")
        print("1. Kontostand überprüfen")
        print("2. Betrag einzahlen")
        print("3. Artikel kaufen")
        print("4. Beenden")
        
        choice = input("Geben Sie Ihre Wahl ein (1-4): ")
        
        if choice == '1':
            check_balance(chip_id)
        elif choice == '2':
            amount = float(input("Geben Sie den Betrag zum Einzahlen ein: "))
            deposit_amount(chip_id, amount)
        elif choice == '3':
            amount = float(input("Geben Sie den Betrag für den Kauf ein: "))
            purchase_item(chip_id, amount)
        elif choice == '4':
            print("Programm wird beendet.")
            return False  # Beende die Schleife und die Verbindung
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        
        # Nach jeder Auswahl wird die NFC-Abfrage erneut durchgeführt
        return True  # Behalte die Verbindung, um den NFC-Tag erneut zu lesen

def check_balance(chip_id):
    conn = sqlite3.connect('kasse.db')  # Verbindung zur Datenbank 'kasse'
    cursor = conn.cursor()
    
    cursor.execute("SELECT kontostand FROM Geldbetrag WHERE chip_id = ?", (chip_id,))
    result = cursor.fetchone()
    
    if result:
        balance = result[0]
        print(f"Aktueller Kontostand: {balance}")
    else:
        print("Chip-ID nicht gefunden.")
    
    conn.close()

def increase_balance(chip_id, amount):
    conn = sqlite3.connect('kasse.db')  # Verbindung zur Datenbank 'kasse'
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Geldbetrag SET kontostand = kontostand + ? WHERE chip_id = ?", (amount, chip_id))
    conn.commit()
    print(f"Kontostand für Chip-ID {chip_id} um {amount} erhöht.")
    
    conn.close()

def deposit_amount(chip_id, amount):
    if amount <= 0:
        print("Der Betrag muss positiv sein.")
        return
    
    increase_balance(chip_id, amount)

def purchase_item(chip_id, amount):
    conn = sqlite3.connect('kasse.db')  # Verbindung zur Datenbank 'kasse'
    cursor = conn.cursor()
    
    # Überprüfen, ob der Benutzer genug Geld hat
    cursor.execute("SELECT kontostand FROM Geldbetrag WHERE chip_id = ?", (chip_id,))
    result = cursor.fetchone()
    
    if result:
        balance = result[0]
        if balance >= amount:
            # Betrag abziehen
            cursor.execute("UPDATE Geldbetrag SET kontostand = kontostand - ? WHERE chip_id = ?", (amount, chip_id))
            conn.commit()
            print(f"Kauf erfolgreich! {amount} wurde abgezogen. Neuer Kontostand: {balance - amount}")
        else:
            print("Nicht genug Geld für diesen Kauf.")
    else:
        print("Chip-ID nicht gefunden.")
    
    conn.close()

def main():
    clf = nfc.ContactlessFrontend('tty:S0')  # Ersetze 'tty:S0' mit dem richtigen Port
    try:
        while True:
            print("Warte auf NFC-Tag...")
            tag = clf.connect(rdwr={'on-connect': on_connect})
            if not tag:
                print("Kein Tag gefunden. Versuche es erneut.")
    finally:
        clf.close()

if __name__ == "__main__":
    main()
