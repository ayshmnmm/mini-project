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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/tic_tac_toe.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self)


    def close(self):
        print("close")
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref):
        self.xo_board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.turn = 1
        self.body = tkinter.Frame(self.parent, background='white')
        self.body.pack(expand=True, fill='both')
        self.body.rowconfigure(0, weight=1)
        self.body.rowconfigure(1, weight=2)
        self.body.rowconfigure(2, weight=1)
        self.body.columnconfigure(0, weight=1)
        self.body.columnconfigure(1, weight=2)
        self.body.columnconfigure(2, weight=1)

        self.area = tkinter.Frame(self.body, background='brown')
        self.area.grid(row=0, column=1, rowspan=2, pady=100, sticky='n')
        self.area.rowconfigure(0,weight=1)
        self.area.rowconfigure(1,weight=1)
        self.area.rowconfigure(2,weight=1)
        self.area.columnconfigure(0,weight=1)
        self.area.columnconfigure(1,weight=1)
        self.area.columnconfigure(2,weight=1)

        self.next_play = tkinter.Label(self.body, text="to play : X", background='white')
        self.next_play.grid(row=2,column=1, pady=10)
        # self.next_play.grid(row=0,column=1, sticky='news')

        self.ref.ximg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/X.png'))
        self.ref.oimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/O.png'))
        self.ref.bimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/blank.png'))
        self.display()

    def display(self):
        for i in range(3):
            for j in range(3):
                cell = self.xo_board[i][j]
                tkinter.Button(self.area, text='e', image=self.ref.ximg if cell=='X' else self.ref.oimg if cell=='O' else self.ref.bimg , borderwidth=0, command=lambda a=i,b=j:self.click(a,b)).grid(row=i, column=j, sticky='news')

    def click(self, i, j):
        if self.xo_board[i][j] != ' ' :
            return
        self.xo_board[i][j] = 'X' if self.turn%2 else 'O'
        self.next_play.configure(text=f"to play : {'O' if self.turn%2 else 'X'}")
        self.turn += 1
        self.display()


