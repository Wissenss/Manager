#third party imports
import sqlite3

class Database():
    def __init__(self):
        #connect to database
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

        self.tasks_table()

    def tasks_table(self, name='tasks'):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
            id integer PRIMARY KEY,
            name text,
            status text);""")
        self.connection.commit()

    def add_record(self, id, task, status="pending"):
        self.cursor.execute("INSERT INTO tasks VALUES(?,?,?)", (id, task, status))
        self.connection.commit()

    def remove_record(self, id):
        self.cursor.execute(f"DELETE FROM tasks WHERE id={id}")
        self.connection.commit()

    def get_records(self, name="tasks"):
        self.cursor.execute(f"""SELECT id,name, status FROM {name}""")
        return self.cursor.fetchall()

    def get_tables(self):
        self.cursor.execute("""SELECT name from sqlite_master where type='table'""")
        return self.cursor.fetchall()

    def update_status(self, id, newstatus):
        self.cursor.execute("""UPDATE tasks SET status = ? WHERE id = ?""", (newstatus, id))
        self.connection.commit()

    def __delf__(self):
        #disconect from database
        self.connection.close()