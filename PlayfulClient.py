from tkinter import *
from tkinter import ttk

options = [
    "Alex",
    "Jim",
    "Tom",
]

def comboclick(event):
    Label(frame, text=myCombo.get()).pack()

def onReturn(event):
    myLabel = Label(frame, text=name + ": " + e.get())
    myLabel.pack()
    e.delete(0, 'end')

root = Tk()
root.title("Client")
name = "Avatar Aang"

frame = LabelFrame(root, text="Group Message", padx=100, pady=200)
frame.pack(padx=10, pady=10)

myCombo = ttk.Combobox(frame, value=options)
myCombo.current(0)
myCombo.pack()

e = Entry(frame, width=30)
e.insert(0, "Send message: ")
e.bind("<Return>", onReturn)
e.pack()

root.mainloop()