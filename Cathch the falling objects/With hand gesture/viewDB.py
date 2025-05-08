import sqlite3
conn = sqlite3.connect('game_scores.db')
cursor = conn.cursor()

# View all records
cursor.execute("SELECT * FROM high_score")
print(cursor.fetchall())

conn.close()