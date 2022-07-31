import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
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

root = tk.Tk()

class App():
    def __init__(self):
        #connecting to database
        self.database = Database()

        #window setup
        root.title('Manager')
        root.iconbitmap('icon.ico')
        root.geometry('500x380')

        #entry 
        input_style = {
            'relief' : 'solid',
            'bd' : 1
        }
        self.task_input = tk.Entry(root, **input_style)
        self.task_input.place(x=20, y=20, width = 300, height=20)

        #generic botton style
        class StyledButton(tk.Button):
            def __init__(self, *args, **kwargs):
                if not kwargs:
                    kwargs = dict()
                kwargs['relief'] = 'solid'
                #if not 'activebackground' in kwargs:
                kwargs['activebackground'] = '#202A44'
                kwargs['activeforeground'] = 'white'
                kwargs['bd'] = 1
                super().__init__(*args, **kwargs)

        ##managment buttons
        #add button
        add_button = StyledButton(root, text='Add', command=self.add_task_button)
        add_button.place(x=340, y=20, width=140, height=20)

        #remove button
        add_button = StyledButton(root, text='Remove', command=self.remove_task_button)
        add_button.place(x=340, y=60, width=140, height=20)

        #clear button
        clear_button = StyledButton(root, text='Clear', command=self.clear_task)
        clear_button.place(x=340, y=100, width=140, height=20)

        ##status buttons
        #completed button
        kwargs = {
        'text': 'Completed', 
        'command': lambda:self.status_button('completed'),
        'bg': '#68a832'}
        completed_button = StyledButton(root, **kwargs)
        completed_button.place(x=340, y=140, width=140, height=20)

        #in progress button
        kwargs = {
        'text': 'In Progress', 
        'command': lambda:self.status_button('inProgress'),
        'bg': '#ffff45'}
        completed_button = StyledButton(root, **kwargs)
        completed_button.place(x=340, y=180, width=140, height=20)

        #pending button
        kwargs = {
        'text': 'Pending', 
        'command': lambda:self.status_button('pending'),
        'bg': 'white'}
        completed_button = StyledButton(root, **kwargs)
        completed_button.place(x=340, y=220, width=140, height=20)

        #task list selector
        self.tasks_list = self.database.get_tables()
        #['default', 'second tasks', 'third tasks']
        self.current_task_list = tk.StringVar(root)
        self.current_task_list.set(self.tasks_list[0][0])
        task_selector = tk.OptionMenu(root, self.current_task_list, *self.tasks_list)
        task_selector.place(x=20, y=60, width=300, height=20)

        #task list
        #configure Treeview
        style = ttk.Style()
        # style.configure('Treeview',
        # background='',
        # foreground='',
        # rowheight=25,
        # fieldbackground=)
        style.map('Treeview', background=[('selected', '#202A44')])

        #create treeview
        self.task_tree = ttk.Treeview(root)
        self.task_tree['columns'] = ('Task')

        self.task_tree.column("#0", width=0, stretch=tk.NO)
        self.task_tree.column("Task", width=300)
        self.task_tree.heading("Task", text="Tasks")

        self.task_tree.place(x=20, y=80)

        #status tags
        self.task_tree.tag_configure('completed', background='#68a832')
        self.task_tree.tag_configure('inProgress', background='#ffff45')
        self.task_tree.tag_configure('pending', background='white')

        #load saved tasks from database
        self.task_id = 0
        self.load_tasks(self.current_task_list.get())

    #managment methods
    def load_tasks(self, name):
        self.clear_task()
        tasks = self.database.get_records(name)
        if tasks:
            self.task_id = tasks[-1][0]+1
            for task in tasks:
                self.add_task(task[1], task[0], task[2])

    def add_task(self, task=None, id=None, status="pending"):
        #display task on widget
        formated_task = task.replace(' ', '\ ')
        self.task_tree.insert('', index='0', iid=id, text='',  values=formated_task, tags=status)  
    
    def remove_task(self, task):
        #remove tasks from widget
        self.database.remove_record(task)
        self.task_tree.delete(task)

    def clear_task(self):
        tasks = self.task_tree.get_children()
        for task in tasks:
            self.remove_task(task)
        self.task_id=0

    #style methods
    def change_tag(self, iid, tag):
        self.task_tree.item(iid, tags=tag)
        #update status in database
        self.database.update_status(iid, tag)

    #button methods/commands
    def status_button(self, tag):
        selected_tasks = self.task_tree.selection()
        for task in selected_tasks:
            self.change_tag(task, tag)

    def remove_task_button(self):
        #remove all selected tasks from widget
        selected_tasks = self.task_tree.selection()
        for task in selected_tasks:
            self.remove_task(task)

    def clear_task_button(self):
        if messagebox.askyesno(title='Delete all', message='are you sure?'):
            self.clear_task()

    def add_task_button(self):
        #update task counter
        self.task_id +=1
        id = self.task_id

        #get text from entry
        task = self.task_input.get()
            
        #return if entry is empty
        if task=='':
            return

        #display task on widget
        self.add_task(task, id)

        #save task on database
        self.database.add_record(id, task)
  
        #clear entry
        self.task_input.delete(0, 'end')

    #experiments
    def entered(self, key):
        if key.char =='\n':
            pass
        else:
            pass

class Select_list_menu():
    def __init__(self, main_window):
        #save root database
        self.database = main_window.database
        self.main_window = main_window

        #create menu window
        self.menu = tk.Toplevel(root)

        #config menu window
        self.menu.title('Load List')
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
        name = 'test new table'
        self.database.tasks_table(name)

    def changeName_button(self):
        pass

    def removeList_button(self):
        pass

    def __delf__(self):
        pass

main_window = App()
Select_list_menu(main_window)


root.mainloop()