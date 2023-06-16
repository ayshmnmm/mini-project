import tkinter
from pages import settings, menu
import os
import random


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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/number_guessing.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self)


    def close(self):
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref):
        self.questions = settings.QUIZ_QUESTIONS.copy()
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.bottom_area = tkinter.Frame(self.parent, background='white')
        self.bottom_area.pack(expand=True, fill='both')
        self.ref.parent.bind("<Key>",self.key_pressed)
        self.chosen = random.randint(1,99)
        self.tries = 0
        self.game_done = False
        self.display()


    def display(self):
        self.area = tkinter.Frame(self.bottom_area, background='white')
        self.area.pack(expand=True, fill='both', padx=120, pady=45)
        self.area.rowconfigure(0,weight=4)
        self.area.rowconfigure(1,weight=1)
        self.area.columnconfigure(0,weight=1)

        self.guess_var = tkinter.StringVar(self.area,'??')
        self.guess = tkinter.Label(self.area, textvariable= self.guess_var, background='white', font=('Arial', 45))
        self.guess.grid(row=0,column=0)

        self.feedback = tkinter.StringVar(self.area, "Start typing to guess")
        self.guess_feedback = tkinter.Label(self.area, textvariable= self.feedback, background='white', font=('Arial', 20))
        self.guess_feedback.grid(row=1,column=0)

    def key_pressed(self, event):

        if self.game_done :
            return
        
        if self.guess_var.get()=="??" and event.char.isdigit():
            self.guess_var.set('')
        current = self.guess_var.get()
        if event.keycode == 13 and self.guess_var.get()!='??':
            self.guess_var.set('')
            self.check(current)
        elif event.keycode == 8:
            self.guess_var.set(current[:-1])
        elif event.char.isdigit() and len(current) < 2:
            self.guess_var.set(current+event.char)

    def check(self, what):
        if not what.isdigit() :
            return
        self.tries += 1
        if int(what) > self.chosen:
            self.feedback.set("TOO HIGH")
            self.guess_feedback.config(fg='red')
        elif int(what) < self.chosen:
            self.feedback.set("TOO LOW")
            self.guess_feedback.config(fg='blue')
        elif int(what) == self.chosen:
            self.guess_var.set(what)
            self.guess_feedback.config(fg='green')
            self.gameover(True)
        if self.tries > settings.MAX_TRIES:
            self.guess_var.set(what)
            self.guess_feedback.config(fg='red')
            self.gameover(False)

    def gameover(self, iswin):
        self.game_done = True
        if iswin:
            self.feedback.set(f"YOU WIN ({self.tries} {'try' if self.tries==1 else 'tries'})")
        else:
            self.feedback.set(f"YOU LOSE (number was {self.chosen})")

        self.area.rowconfigure(2,weight=1)

        tkinter.Button(self.area, text = 'Replay')
        tkinter.Button(self.area, text='Play Again', background='white', font=('Arial',20), command=self.replay, relief=tkinter.GROOVE).grid(row=2,column=0, sticky='ew', pady=30, padx=40)

    def replay(self):
        Page(self.ref.parent,self.cwd)
        self.parent.destroy()



        
        
