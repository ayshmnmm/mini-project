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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/quiz.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self, self.top_bar)


    def close(self):
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref, top_bar):
        self.questions = settings.QUIZ_QUESTIONS.copy()
        self.score = 0
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.count = 0
        self.top_bar = top_bar
        self.quiz_area = tkinter.Frame(self.parent, background='white')
        self.quiz_area.pack(expand=True, fill='both')
        self.scoreboard = tkinter.Label(self.top_bar, text=f'', font=('Arial', 25), background='white')
        self.scoreboard.pack(side='right', padx=15)
        
        ques = random.choice(self.questions)
        self.questions.remove(ques)
        self.display(ques[0],ques[1],ques[2])
        

    def display(self, question, options, correct_index):
        self.area = tkinter.Frame(self.quiz_area, background='white')
        self.area.pack(expand=True, fill='both', padx=120, pady=45)
        self.area.rowconfigure(0,weight=1)
        self.area.rowconfigure(1,weight=1)
        self.area.rowconfigure(2,weight=1)
        self.area.rowconfigure(3,weight=1)
        self.area.rowconfigure(4,weight=1)
        self.area.rowconfigure(5,weight=1)
        self.area.columnconfigure(0,weight=1)
        tkinter.Label(self.area, text=question, font=('Arial',15), background='white', wraplength=360).grid(row=0, column=0, sticky='n')
        self.buttons = []
        for i in range(1,5):
            self.buttons.append(tkinter.Button(self.area, text=options[i-1], background='white', activebackground='#94e36f' if (i-1)==correct_index else '#e38f8f', bd=0, command=lambda x=i-1, bts=self.buttons:self.click(x,correct_index,bts), relief=tkinter.GROOVE, borderwidth=1, disabledforeground='black'))
        
        randorder = list(range(4))
        random.shuffle(randorder)
        k = 0
        for i in randorder:
            self.buttons[k].grid(row=i+1, column=0, sticky='ewns', pady=2)
            k += 1

    def ask_questions(self):  
        ques = random.choice(self.questions)
        self.questions.remove(ques)
        self.area.destroy()
        self.display(ques[0],ques[1],ques[2])
        if self.count >= settings.QUESTIONS_COUNT: 
            self.gameover()
        

    def click(self, choice, correct_index, buttons):
        for button in buttons:
            button.config(state=tkinter.DISABLED)
        self.count += 1
        if choice==correct_index:
            buttons[choice].config(background='#94e36f')
            self.score += 1
        else:
            buttons[choice].config(background='#e38f8f')
        self.scoreboard.config(text=f'{self.score}/{self.count}')
        self.area.after(1000,lambda:self.ask_questions())

    def gameover(self):
        self.area.destroy()
        self.message = tkinter.Frame(self.quiz_area, background='white')
        self.message.pack(expand=True,fill='both', padx=120, pady=75)
        self.message.rowconfigure(0,weight=1)
        self.message.rowconfigure(0,weight=1)
        self.message.columnconfigure(0,weight=1)
        tkinter.Label(self.message, text=f'{(100*self.score/self.count):.2f}%', font=('Arial',50), background='white').grid(row=0,column=0)
        tkinter.Button(self.message, text='Play Again', background='white', font=('Arial',20), command=self.replay, relief=tkinter.GROOVE).grid(row=1,column=0, sticky='ew', pady=30, padx=40)
        # tkinter.Label(self.message, text='OVERRR')

    def replay(self):
        Page(self.ref.parent,self.cwd)
        self.parent.destroy()

