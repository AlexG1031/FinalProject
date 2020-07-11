from tkinter import *
from tkinter import ttk, Text
import socket
import errno
import sys
import threading


class Client:

    def __init__(self):
        self.clients_online = ["Everybody"]
        self.conv_texts = [
            [],
        ]
        self.HEADER_LENGTH = 10
        self.IP = "127.0.0.1"
        self.PORT = 1234
        self.root = root
        self.my_username = ""
        self.name = self.my_username

        # creating client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_up_connection(self):
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(True)

    def send(self, message, whom):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        whom = whom.encode('utf-8')
        whom_header = f"{len(whom):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message + whom_header + whom)

    def receive(self):
        try:
            username_header = self.client_socket.recv(self.HEADER_LENGTH)
            if not len(username_header):
                username_header = self.client_socket.recv(self.HEADER_LENGTH)
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            from_username = self.client_socket.recv(username_length).decode('utf-8')

            message_header = self.client_socket.recv(self.HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')

            clients_name_header = self.client_socket.recv(self.HEADER_LENGTH)
            clients_name_length = int(clients_name_header.decode('utf-8').strip())
            clients_name = self.client_socket.recv(clients_name_length).decode('utf-8')
            clients_list = list(clients_name.split(" "))

            # self.clients_online = clients_list
            for client in clients_list:
                if client not in self.clients_online:
                    self.clients_online.append(client)
                    self.conv_texts.append([])
            for client in self.clients_online:
                if client not in clients_list:
                    index = self.clients_online.index(client)
                    self.clients_online.remove(client)
                    self.conv_texts.remove(self.conv_texts[index])
            print(f'{from_username} > {message}')
            return message

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            # continue

        except Exception as e:
            print('Reading error: '.format(str(e)))
            sys.exit()


class App:

    def __init__(self, root, uname, client):
        self.client = client
        self.uname = uname

        # set up frame layout
        self.root = root
        self.frame1 = Frame(self.root)  # Message box
        self.frame2 = Frame(self.root)  # To: "___"
        self.frame3 = Frame(self.root)  # TypeBox
        self.frame()

        # set up list box
        self.listbox1 = Listbox(self.frame1)
        self.listbox()

        # set up labels
        self.label1 = Label(self.frame2, text="To: ")
        self.label()

        # create combobax
        self.combo_box = ttk.Combobox(self.frame2, value=self.client.clients_online)
        self.comboBox()
        self.combo_box.current(0)

        # create text
        self.text1 = Text(self.frame3, width=40, height=5)
        self.text()

        # self.set_up_connection() #Don't think we need this here...
        self.create_start_workers()

        self.root.mainloop()

    def frame(self):
        self.frame1.pack(fill=X, side="top")
        self.frame3.pack(fill=X, side="bottom")
        self.frame2.pack(fill=X, side="bottom")

    def listbox(self):
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

    def label(self):
        self.label1.pack(side="left", fill=X)

    def comboBox(self):
        self.combo_box.pack(side="left", fill=X)
        self.combo_box.bind("<<ComboboxSelected>>", self.comboclick)

    def text(self):
        self.text1.pack(side="left")
        self.text1.bind("<Return>", self.onReturn)

    def onReturn(self, nothing):
        msg = self.uname + ": " + self.text1.get("0.0", "end")
        self.text1.delete("0.0", "end")

        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

        index = self.client.clients_online.index(self.combo_box.get())
        self.client.conv_texts[index].append(msg)
        for past_msg in self.client.conv_texts[index]:
            self.listbox1.insert(END, past_msg)
        self.client.send(msg, self.combo_box.get())

    def comboclick(self, nothing):
        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)
        index = self.client.clients_online.index(self.combo_box.get())
        for past_msg in self.client.conv_texts[index]:
            print(f'past_msg is {past_msg}')
            self.listbox1.insert(END, past_msg)

    # Create worker threads
    def create_start_workers(self):
        t = threading.Thread(target=self.work)
        t.daemon = True
        t.start()

    def work(self):
        while True:
            msg = self.client.receive()
            self.display_recvd_message(msg)

    def display_recvd_message(self, msg):
        index = self.client.clients_online.index(self.combo_box.get())
        self.combo_box.destroy()
        self.combo_box = ttk.Combobox(self.frame2, value=self.client.clients_online)
        self.comboBox()
        self.combo_box.current(index)
        # self.comboBox()  # should this be here, bottom or doesn't matter?
        self.displayToScreen(msg)

    def displayToScreen(self, message):
        self.listbox1.destroy()
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.pack(side="left", fill=BOTH, expand=1)

        index = self.client.clients_online.index(self.combo_box.get())
        self.client.conv_texts[index].append(message)
        for past_msg in self.client.conv_texts[index]:
            self.listbox1.insert(END, past_msg)


root = Tk()
root.title("Group Chat")
root.geometry("300x600")

# create client
client = Client()
client.set_up_connection()

while True:
    my_username = input("Username: ")
    if my_username == "SERVER":
        print('Cannot have name be "SERVER')
    else:
        client.send(my_username, "")
        # now need to wait for response and see if name has already been picked
        response_header = client.client_socket.recv(client.HEADER_LENGTH)
        response_length = int(response_header.decode('utf-8').strip())
        response = client.client_socket.recv(response_length).decode('utf-8')
        if response == "username accepted :)":
            print('username accepted :)')
            break
        else:
            print('Username already chosen, please choose another name...')

app = App(root, my_username, client)
