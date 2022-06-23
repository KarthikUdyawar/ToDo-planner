import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS planer (id INTEGER PRIMARY KEY, data TEXT, status INTEGER)")
        self.conn.commit()

    def insert(self, data, status=0):
        self.cur.execute("INSERT INTO planer VALUES (NULL, ?, ?)", (data, status))
        self.conn.commit()

    def view_todo(self):
        self.cur.execute("SELECT id, data FROM planer WHERE status = 0")
        return self.cur.fetchall()

    def view_doing(self):
        self.cur.execute("SELECT id, data FROM planer WHERE status = 1")
        return self.cur.fetchall()

    def view_done(self):
        self.cur.execute("SELECT id, data FROM planer WHERE status = 2")
        return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute("DELETE FROM planer WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, data):
        self.cur.execute("UPDATE planer SET data=? WHERE id=?", (data, id))
        self.conn.commit()

    def push_to_doing(self, id):
        self.cur.execute("UPDATE planer SET status=1 WHERE id=?", (id,))
        self.conn.commit()

    def push_to_done(self, id):
        self.cur.execute("UPDATE planer SET status=2 WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()