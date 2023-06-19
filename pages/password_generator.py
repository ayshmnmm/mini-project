import tkinter
from pages import settings, menu
import os
import random
import pyperclip


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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/password.png'))
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
        self.gen_area = tkinter.Frame(self.parent, background='white')
        self.gen_area.pack(expand=True, fill='both')
        self.limit = False
        self.display()

    def set_text(self, e, text):
        e.delete(0,tkinter.END)
        e.insert(0,text)

    def display(self):
        self.area = tkinter.Frame(self.gen_area, background='white')
        self.area.pack(expand=True, fill='both', padx=140, pady=140)
        self.area.columnconfigure(0, weight=1)
        self.area.columnconfigure(1, weight=1)
        self.area.rowconfigure(0, weight=5)
        self.area.rowconfigure(1, weight=1)
        self.password = tkinter.Entry(self.area, font=('Arial',20), justify='center', relief='flat')
        self.password.grid(row=0,column=0, columnspan=2, sticky='new')

        self.ref.refresh = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/refresh.png'))
        self.ref.copy = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/copy.png'))
        self.regen_btn = tkinter.Button(self.area, text='Regenerate', image=self.ref.refresh, command=self.generate_password, borderwidth=0, background='white')
        self.regen_btn.grid(row=1, column=0)
        self.copy_btn = tkinter.Button(self.area, text="Copy", image=self.ref.copy, command=self.copy, borderwidth=0, background='white', disabledforeground='white')
        self.copy_btn.grid(row=1, column=1)
        self.generate_password()
    
    def copy(self):
        if self.limit : return
        self.confirmation = tkinter.Label(self.parent, text='Copied!', foreground='green', background='white', font=('Arial', 20))
        self.confirmation.place(x=settings.WIDTH//2,y=300,anchor='center')
        self.limit = True
        self.area.after(800, lambda: self.confirmation.destroy())
        self.area.after(800, lambda: self.update_limit())
        pyperclip.copy(self.password.get())

    def update_limit(self):
        self.limit = False

    def generate_password(self):
        passwd = []
        uppercase = [chr(x) for x in range(65,65+26)]
        lowercase = [chr(x) for x in range(97,97+26)]
        digit = [str(i) for i in range(10)]
        symbol = ("!@#$%^&*(){}[]-_=+.,<>|~`")
        passwd.extend(random.sample(uppercase,random.randint(3,5)))
        passwd.extend(random.sample(lowercase,random.randint(3,5)))
        passwd.extend(random.sample(digit,random.randint(3,5)))
        passwd.extend(random.sample(symbol,random.randint(3,5)))
        random.shuffle(passwd)
        self.password.config(state='normal')
        self.set_text(self.password, ''.join(passwd))
        self.password.config(state='readonly')
