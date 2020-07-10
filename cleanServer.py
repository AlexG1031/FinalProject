import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}
clients_str = ""
print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            if (len(clients_str) > 0):
                clients_str += " " + user['data'].decode('utf-8')
            else:
                clients_str = user['data'].decode('utf-8')
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))

        else:
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                # worry about this later
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            needed_spaces = 10 - len(bytes(str(len(clients_str)), 'utf-8')) # number of bits needed to be filled with ''
            spaces = ""
            while needed_spaces > 0:
                spaces += " "
                needed_spaces = needed_spaces - 1
            print(f'spaces is {needed_spaces}')
            clients_send = {'header': bytes(str(len(clients_str)) + spaces, 'utf-8'),
                            'data': bytes(str(clients_str), 'utf-8')}
            print(f'clients_send header is {bytes(str(len(clients_str)), "utf-8")}')
            print(f'client_send data is {bytes(str(clients_str), "utf-8")}')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']
                                       + clients_send['header'] + clients_send['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
