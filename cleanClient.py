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
        [],
        [],
        [],
        [],
    ]

    def __init__(self, root):
        self.root = root
        self.name = "Avatar Aang"
        self.frame()
        self.listbox()
        self.label()
        self.comboBox()
        self.text()
        self.text1.bind("<Return>", lambda x: self.onReturn())
        self.comboBox1.bind("<<ComboboxSelected>>", lambda x: self.comboclick())

    def frame(self):
        #TODO: be sure frame1 has a scroll to see past msgs
        self.frame1 = Frame(self.root) # Message box
        self.frame2 = Frame(self.root) # To: "___"
        self.frame3 = Frame(self.root) # TypeBox

        self.frame1.pack(fill=X, side="top")
        self.frame3.pack(fill=X, side="bottom")
        self.frame2.pack(fill=X, side="bottom")

    def listbox(self):
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)


    def label(self):
        self.label1= Label(self.frame2, text="To: ")
        self.label1.pack(side="left", fill=X)

    def comboBox(self):
        self.comboBox1 = ttk.Combobox(self.frame2, value=self.options)
        self.comboBox1.current(0)
        self.comboBox1.pack(side="left", fill=X)

    def text(self):
        self.text1 = Text(self.frame3, width=40, height=5)
        self.text1.pack(side="left")

    def onReturn(self):
        msg = self.name + ": " + self.text1.get("0.0", "end")
        self.text1.delete("0.0", "end")

        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

        index = self.options.index(self.comboBox1.get())
        self.conv_texts[index].append(msg)
        for past_msg in self.conv_texts[index]:
            self.listbox1.insert(END, past_msg)

    def comboclick(self):
        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)
        index = self.options.index(self.comboBox1.get())
        for past_msg in self.conv_texts[index]:
            self.listbox1.insert(END, past_msg)

root = Tk()
root.title("Group Chat")
root.geometry("300x600")

app = App(root)
root.mainloop()
