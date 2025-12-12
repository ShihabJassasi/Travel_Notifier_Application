import sqlite3

con = sqlite3.connect('travel_notifier.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS timeline(duration_minutes REAL, distance_km REAL)")

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='timeline'")
print("Table found:", cur.fetchone())  


def insert(duration_minutes: float, distance_km: float):
    cur.execute("INSERT INTO timeline(duration_minutes, distance_km) VALUES (?,?)",
                (duration_minutes, distance_km))
    con.commit()