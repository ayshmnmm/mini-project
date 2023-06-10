import tkinter
from pages import settings, menu
import os


class Page:
    def __init__(self, parent, cwd):
        self.parent = parent
        self.page = tkinter.Frame(self.parent, height=settings.HEIGHT, width=settings.WIDTH, background='white')
        self.cwd = cwd
        self.page.pack(expand=True, fill='both')
        self.top_bar = tkinter.Frame(self.page, background='white')
        self.top_bar.pack(expand=False, fill='x', side='top')
        self.render()

    def render(self):
        self.back_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/back.png'))
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/quiz.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self)


    def close(self):
        print("close")
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref):
        self.xo_board = [[' ','X','O'],[' ',' ',' '],[' ',' ',' ']]
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.turn = 1
        self.area = tkinter.Frame(self.parent, background='green')
        self.area.pack(expand=True, fill='x', padx=150, pady=75)
        self.area.rowconfigure(0,weight=1)
        self.area.rowconfigure(1,weight=1)
        self.area.rowconfigure(2,weight=1)
        self.area.rowconfigure(3,weight=1)
        self.area.columnconfigure(0,weight=1)

        self.ref.ximg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/X.png'))
        self.ref.oimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/O.png'))
        self.ref.bimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/blank.png'))
        self.display()

    def display(self):
        for i in range(4):
            tkinter.Button(self.area, text="replace soon").grid(row=i, column=0, sticky='ew')


