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
        self.comboBox()
        self.text()
        self.text1.bind("<Return>", lambda x: self.onReturn())
        self.comboBox1.bind("Click", lambda x: self.comboclick())

    def frame(self):
        #TODO: be sure frame1 doesn't go over the other frames
        self.frame1 = Frame(self.root) # Message box
        self.frame2 = Frame(self.root) # To: "___"
        self.frame3 = Frame(self.root) # TypeBox

        self.frame1.pack(fill=X, side="top")
        self.frame3.pack(fill=X, side="bottom")
        self.frame2.pack(fill=X, side="bottom")

    def label(self):
        self.label1 = Label(self.frame1, text=self.conv_texts[0])
        self.label2= Label(self.frame2, text="To: ")
        self.label1.pack(side="left")
        self.label2.pack(side="left", fill=X)

    def comboBox(self):
        self.comboBox1 = ttk.Combobox(self.frame2, value=self.options)
        self.comboBox1.current(0)
        self.comboBox1.pack(side="left", fill=X)

    def text(self):
        self.text1 = Text(self.frame3, width=40, height=5)
        self.text1.pack(side="left")

    def onReturn(self):
        # TODO: possibly for return, have each text be in a frame so that
        #       they all can be on the left side
        index = self.options.index(self.comboBox1.get())
        self.conv_texts[index] = self.conv_texts[index] + self.name + ": " + self.text1.get("0.0", "end")
        self.label1.destroy()
        self.label1 = Label(self.frame1, text=self.conv_texts[index])
        self.label1.pack(side="left")
        self.text1.delete("0.0", "end")

    def comboclick(self):
        # TODO: have this work properly so that changing the thing within
        #       the comboBox also changes the text displayed on top
        self.label1 = Label(self.frame1, text=self.comboBox1.get())
        self.label1.pack(side="left")
        self.onReturn()

root = Tk()
root.title("Group Chat")
root.geometry("300x600")

app = App(root)
root.mainloop()
