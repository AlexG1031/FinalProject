import tkinter as tk

root = tk.Tk()
root.title("Playful GUI")
root.geometry("400x500")

e = tk.Entry(root, width=30)
e.insert(0, "Send message: ")
e.pack()

def myClick():
    myLabel = tk.Label(root, text=e.get())
    myLabel.pack()

myButton = tk.Button(root, text="Send message", command=myClick)
myButton.pack()


root.mainloop()

# canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
# canvas.grid(row=0, column=0)
#
# var=tk.StringVar()
# people_list = tk.OptionMenu(root, var, "1", "2", "3")
# people_list.config(font=("Arial", 25))
# people_list.grid(row=1, column=0)
#
# frame = tk.Frame(root, bg="white")
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
#
# b = tk.StringVar() # this will store value of textbox, now we have to print it so
# b = 'Type message here'
# label1 = tk.Label(root, text="Message box")
# label1.grid(row=3, column=0)
#
# button = tk.Button(text='Press to send message', command=com(), fg='blue')
# button.grid(row=4, column=0)
#
# text = tk.Entry(textvariable=b)
# text.grid(row=5, column=0)
