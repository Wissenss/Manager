import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

class Database():
    def __init__(self):
        self.connection = sql.connect('test_database.db')
        self.cursor = self.connection.cursor()

        self.make_table()

    def make_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS test_table (
            id integer PRIMARY KEY,
            name text);""")
        self.connection.commit()

    def add_record(self, id, task):
        self.cursor.execute("INSERT INTO test_table VALUES(?,?)", (id, task))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

class App():
    def __init__(self):
        #database
        self.database = Database()

        root.title('Test Window')
        root.geometry('500x500')

        myEntry = tk.Entry(root)
        myEntry.place(x=100, y=20, width=300, height=20)
        self.myEntry = myEntry

        myButton = tk.Button(root, text='click me!', command=self.button_command)
        myButton.place(x=200, y=60, width=100, height=20)

        columns = ('name')
        myTreeView = ttk.Treeview(root, columns=columns, show='')
        myTreeView.column('#0', width=300)
        myTreeView.column('name', width=300)
        myTreeView.place(x=100, y=100)
        self.myTreeView = myTreeView

        self.entry_id = 0

    def button_command(self):
        entryText = self.myEntry.get()
        self.myTreeView.insert('', tk.END, iid=self.entry_id, values=entryText.replace(' ', '\ '))
        self.database.add_record(self.entry_id, entryText)
        self.entry_id += 1 
        print(entryText)

App()

root.mainloop()