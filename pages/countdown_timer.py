import tkinter
from pages import settings, menu
import os
import playsound


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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/timer.png'))
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
        self.timer_running = False
        self.default_value = 5*60
        self.bottom_area = tkinter.Frame(self.parent, background='white')
        self.bottom_area.pack(expand=True, fill='both', padx=100, pady=90)
        self.bottom_area.rowconfigure(0, weight=1)
        self.bottom_area.rowconfigure(1, weight=1)
        self.bottom_area.columnconfigure(0, weight=1)
        self.bottom_area.columnconfigure(1, weight=1)

        self.timer = tkinter.Frame(self.bottom_area, background='white')
        self.timer.grid(row=0, column=0, columnspan=2, pady=20, sticky='n')
        self.timer.rowconfigure(0, weight=1)
        self.timer.columnconfigure(0,weight=2)
        self.timer.columnconfigure(1,weight=1)
        self.timer.columnconfigure(2,weight=2)
        self.timer.columnconfigure(3,weight=1)
        self.timer.columnconfigure(4,weight=2)

        tkinter.Label(self.timer, text=':', font=('Arial', 50), background='white').grid(row=0, column=1)
        tkinter.Label(self.timer, text=':', font=('Arial', 50), background='white').grid(row=0, column=3)

        self.hour_var = tkinter.StringVar(self.timer,'00')
        self.min_var = tkinter.StringVar(self.timer,'05')
        self.sec_var = tkinter.StringVar(self.timer,'00')

        self.reg=self.timer.register(self.validate_input)

        self.e1 = tkinter.Entry(self.timer, textvariable=self.hour_var, justify='center', font=('Arial',50), width=4, relief=tkinter.FLAT, validate="key", validatecommand=(self.reg, '%P'))
        self.e1.grid(row=0, column=0)
        self.e2 = tkinter.Entry(self.timer, textvariable=self.min_var, justify='center', font=('Arial',50), width=4, relief=tkinter.FLAT, validate="key", validatecommand=(self.reg, '%P'))
        self.e2.grid(row=0, column=2)
        self.e3 = tkinter.Entry(self.timer, textvariable=self.sec_var, justify='center', font=('Arial',50), width=4, relief=tkinter.FLAT, validate="key", validatecommand=(self.reg, '%P'))
        self.e3.grid(row=0, column=4)

        self.ref.refresh = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/refresh.png'))
        self.reset_btn = tkinter.Button(self.bottom_area, text='RESET',image=self.ref.refresh, borderwidth=0, background='white', command=self.reset)
        self.reset_btn.grid(row=1,column=0, padx=60, pady=0, sticky='ne')

        self.ref.play = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/play.png'))
        self.ref.pause = tkinter.PhotoImage(file=os.path.join(self.cwd,'img/pause.png'))
        self.start_btn = tkinter.Button(self.bottom_area, text='START', image=self.ref.play, borderwidth=0, background='white', command=self.start_countdown)
        self.start_btn.grid(row=1,column=1, padx=60, pady=0, sticky='nw')

        self.e1.bind("<FocusOut>", self.set_default)
        self.e2.bind("<FocusOut>", self.set_default)
        self.e3.bind("<FocusOut>", self.set_default)


    def set_default(self, event):
        self.default_value = int(self.hour_var.get())*3600 + int(self.min_var.get())*60 + int(self.sec_var.get())
        

    def validate_input(self, data):
        if len(data) <= 2 and data.isdigit():
            return True
        if data=='':
            return True
        return False
    
    def start_countdown(self):
        if not self.hour_var.get(): self.hour_var.set('00')
        if not self.min_var.get(): self.min_var.set('00')
        if not self.sec_var.get(): self.sec_var.set('00')
        self.timer.focus_set()
        self.total_seconds = int(self.hour_var.get())*3600 + int(self.min_var.get())*60 + int(self.sec_var.get())
        if not self.total_seconds : return
        if self.timer_running:
            self.timer_running = False
            self.start_btn.config(image=self.ref.play)
            return
        else:
            self.timer_running = True
            self.start_btn.config(image=self.ref.pause)
        self.timer.after(1000, self.update)

    def reset(self):
        self.timer_running = False
        self.start_btn.config(image=self.ref.play)
        hours = int(self.default_value)//3600
        self.hour_var.set(f"{hours if hours else '00':0>2}")
        mins = int(self.default_value%3600)//60
        self.min_var.set(f"{mins if mins else '00':0>2}")
        secs = int(self.default_value)%60
        self.sec_var.set(f"{secs if secs else '00':0>2}")

    def update(self):
        if self.total_seconds < 1 or not self.timer_running: return
        self.total_seconds -= 1
        hours = int(self.total_seconds)//3600
        self.hour_var.set(f"{hours if hours else '00':0>2}")
        mins = int(self.total_seconds%3600)//60
        self.min_var.set(f"{mins if mins else '00':0>2}")
        secs = int(self.total_seconds)%60
        self.sec_var.set(f"{secs if secs else '00':0>2}")
        self.timer.update()
        if not self.total_seconds: self.time_up()
        if self.total_seconds>= 1 and self.timer_running: self.timer.after(1000, self.update)

    def time_up(self):
        self.timeup = tkinter.Label(self.bottom_area, text="TIME'S UP!", background='white', font=('Arial',30))
        self.timeup.grid(row=0, column=0, columnspan=2, sticky='news')
        self.bottom_area.after(1000, self.timeup.destroy)
        self.timer_running = False
        self.start_btn.config(image=self.ref.play)
        self.timer.update()
        playsound.playsound(os.path.join(self.cwd,'audio/notify.mp3'))


        
        
