import tkinter 
import os
from pages import settings, menu, tic_tac_toe, quiz, password_generator

root = tkinter.Tk()
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Mini Project")
root.resizable(False,False)

cwd = os.path.dirname(__file__)
menu.Page(root, cwd)

root.mainloop()
