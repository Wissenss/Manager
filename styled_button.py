import tkinter as tk

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