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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/hangman.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        self.g = Game(self.page, self.cwd, self)


    def close(self):
        self.g.game_done = True
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref):
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.bottom_area = tkinter.Frame(self.parent, background='white')
        self.bottom_area.pack(expand=True, fill='both')
        self.game_done = False
        self.ref.parent.bind("<Key>",self.key_pressed)
        self.tries = 0
        self.guesses = []
        self.word = random.choice(settings.HANGMAN_WORDS)
        self.display()


    def display(self):
        self.area = tkinter.Frame(self.bottom_area, background='white')
        self.area.pack(expand=True, fill='both', padx=50, pady=20)
        self.area.rowconfigure(0,weight=1)
        self.area.rowconfigure(1,weight=1)
        self.area.columnconfigure(0,weight=1)
        self.area.rowconfigure(2,weight=1)
        self.area.rowconfigure(3,weight=1)
        self.area.grid_rowconfigure(3, minsize=40)


        self.ref.hang_stages = []
        for i in range(1,8):
            self.ref.hang_stages.append(tkinter.PhotoImage(file=os.path.join(self.cwd,f'img/{i}.png')))
        
        self.hanging_img = tkinter.Label(self.area, image=self.ref.hang_stages[0], borderwidth=0, background='white')
        self.hanging_img.grid(row=0, column=0, sticky='s', pady=0)

        self.guess = tkinter.Label(self.area, text=self.calculate_text(), font=('Arial',25), background='white')
        self.guess.grid(row=1, column=0)

        tkinter.Label(self.area, text=self.word[1], background='white').grid(row=2, column=0, sticky='news')


    def calculate_text(self):
        txt = ''
        for ch in  self.word[0]:
            if ch.upper() in self.guesses :
                txt += ch.upper()
            elif ch == ' ':
                txt += ' '
            else:
                txt += '_'
            txt += ' '
        return txt
    
    def check_guess(self, ch):
        if ch not in self.word[0].upper():
            self.tries += 1
            self.hanging_img.config(image=self.ref.hang_stages[self.tries])
        if self.tries >= 6:
            self.gameover(False)
            return
        if '_' not in self.calculate_text():
            self.gameover(True)

    def key_pressed(self, event):
        if self.game_done or not event.char.isalpha() or event.char.upper() in self.guesses:
            return

        guess_char = event.char.upper()
        self.guesses.append(guess_char)
       
        self.guess.config(text=self.calculate_text())
        self.check_guess(event.char.upper())


    def gameover(self, iswin):
        self.game_done = True
        if not iswin:
            self.guess.config(text=f'ans : {self.word[0]}')

        tkinter.Button(self.area, text='Play Again', background='#fae9e1', font=('Arial',15), command=self.replay, relief=tkinter.FLAT).grid(row=3,column=0, sticky='ew', pady=0, padx=100)

    def replay(self):
        Page(self.ref.parent,self.cwd)
        self.parent.destroy()



        
        
