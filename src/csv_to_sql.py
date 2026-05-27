import sqlite3
import csv
from utils import DATA_CSV

con = sqlite3.connect(DATA_CSV)

cur = con.cursor()

### Create Table ###
cur.execute("""CREATE TABLE IF NOT EXISTS members
                (id INT NOT NULL,
                name TEXT NOT NULL,
                guild_id INT NOT NULL,
                guild_name TEXT NOT NULL,
                is_friend INT NOT NULL,
                PRIMARY KEY (id, guild_id)
                )""")

### Feed Database ###
with open('data.csv', "r") as data_csv:
    dr = csv.reader(data_csv)
    db = ((i[0], i[1], i[4], i[3], i[2]) for i in dr)

    cur.executemany("INSERT INTO members (id, name, guild_id, guild_name, is_friend) VALUES (?, ?, ?, ?, ?)", db)

    con.commit()


### Query Database ###
cur.execute("SELECT name, id, COUNT(guild_id) FROM members GROUP BY id HAVING COUNT(guild_id) > 1 ORDER BY count(guild_id) DESC")
"""
SELECT name, id, COUNT(guild_id) FROM members GROUP BY id HAVING COUNT(guild_id) > 1 ORDER BY count(guild_id) DESC
"""

results = cur.fetchall()

for line in results:
    for i in line:
        print(i, end="")
    print()

cur.close()