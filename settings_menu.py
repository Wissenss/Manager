import tkinter as tk

class SettingsMenu():
    def __init__(self, main_window):
        #save root database
        self.database = main_window.database
        self.main_window = main_window

        #create menu window
        self.menu = tk.Toplevel(main_window.window)

        #config menu window
        self.menu.title('Load List')
        self.menu.iconbitmap('icon.ico')
        self.menu.geometry("250x300")

        #dropdown tasks list
        self.selected_list = tk.StringVar()
        self.selected_list.set(main_window.current_task_list.get())
        self.list = tk.OptionMenu(self.menu, self.selected_list, self.database.get_tables())
        self.list.place(x=20, y=20, height=20, width=210)

        #load button
        load_button = tk.Button(self.menu, text="Load", command=self.load_button)
        load_button.place(x=20, y=60, height=20, width=210)

        #change name button
        changeName_button = tk.Button(self.menu, text="Change Name", command=self.changeName_button)
        changeName_button.place(x=20, y=100, height=20, width=210)

        #create new list button
        newList_button = tk.Button(self.menu, text="Create New", command=self.addList_button)
        newList_button.place(x=20, y=140, height=20, width=210)

        #remove list button
        removeList_button = tk.Button(self.menu, text="Delete Current", command=self.removeList_button)
        removeList_button.place(x=20, y=180, height=20, width=210)

    def load_button(self):
        self.main_windowk.load_tasks(self.selected_list.get())
        self.delf()

    def addList_button(self):
        name = 'test_new_table'
        self.database.tasks_table(name)
        self.selected_list.set(name)

    def changeName_button(self):
        pass

    def removeList_button(self):
        pass

    def __delf__(self):
        pass

"""
#task list selector
        self.tasks_list = self.database.get_tables()
        #['default', 'second tasks', 'third tasks']
        self.current_task_list = tk.StringVar(root)
        self.current_task_list.set(self.tasks_list[0][0])
        task_selector = tk.OptionMenu(root, self.current_task_list, *self.tasks_list)
        task_selector.place(x=20, y=60, width=300, height=20)
"""