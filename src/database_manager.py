from typing import Any
import sqlite3
import csv
import os

if __name__ == "__main__":
    from utils import DEFAULT_CSV_PATH, DEFAULT_DB_PATH, console
else:
    from .utils import DEFAULT_CSV_PATH, DEFAULT_DB_PATH, console  # ty:ignore[unresolved-import]

class DataBaseManager:
    csv_path = DEFAULT_CSV_PATH
    db_path = DEFAULT_DB_PATH
    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, csv_path=DEFAULT_CSV_PATH, db_path=DEFAULT_DB_PATH):
        self.csv_path = os.path.abspath(csv_path)
        self.db_path = os.path.abspath(db_path)
        self.connect_db()
        self.create_db()

    def __del__(self):
        try:
            self.cur.close()
        except Exception as err:
            console.error(err)

    def connect_db(self) -> None:
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

    def create_db(self) -> None:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS members
                        (id INT NOT NULL,
                        name TEXT NOT NULL,
                        guild_id INT NOT NULL,
                        guild_name TEXT NOT NULL,
                        is_friend INT NOT NULL,
                        PRIMARY KEY (id, guild_id)
                        )""")

    def feed_db(self) -> None:
        with open(self.csv_path, "r") as data_csv:
            dr = csv.reader(data_csv)
            db = ((i[0], i[1], i[4], i[3], i[2]) for i in dr)

            self.cur.executemany(
                "INSERT INTO members (id, name, guild_id, guild_name, is_friend) VALUES (?, ?, ?, ?, ?)",
                db,
            )

            self.con.commit()

    def query_db(self, query) -> list[Any]:
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_members(self, min_servers=2) -> list[Any]:
        query = f"SELECT name, id, COUNT(guild_id) FROM members GROUP BY id HAVING COUNT(guild_id) > {min_servers} ORDER BY count(guild_id) DESC"
        return self.query_db(query)


if __name__ == "__main__":
    db = DataBaseManager()
    results = db.get_members()

    for line in results:
        for i in line:
            print(i, end="")
        print()  # newline
