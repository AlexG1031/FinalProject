from tkinter import *
from tkinter import ttk, Text

options = [
    "Alex",
    "Jim",
    "Tom",
]

def comboclick(event):
    Label(frame, text=myCombo.get()).pack()

def onReturn(event):
    myLabel = Label(frame, text=name + ": " + t.get("0.0", "end"))
    myLabel.pack()
    t.delete("0.0", "end")

root = Tk()
root.title("Client")
name = "Avatar Aang"

frame = LabelFrame(root, text="Group Message", padx=100, pady=200)
frame.pack(padx=10, pady=10)

toLabel = Label(frame, text="To: ")
toLabel.pack()

myCombo = ttk.Combobox(frame, value=options)
myCombo.current(0)
myCombo.pack()

t = Text(frame, height=5, width=50)
t.bind("<Return>", onReturn)
t.pack(ipady=3)

root.mainloop()