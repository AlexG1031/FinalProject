from tkinter import *
from tkinter import ttk, Text

class App:
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

    def __init__(self, root):
        self.root = root
        self.name = "Avatar Aang"
        self.frame()
        self.label()
        self.text()
        self.text1.bind("<Return>", lambda x: self.onReturn())
        # self.comb

    def frame(self):
        self.frame1 = Frame(self.root) # Message box
        self.frame2 = Frame(self.root) # To: "___"
        self.frame3 = Frame(self.root) # TypeBox

        self.frame1.pack(fill=X)
        self.frame2.pack(fill=X)
        self.frame3.pack(fill=X)

    def label(self):
        self.label1= Label(self.frame2, text="To: ")
        self.label1.pack(side="left", fill=X)
        self.comboBox1 = ttk.Combobox(self.frame2, value=self.options)
        self.comboBox1.current(0)
        self.comboBox1.pack(side="left", fill=X)

    def text(self):
        self.text1 = Text(self.frame3, width=40, height=5)
        self.text1.pack(side="left")

    # def comboclick(self):
    #     self.label1 = Label(self.frame1, text=self.comboBox1.get())
    #     self.label1.pack()

    def onReturn(self):
        index = self.options.index(self.comboBox1.get())
        self.conv_texts[index] = self.conv_texts[index] + self.name + ": " + self.text1.get("0.0", "end")
        self.label2 = Label(self.frame1, text=self.conv_texts[index])
        self.label2.pack(fill=X)
        self.text1.delete("0.0", "end")

root = Tk()
root.title("Group Chat")
root.geometry("300x600")

app = App(root)
root.mainloop()
