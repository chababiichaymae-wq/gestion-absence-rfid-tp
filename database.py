import sqlite3

conn = sqlite3.connect("smarttp.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Admin par défaut
c.execute("INSERT OR IGNORE INTO admins (username,password) VALUES (?,?)",
          ("admin", "admin123"))

conn.commit()
conn.close()

print("Base de données créée + admin ajouté")
