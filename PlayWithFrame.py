from tkinter import *

root = Tk()
root.title('Hello, Zuko here')

frame = LabelFrame(root, text="Group message", padx=50, pady=50)
frame.pack(padx=10,pady=10)

b = Button(frame, text="send message")
# label.grid(row=0, column=0)
b.grid(row=0, column=0)

root.mainloop()