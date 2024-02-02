import sqlite3


# Створює та зберігає дані, якщо БД пуста
def save_to_db():
    with sqlite3.connect('auto.db') as con:
        print("Opened database successfully")
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS cars( 
        id INTEGER PRIMARY KEY,
        title TEXT, 
        price INTEGER, 
        url TEXT,
        image1 BLOB, 
        image2 BLOB, 
        image3 BLOB 
        )''')

        print("Close database successfully")
