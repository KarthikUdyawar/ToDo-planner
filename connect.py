import sqlite3


class Database:
    def __init__(self, db: str) -> None:
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS planer (id INTEGER PRIMARY KEY, data TEXT, status INTEGER)"
        )
        self.conn.commit()

    def insert(self, data: str, status: int = 0) -> None:
        self.cur.execute("INSERT INTO planer VALUES (NULL, ?, ?)", (data, status))
        self.conn.commit()

    def view_todo(self) -> list:
        self.cur.execute("SELECT id, data FROM planer WHERE status = 0")
        return self.cur.fetchall()

    def view_doing(self) -> list:
        self.cur.execute("SELECT id, data FROM planer WHERE status = 1")
        return self.cur.fetchall()

    def view_done(self) -> list:
        self.cur.execute("SELECT id, data FROM planer WHERE status = 2")
        return self.cur.fetchall()

    def delete(self, id: str) -> None:
        self.cur.execute("DELETE FROM planer WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, data: str) -> None:
        self.cur.execute("UPDATE planer SET data=? WHERE id=?", (data, id))
        self.conn.commit()

    def push_to_doing(self, id: str) -> None:
        self.cur.execute("UPDATE planer SET status=1 WHERE id=?", (id,))
        self.conn.commit()

    def push_to_done(self, id: str) -> None:
        self.cur.execute("UPDATE planer SET status=2 WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self) -> None:
        self.conn.close()
