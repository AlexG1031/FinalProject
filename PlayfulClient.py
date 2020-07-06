from tkinter import *

root = Tk()
root.title("Client")
# root.geometry("200x600")

frame = LabelFrame(root, text="Group Message", padx=100, pady=200)
frame.pack(padx=10, pady=10)

click=StringVar()
list = OptionMenu(frame,click, "Alpha", "Beta", "Gamma")
list.config(font=("Arial", 15))
list.pack()

e = Entry(frame, width=30)
e.insert(0, "Send message: ")
e.pack()

def myClick():
    myLabel = Label(frame, text=e.get())
    myLabel.pack()

myButton = Button(frame, text="send", command=myClick)
myButton.pack()

root.mainloop()