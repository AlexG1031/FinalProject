import socket
import select
from copy import copy


def get_needed_space(message):
    needed_spaces = 10 - len(
        bytes(str(len(message)), 'utf-8'))  # number of bits needed to be filled with ''
    return ' ' * needed_spaces


def generate_message(message):
    spaces = get_needed_space(message)
    return {'message_header': bytes(str(len(message)) + spaces, 'utf-8'),
            'message_data': bytes(str(message), 'utf-8')}

def notfify_clients(type, actor):
    server_name = "SERVER"
    clients_send = generate_message(clients_str)
    server_send = generate_message(server_name)

    if type == 'client_joined':
        notif_msg = "Client " + actor['message_data'].decode(
            'utf-8').strip() + " has just joined the group chat. Praise the sun!"
        notif_msg = generate_message(notif_msg)
    elif type == 'client_exited':
        notif_msg = "Client " + actor['message_data'].decode(
            'utf-8').strip() + " has just left."
        notif_msg = generate_message(notif_msg)
    else:
        raise Exception('Server: unrecognized notification type')
    for client_socket in clients:
        client_socket.send(server_send['message_header'] + server_send['message_data'] +
                           notif_msg['message_header'] + notif_msg['message_data'] +
                           clients_send['message_header'] + clients_send['message_data'])

def generate_clients_str(c_dict):
    rtn = "Everybody"
    for key, value in c_dict.items():
        val = value['message_data'].decode('utf-8')
        rtn += " " + val
    return rtn

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}
clients_str = " everyone"
client_to_socket = {}
print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        message_data = client_socket.recv(message_length)
        whom_header = client_socket.recv(HEADER_LENGTH)
        whom_length = int(whom_header.decode('utf-8').strip())
        whom_data = client_socket.recv(whom_length)
        return {'message_header': message_header, 'message_data': message_data,
                'whom_header': whom_header, 'whom_data': whom_data}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            while True:
                user = receive_message(client_socket)
                if user is False:
                    continue
                if (user['message_data'].decode('utf-8') in clients_str):
                    rejected_username = "Another client already has that username... Please choose another name"
                    rejected_username = generate_message(rejected_username)
                    client_socket.send(rejected_username['message_header'] + rejected_username['message_data'])
                else:
                    accepted_username = "username accepted :)"
                    accepted_username = generate_message(accepted_username)
                    client_socket.send(accepted_username['message_header'] + accepted_username['message_data'])
                    sockets_list.append(client_socket)
                    clients[client_socket] = user
                    clients_str = generate_clients_str(clients)
                    client_to_socket.update({user['message_data'].decode('utf-8'): client_socket})
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                                    user['message_data'].decode('utf-8')))
                    notfify_clients('client_joined', actor=user)
                    break
        else:
            remove_client = copy(clients[notified_socket])
            removed_client_encoded = clients[notified_socket]['message_data'].decode('utf-8')
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(removed_client_encoded))
                # worry about this later
                sockets_list.remove(notified_socket)

                # notify all the clients that someone just exited.
                del clients[notified_socket]
                clients_str = generate_clients_str(clients)
                del client_to_socket[removed_client_encoded]
                notfify_clients('client_exited', actor=remove_client)
                continue
            user = clients[notified_socket]
            print(f'Received message from {user["message_data"].decode("utf-8")}: {message["message_data"].decode("utf-8")}')
            clients_send = generate_message(clients_str)
            if message["whom_data"].decode('utf-8').strip() == "Everybody":
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['message_header'] + user['message_data']
                                           + message['message_header'] + message['message_data']
                                           + clients_send['message_header'] + clients_send['message_data'])
            else:
                client_socket = client_to_socket.get(message["whom_data"].decode('utf-8').strip())
                client_socket.send(user['message_header'] + user['message_data'] +
                                   message['message_header'] + message['message_data'] +
                                   clients_send['message_header'] + clients_send['message_data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
