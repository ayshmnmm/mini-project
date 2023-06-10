import tkinter
from pages import settings, menu
import os
import random

x_wins = 0
y_wins = 0

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
        global x_wins, y_wins
        x_wins = 0
        y_wins = 0
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

        self.area = tkinter.Frame(self.body, background='white')
        self.area.grid(row=0, column=1, rowspan=2, pady=100, sticky='n')
        self.area.rowconfigure(0,weight=1)
        self.area.rowconfigure(1,weight=1)
        self.area.rowconfigure(2,weight=1)
        self.area.columnconfigure(0,weight=1)
        self.area.columnconfigure(1,weight=1)
        self.area.columnconfigure(2,weight=1)

        self.next_play = tkinter.Label(self.body, text="to play : X", background='white')
        self.next_play.grid(row=2,column=1, pady=10)

        self.ref.ximg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/X.png'))
        self.ref.oimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/O.png'))
        self.ref.bimg =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/blank.png'))
        self.display()

    def display(self):
        for i in range(3):
            for j in range(3):
                cell = self.xo_board[i][j]
                tkinter.Button(self.area, text='e', image=self.ref.ximg if cell=='X' else self.ref.oimg if cell=='O' else self.ref.bimg , borderwidth=0, command=lambda a=i,b=j:self.click(a,b,'user')).grid(row=i, column=j, sticky='news')

    def random_play(self):
        while True:
            i = random.randint(0,2)
            j = random.randint(0,2)
            if self.xo_board[i][j] == ' ':
                self.click(i,j,'bot')
                break

    # def minimax(self, board, maximise):
    #     for i in range(2):
    #         for j in range(2):
    #             if board[i][j] == ' ':
    #                 board[i][j] = 'O' if maximise else 'X'
    #                 score +=
        

    def click(self, i, j, who):
        if self.xo_board[i][j] != ' ' :
            return
        self.xo_board[i][j] = 'X' if self.turn%2 else 'O'
        self.display()
        if self.check_win() != ' ':
            self.game_over(self.check_win())
            return
        self.next_play.configure(text=f"to play : {'O' if self.turn%2 else 'X'}")
        self.turn += 1
        if who == 'user':
            self.random_play()
        
    def check_win(self):
        for i in range(3):
            if self.xo_board[0][i] == self.xo_board[1][i] == self.xo_board[2][i] != ' ' :
                return self.xo_board[0][i]
            if self.xo_board[i][0] == self.xo_board[i][1] == self.xo_board[i][2] != ' ' :
                return self.xo_board[i][0]
        if self.xo_board[0][0] == self.xo_board[1][1] == self.xo_board[2][2] != ' ':
            return self.xo_board[0][0]
        if self.xo_board[0][2] == self.xo_board[1][1] == self.xo_board[2][0] != ' ':
            return self.xo_board[1][1]
        if self.turn >= 9:
            return 'draw'
        return ' '

    def game_over(self, winner):
        global x_wins, y_wins
        if winner == 'draw' :
            self.next_play.configure(text='Game over: DRAW')
        else:
            self.next_play.configure(text=f'{winner} WINS!')
        x_wins += 1 if winner == 'X' else 0
        y_wins += 1 if winner == 'O' else 0
        self.parent.after(1000, self.replay)

    def replay(self):
        Page(self.ref.parent,self.cwd)
        self.parent.destroy()

