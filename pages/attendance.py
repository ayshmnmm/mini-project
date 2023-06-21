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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/attendance.png'))
        tkinter.Button(self.top_bar, image=self.back_btn, borderwidth=0, background='white', command=self.close).pack(side='left', padx=30, pady=25)
        tkinter.Label(self.top_bar, image=self.title, borderwidth=0).place(anchor='center', x = settings.WIDTH//2, y = 50)
        Game(self.page, self.cwd, self, self.top_bar)


    def close(self):
        self.page.destroy()
        menu.Page(self.parent, self.cwd)


class Game(Page):
    def __init__(self, parent, cwd, ref, top_bar):
        self.parent = parent
        self.cwd = cwd
        self.ref = ref
        self.top_bar = top_bar
        self.default_value = 5*60
        self.bottom_area = tkinter.Frame(self.parent, background='white')
        self.bottom_area.pack(expand=True, fill='both', padx=80, pady=20)
        self.bottom_area.columnconfigure(0, weight=1)
        self.bottom_area.rowconfigure(0, weight=4)
        self.bottom_area.rowconfigure(1, weight=1)

        self.data = [
            {'code':'21MATCS41', 'subject':'Mathematics', 'attended': 30, 'total':30},
            {'code':'21CS42', 'subject':'DAA', 'attended': 57, 'total':60},
            {'code':'21CS43', 'subject':'MES', 'attended': 30, 'total':34},
            {'code':'21CS44', 'subject':'OS', 'attended': 59, 'total':60},
            {'code':'21BE45', 'subject':'Biology', 'attended': 30, 'total':70},
            {'code':'21CSL46', 'subject':'Python', 'attended': 30, 'total':40},
            {'code':'21CSL481', 'subject':'WTA', 'attended': 53, 'total':60},
            {'code':'21UH49', 'subject':'Data', 'attended': 45, 'total':56},
        ]

        self.overall = tkinter.Label(self.top_bar, text=f'', font=('Arial', 20), background='white')
        self.overall.pack(side='right', padx=15)

        self.sub_area = tkinter.Frame(self.bottom_area, background='white')
        self.sub_area.grid(row=0, column=0, sticky='news')

        self.ref.present =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/present.png'))
        self.ref.absent =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/absent.png'))

        self.display()

    def display(self):
        
        total_attended = sum([x['attended'] for x in self.data])
        total = sum([x['total'] for x in self.data])
        # print(total_attended, total)
        self.overall.config(text=f'{(total_attended/total)*100:.2f}%')

        self.sub_area.destroy()
        self.sub_area = tkinter.Frame(self.bottom_area, background='white')
        self.sub_area.grid(row=0, column=0, sticky='news')

        for i,sub in enumerate(self.data):
            frame = tkinter.Frame(self.sub_area, background='white')
            frame.rowconfigure(0, weight=1)
            # frame.rowconfigure(1, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=40)
            frame.columnconfigure(2, weight=1)
            frame.columnconfigure(3, weight=1)

            tkinter.Label(frame, text=f"{sub['code']}", anchor='w', justify='left', font=('Arial',19), background='white').grid(row=0, column=0, sticky='nsw', rowspan=2)
            if sub['total']: txt = f"{sub['attended']/sub['total']*100:.2f}%\n{self.get_comment(sub)}"
            else: txt = ''
            tkinter.Label(frame, text=txt, anchor='w', font=('Arial',9), justify='left', background='white', foreground=self.get_color(sub)).grid(row=0, column=1, sticky='sw')
            # tkinter.Label(frame, text=f"", anchor='w', justify='left', background='white').grid(row=1, column=1, sticky='nw')

            tkinter.Button(frame, text = 'Present', image=self.ref.present, background='white', borderwidth=0, command=lambda x=i: self.update(x, True)).grid(row=0, column=2)
            tkinter.Button(frame, text = 'Bunk', image=self.ref.absent, background='white', borderwidth=0, command= lambda x=i: self.update(x, False)).grid(row=0, column=3)


            frame.pack(fill='x', side='top', pady=5)

    def get_comment(self, sub):
        available_bunks = self.calculate_available(sub)
        if available_bunks >= 2:
            return f'{available_bunks} classes available to bunk'
        elif available_bunks == 1:
            return f'{available_bunks} class available to bunk'
        else:
            return f'Please attend classes'
        
    def get_color(self, sub):
        available_bunks = self.calculate_available(sub)
        if available_bunks >= 3:
            return '#45a120'
        elif available_bunks > 0:
            return '#a19a20'
        else:
            return '#eb4034'
    
        
    def calculate_available(self, sub):
        n = 0
        if not sub['total']: return 0
        a = sub['total']
        while sub['attended']/a*100 >= 85:
            a += 1
            n += 1

        return n
        

    def update(self, sub_index, ispresent):
        self.data[sub_index]['total'] += 1
        if ispresent: self.data[sub_index]['attended'] += 1
        self.display()









        
        





    
        

        
        
