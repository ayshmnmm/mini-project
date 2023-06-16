import tkinter
from pages import settings, menu
import os
import random
import time


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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/sudoku_solver.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self)


    def close(self):
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref):
        self.parent = parent
        self.cwd = cwd
        self.ref = ref

        self.sud_area = tkinter.Frame(self.parent, background='white', padx=120, pady=45)
        self.sud_area.pack(expand=True, fill='both')
        self.sud_area.rowconfigure(0, weight=1)
        self.sud_area.rowconfigure(1, weight=1)
        self.sud_area.columnconfigure(0, weight=1)
        self.sud_area.columnconfigure(1, weight=1)

        self.display()

        self.ref.solve_img = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/solve.png'))
        self.solve_btn = tkinter.Button(self.sud_area, image=self.ref.solve_img, text='solve', bd=0 , command=self.solve_sudoku)
        self.solve_btn.grid(row=1,column=1,sticky='ws',padx=20, pady=20)

        self.ref.generate_img = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/generate.png'))
        self.generate_btn = tkinter.Button(self.sud_area, image=self.ref.generate_img, bd=0, text='generate', command=self.generate)
        self.generate_btn.grid(row=1,column=0,sticky='es',padx=20, pady=20)

    def generate(self):
        for i in range(9):
            for j in range(9):
                self.sudoku_board[i][j].set("")
        self.solve_sudoku(isgen=True)
        removed = 0
        for i in range(9):
            for j in range(9):
                if removed > 55:
                    return
                if random.random() < 0.62:
                    self.sudoku_board[i][j].set("")
                    removed += 1


        
    def validate_input(self, data):
        if data=='0':
            return False
        if len(data) <= 1 and data.isdigit():
            return True
        if data=='':
            return True
        return False

    def solve_sudoku(self, isgen=False):
        self.area.focus_set()
        self.start = time.time()
        self.solve_btn.config(state=tkinter.DISABLED)
        if not self.solve(self.sudoku_board, isgen=isgen):
            self.unsolvable()
        self.solve_btn.config(state=tkinter.NORMAL)
    
    def unsolvable(self, txt="UNSOLVABLE!"):
        self.msg = tkinter.Label(self.parent, text=txt, background='white', foreground='red', font=('Arial',20))
        self.msg.place(x=settings.WIDTH//2,y=300, anchor='center')
        self.area.after(1500, self.msg.destroy)

    

    def valid_move(self, board, num, row, column):
        for i in range(9):
            if board[row][i].get() == str(num):
                return False
            if board[i][column].get() == str(num):
                return False
        
        r = (row//3)*3
        c = (column//3)*3

        for i in range(r,r+3):
            for j in range(c,c+3):
                # print(board[i][j])
                if board[i][j].get() == str(num):
                    return False
                
        return True
    


    def solve(self, board, row=0, column=0, isgen=False):
        if row==8 and column==9:
            return True
        if time.time() - self.start > 12:
            self.unsolvable()
            return False
        
        if column==9:
            row += 1
            column = 0
        
        if board[row][column].get() :
            return self.solve(board, row, column+1, isgen)
        
        order = list(range(1,10))
        random.shuffle(order)
        for i in order:
            if self.valid_move(board, i, row, column):
                board[row][column].set(i)
                if not isgen and time.time() - self.start < 3: self.area.update()
                if self.solve(board, row, column+1, isgen):
                    return True
            board[row][column].set("")

        return False

    def display(self):
        self.area = tkinter.Frame(self.sud_area, background='white')
        self.area.grid(row=0,column=0,columnspan=2)
        self.area.rowconfigure(tuple(range(9)), weight=1)
        self.area.columnconfigure(tuple(range(9)), weight=1)
        self.sudoku_board = [[tkinter.StringVar(self.area) for j in range(9)] for i in range(9)]
        self.reg=self.area.register(self.validate_input)

        self.entries = []
        for i in range(9):
            self.row = []
            for j in range(9):
                self.row.append(tkinter.Entry(self.area, justify='center', font=('Arial', 20), relief=tkinter.RIDGE, textvariable=self.sudoku_board[i][j]))
                self.row[j].grid(row=i,column=j, sticky='news')
                self.row[j].config(validate="key", validatecommand=(self.reg, '%P'))
            self.entries.append(self.row)

    


        


