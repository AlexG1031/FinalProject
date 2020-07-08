from tkinter import *
from tkinter import ttk, Text

options = [
    "Everyone",
    "Alex",
    "Jim",
    "Tom",
]

conv_texts = [
    "",
    "",
    "",
    "",
]

def comboclick(event):
    Label(frame, text=myCombo.get()).pack()


def onReturn(event):
    index = options.index(myCombo.get())
    conv_texts[index] = conv_texts[index] + name + ": " + t.get("0.0", "end")
    myLabel = Label(frame, text=conv_texts[index])
    myLabel.pack()
    t.delete("0.0", "end")

root = Tk()
root.title("Client")
root.geometry("800x800")
name = "Avatar Aang"

frame = LabelFrame(root, text="Group Message")
frame.pack(padx=10, pady=10, fill=None, expand=False)

toLabel = Label(frame, text="To: ")
toLabel.pack()

myCombo = ttk.Combobox(frame, value=options)
myCombo.current(0)
myCombo.pack()

t = Text(frame, height=5, width=50)
t.bind("<Return>", onReturn)
t.pack(ipady=3)

root.mainloop()