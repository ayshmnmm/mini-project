import tkinter 
import os
from pages import settings, menu, tic_tac_toe, quiz, password_generator, sudoku_solver, number_guess, countdown_timer, hangman, chatbot

root = tkinter.Tk()
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title("Mini Project")
root.resizable(False,False)

cwd = os.path.dirname(__file__)
icon = tkinter.PhotoImage(file=os.path.join(cwd, "img/logo.png"))
root.iconphoto(False, icon)
menu.Page(root, cwd)

root.mainloop()
