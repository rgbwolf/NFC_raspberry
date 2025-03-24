import sqlite3

def create_table():
    conn = sqlite3.connect('kasse.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Geldbetrag (
            chip_id TEXT PRIMARY KEY,
            kontostand REAL
        )
    ''')
    conn.commit()
    conn.close()
    
def insert_initial_data():
    conn = sqlite3.connect('kasse.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Geldbetrag (chip_id, kontostand) VALUES (?, ?)", ('01234567', 100.0))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    insert_initial_data()
