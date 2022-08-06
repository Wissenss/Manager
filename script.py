#built-in imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#local/relative imports
import database
import styled_button
import settings_menu

class App():
    def __init__(self):
        #create window
        root = tk.Tk()
        self.window = root

        #connecting to database
        self.database = database.Database()

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

        ##managment buttons
        #add button
        add_button = styled_button.StyledButton(root, text='Add', command=self.add_task_button)
        add_button.place(x=340, y=20, width=140, height=20)

        #remove button
        add_button = styled_button.StyledButton(root, text='Remove', command=self.remove_task_button)
        add_button.place(x=340, y=60, width=140, height=20)

        #clear button
        clear_button = styled_button.StyledButton(root, text='Clear', command=self.clear_task)
        clear_button.place(x=340, y=100, width=140, height=20)

        ##status buttons
        #completed button
        kwargs = {
        'text': 'Completed', 
        'command': lambda:self.status_button('completed'),
        'bg': '#68a832'}
        completed_button = styled_button.StyledButton(root, **kwargs)
        completed_button.place(x=340, y=140, width=140, height=20)

        #in progress button
        kwargs = {
        'text': 'In Progress', 
        'command': lambda:self.status_button('inProgress'),
        'bg': '#ffff45'}
        completed_button = styled_button.StyledButton(root, **kwargs)
        completed_button.place(x=340, y=180, width=140, height=20)

        #pending button
        kwargs = {
        'text': 'Pending', 
        'command': lambda:self.status_button('pending'),
        'bg': 'white'}
        completed_button = styled_button.StyledButton(root, **kwargs)
        completed_button.place(x=340, y=220, width=140, height=20)

        #list settings button
        kwargs = {
        'text': 'Settings', 
        'command': self.list_settings_button,
        'bg': 'white'}
        completed_button = styled_button.StyledButton(root, **kwargs)
        completed_button.place(x=340, y=260, width=140, height=20)

        #recode this when u have the time, it aint too elegant
        self.tasks_list = self.database.get_tables()
        self.current_task_list = tk.StringVar(root)
        self.current_task_list.set(self.tasks_list[0][0])

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

        self.task_tree.place(x=20, y=60)

        #status tags
        self.task_tree.tag_configure('completed', background='#68a832')
        self.task_tree.tag_configure('inProgress', background='#ffff45')
        self.task_tree.tag_configure('pending', background='white')

        #load saved tasks from database
        self.task_id = 0
        self.load_tasks(self.current_task_list.get())

        root.mainloop()

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

    def list_settings_button(self):
        menu = settings_menu.SettingsMenu(self)

App()