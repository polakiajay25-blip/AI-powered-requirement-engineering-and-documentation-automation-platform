import sqlite3

conn = sqlite3.connect("projects.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM projects")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()