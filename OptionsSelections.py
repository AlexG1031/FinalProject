from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Hello, Zuko here")
root.geometry("400x400")

def selected(event):
    if clicked.get() == 'Friday':
        myLabel = Label(root, text="Yay, it's Friday!").pack()
    else:
        myLabel = Label(root, text=clicked.get()).pack()

def comboclick(event):
    if myCombo.get() == 'Friday':
        myLabel = Label(root, text="Yay, it's Friday!").pack()
    else:
        myLabel = Label(root, text=myCombo.get()).pack()


options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options, command=selected)
drop.pack(pady=20)

myCombo = ttk.Combobox(root, value=options)
myCombo.current(0)
myCombo.bind("<<ComboboxSelected>>", comboclick)
myCombo.pack()

root.mainloop()