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
        self.combo()
        self.text()
        self.text1.bind("<Return>", lambda x: self.onReturn())

    def frame(self):
        self.frame1 = LabelFrame(root, text="Group Message")
        self.frame1.pack(padx=10, pady=10, fill=None, expand=False)

    def label(self):
        self.label1 = Label(self.frame1, text="To: ")
        self.label1.pack()

    def combo(self):
        self.myCombo1 = ttk.Combobox(self.frame1, value=self.options)
        self.myCombo1.current(0)
        self.myCombo1.pack()

    def text(self):
        self.text1 = Text(self.frame1, height=5, width=50)
        self.text1.pack(ipady=3)

    def comboclick(self):
        self.label1 = Label(self.frame1, text=self.myCombo1.get()).pack()

    def onReturn(self):
        print("starting at onReturn")
        index = self.options.index(self.myCombo1.get())
        self.conv_texts[index] = self.conv_texts[index] + self.name + ": " + self.text1.get("0.0", "end")
        self.myLabel = Label(self.frame1, text=self.conv_texts[index])
        self.myLabel.pack()
        self.text1.delete("0.0", "end")

root = Tk()
root.title("Client")
root.geometry("800x800")

app = App(root)
root.mainloop()
