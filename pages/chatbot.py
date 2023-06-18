import tkinter
from pages import settings, menu
import os
from chatterbot import ChatBot
import time
time.clock = time.time
from chatterbot.trainers import ChatterBotCorpusTrainer
import collections.abc
collections.Hashable = collections.abc.Hashable

chatbot = ChatBot("Bot")
# trainer = ChatterBotCorpusTrainer(chatbot)

# trainer.train("chatterbot.corpus.english.greetings",
#         "chatterbot.corpus.english.conversations",
#         "chatterbot.corpus.english")

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
        self.title =  tkinter.PhotoImage(file=os.path.join(self.cwd,'img/chattybot.png'))
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
        self.bottom_area.pack(expand=True, fill='both', padx=80, pady=45)
        self.bottom_area.columnconfigure(0, weight=1)
        self.bottom_area.rowconfigure(0, weight=4)
        self.bottom_area.rowconfigure(1, weight=1)

        self.input_area = tkinter.Frame(self.bottom_area, background='white')
        self.input_area.grid(row=1, column=0, sticky='ew', padx=0)

        self.input_area.columnconfigure(0, weight=4)
        self.input_area.columnconfigure(1, weight=1)
        self.input_area.rowconfigure(0, weight=1)

        self.msgs = [{'author':'BOT', 'message':'Hello I am a chatbot, start the chat by saying hi.'}]

        self.input_var = tkinter.StringVar(self.input_area)
        self.input_wid = tkinter.Entry(self.input_area, textvariable=self.input_var, font=('Arial',15))
        self.input_wid.bind('<Return>',self.send)
        self.input_wid.focus()
        self.input_wid.grid(row=0,column=0, sticky='news')

        self.ref.send_img = tkinter.PhotoImage(file=os.path.join(cwd, "img/send.png"))
        self.send_btn = tkinter.Button(self.input_area, image=self.ref.send_img, background='white', borderwidth=0, command=self.send)
        self.send_btn.grid(row=0, column=1, sticky='e')

        self.chat_area = tkinter.Frame(self.bottom_area, background='green')
        self.chat_area.grid(row=0, column=0, sticky='news')

        self.display_texts()

    def display_texts(self):
        prev_msg = None
        self.chat_area.destroy()
        self.chat_area = tkinter.Frame(self.bottom_area, background='white')
        self.chat_area.grid(row=0, column=0, sticky='news')

        for msg in self.msgs[-7:]:
            if not prev_msg or msg['author'] != prev_msg['author']:
                tkinter.Label(self.chat_area, text=msg['author'], anchor='w', background='white', foreground='red' if msg['author']=='ME' else 'blue').pack(fill='x', side='top')
            frame = tkinter.Frame(self.chat_area, background='white')
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=80)
            tkinter.Frame(frame, background='red' if msg['author']=='ME' else 'blue', width=3).grid(row=0, column=0, sticky='wns')
            tkinter.Label(frame, text=msg['message'], anchor='w', wraplength=406, font=('Arial',12), justify='left', background='white').grid(row=0, column=1, sticky='ew')
            frame.pack(fill='x', side='top')

            prev_msg = msg

    def respond(self, query):
        msg = {}
        msg['author'] = 'BOT'
        msg['message'] = chatbot.get_response(query)
        self.msgs.append(msg)
        self.display_texts()

    def send(self, event=None):
        inp = self.input_var.get()
        if not inp.strip(): return
        msg = {}
        msg['author'] = 'ME'
        msg['message'] = inp
        self.msgs.append(msg)
        self.display_texts()
        self.input_var.set('')
        self.bottom_area.update()
        self.respond(inp)
        
        





    
        

        
        
