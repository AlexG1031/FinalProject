from tkinter import *

root = Tk()
root.title("Client")
name = "Avatar Aang"

frame = LabelFrame(root, text="Group Message", padx=100, pady=200)
frame.pack(padx=10, pady=10)

click=StringVar()
list = OptionMenu(frame,click, "Alpha", "Beta", "Gamma")
list.config(font=("Arial", 15))
list.pack()

def onReturn(event):
    myLabel = Label(frame, text=name + ": " + e.get())
    myLabel.pack()
    e.delete(0, 'end')


e = Entry(frame, width=30)
e.insert(0, "Send message: ")
e.bind("<Return>", onReturn)
e.pack()

root.mainloop()