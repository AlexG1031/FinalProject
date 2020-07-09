from tkinter import *
from tkinter import ttk, Text
import socket
import errno
import sys
import threading
from queue import Queue


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
    HEADER_LENGTH = 10
    IP = "127.0.0.1"
    PORT = 1234
    my_username = input("Username: ")
    NUMBER_OF_THREADS = 3
    JOB_NUMBER = [1, 2, 3]
    queue = Queue()
    all_connections = []
    all_address = []

    def __init__(self, root):
        self.root = root
        self.name = self.my_username
        self.frame()
        self.listbox()
        self.label()
        self.comboBox()
        self.text()
        self.text1.bind("<Return>", lambda x: self.onReturn())
        self.comboBox1.bind("<<ComboboxSelected>>", lambda x: self.comboclick())
        self.set_up_connection()
        self.create_workers()
        self.create_job(3) # will run GUI
        self.create_job(2) # will always listen for incoming message
        self.work()

    def frame(self):
        # TODO: be sure frame1 has a scroll to see past msgs
        self.frame1 = Frame(self.root)  # Message box
        self.frame2 = Frame(self.root)  # To: "___"
        self.frame3 = Frame(self.root)  # TypeBox

        self.frame1.pack(fill=X, side="top")
        self.frame3.pack(fill=X, side="bottom")
        self.frame2.pack(fill=X, side="bottom")

    def listbox(self):
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

    def label(self):
        self.label1 = Label(self.frame2, text="To: ")
        self.label1.pack(side="left", fill=X)

    def comboBox(self):
        self.comboBox1 = ttk.Combobox(self.frame2, value=self.options)
        self.comboBox1.current(0)
        self.comboBox1.pack(side="left", fill=X)

    def text(self):
        self.text1 = Text(self.frame3, width=40, height=5)
        self.text1.pack(side="left")

    def onReturn(self):
        self.msg = self.name + ": " + self.text1.get("0.0", "end")
        self.text1.delete("0.0", "end")

        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

        index = self.options.index(self.comboBox1.get())
        self.conv_texts[index].append(self.msg)
        for past_msg in self.conv_texts[index]:
            self.listbox1.insert(END, past_msg)
        # self.create_job(1)
        self.send_message()
        # print(self.msg)

    def comboclick(self):
        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)
        index = self.options.index(self.comboBox1.get())
        for past_msg in self.conv_texts[index]:
            self.listbox1.insert(END, past_msg)

    def set_up_connection(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)
        self.username = self.my_username.encode('utf-8')
        username_header = f"{len(self.username):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + self.username)

    # Create worker threads
    def create_workers(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    # Do next job that is in the queue (send message or display new message)
    def work(self):
        # while not self.queue.empty():
        while True:
            x = self.queue.get()
            # print(f'x is {x}')
            if x == 1:
                self.send_message() # don't think this will ever be used...
            if x == 2:
                self.display_recv_message()
            if x == 3:
                self.root.mainloop()
            # self.queue.task_done()

    def create_job(self, x):  # x can only be 1 or 2
        # for x in self.JOB_NUMBER:
        if x == 1 or x == 2 or x == 3:
            self.queue.put(x)
            # print("hello")
            # self.queue.join()
        else:
            print("x is not 1, 2 or 3")

    def send_message(self):
        # print("begin send_message")
        # while True:
        # print("while true 1")
        # message = input(f'{self.my_username} > ')
        message = self.msg
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + message)
        try:
            # while True:
            # print("while true 2")
            username_header = self.client_socket.recv(self.HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = self.client_socket.recv(username_length).decode('utf-8')

            message_header = self.client_socket.recv(self.HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')
            self.create_job(2)  # makes sure other clients gets updated

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            # continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()

    def display_recv_message(self):
        while True:
            # time = 0.00125
            message = ""
            if message:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.client_socket.send(message_header + message)
            try:
                while True:
                    username_header = self.client_socket.recv(self.HEADER_LENGTH)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()
                    username_length = int(username_header.decode('utf-8').strip())
                    username = self.client_socket.recv(username_length).decode('utf-8')

                    message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = self.client_socket.recv(message_length).decode('utf-8')

                    print(f'{username} > {message}')
                    self.displayToScreen(message)

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
                continue

            except Exception as e:
                print('Reading error: '.format(str(e)))
                sys.exit()
    def displayToScreen(self, message):
        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

        index = self.options.index(self.comboBox1.get())
        self.conv_texts[index].append(message)
        for past_msg in self.conv_texts[index]:
            self.listbox1.insert(END, past_msg)

root = Tk()
root.title("Group Chat")
root.geometry("300x600")

app = App(root)
