import tkinter
import os
from pages import settings
import pages


class Page:
    def __init__(self, parent, cwd):
        self.parent = parent
        self.menu = tkinter.Frame(self.parent, background='white')
        self.menu.pack(expand=True, fill='both')
        self.cwd = cwd
        self.top_bar = tkinter.Frame(self.menu, background='white')
        self.top_bar.pack(expand=False, fill='x', side='top')
        self.render()

    def render(self):
        self.launcher = tkinter.Frame(self.menu, background='white')
        self.launcher.pack(expand=True, fill='both', padx=75, pady=30)
        self.launcher.rowconfigure(0,weight=1)
        self.launcher.rowconfigure(1,weight=1)
        self.launcher.rowconfigure(2,weight=1)
        self.launcher.rowconfigure(3,weight=1)
        self.launcher.columnconfigure(0,weight=1)
        self.launcher.columnconfigure(1,weight=1)
        self.launcher.columnconfigure(2,weight=1)


        self.back_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/blank.png'))
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/replace_me.png'))
        # tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=lambda: self.parent.destroy()).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).pack(side='top', pady=10)


        self.xo_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/XO.png'))
        tkinter.Button(self.launcher, image=self.xo_btn, borderwidth=0, background='white', command=lambda: self.launch(pages.tic_tac_toe)).grid(row=0, column=0)

        self.quiz_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/bulb.png'))
        tkinter.Button(self.launcher, image=self.quiz_btn, borderwidth=0, background='white', command=lambda: self.launch(pages.quiz)).grid(row=0, column=1)

        self.passwd_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/lock.png'))
        tkinter.Button(self.launcher, image=self.passwd_btn, borderwidth=0, background='white', command=lambda: self.launch(pages.password_generator)).grid(row=0, column=2)

        self.sudoku_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/sudoku.png'))
        tkinter.Button(self.launcher, image=self.sudoku_btn, borderwidth=0, background='white', command=lambda: self.launch(pages.sudoku_solver)).grid(row=1, column=0)

        self.guess_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/18.png'))
        tkinter.Button(self.launcher, image=self.guess_btn, borderwidth=0, background='white',  command=lambda: self.launch(pages.number_guess)).grid(row=1, column=1)
        
        self.clock_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/clock.png'))
        tkinter.Button(self.launcher, image=self.clock_btn, borderwidth=0, background='white',  command=lambda: self.launch(pages.countdown_timer)).grid(row=1, column=2)

        self.hang_btn = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/hanged_man.png'))
        tkinter.Button(self.launcher, image=self.hang_btn, borderwidth=0, background='white',  command=lambda: self.launch(pages.hangman)).grid(row=2, column=0)

        self.footer_img = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/heart.png'))
        self.footer = tkinter.Label(self.launcher, image=self.footer_img, bd=0, borderwidth=0)
        self.footer.grid(row=3,column=0,columnspan=3, sticky='s')


    def close(self):
        self.page.destroy()

    def launch(self, what):
        self.menu.destroy()
        what.Page(self.parent, self.cwd)



