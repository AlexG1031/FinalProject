import socket
import select
from copy import copy


def get_needed_space(message):
    needed_spaces = 10 - len(
        bytes(str(len(message)), 'utf-8'))  # number of bits needed to be filled with ''
    return ' ' * needed_spaces


def generate_message(message):
    spaces = get_needed_space(message)
    return {'header': bytes(str(len(message)) + spaces, 'utf-8'),
            'data': bytes(str(message), 'utf-8')}

def notfify_clients(type, actor):
    server_name = "SERVER"  # TODO a client cannot call him or her self SERVER
    clients_send = generate_message(clients_str)
    server_send = generate_message(server_name)

    if type == 'client_joined':
        notif_msg = "Client " + actor['data'].decode(
            'utf-8').strip() + " has just entered the group chat. Praise the sun!"
        notif_msg = generate_message(notif_msg)
    elif type == 'client_exited':
        notif_msg = "Client" + actor['data'].decode(
            'utf-8').strip() + " has just left."
        notif_msg = generate_message(notif_msg)
    else:
        raise Exception('Server: unrecognized notification type')
    for client_socket in clients:
        client_socket.send(server_send['header'] + server_send['data'] +
                           notif_msg['header'] + notif_msg['data'] +
                           clients_send['header'] + clients_send['data'])

def generate_clients_str(c_dict):
    rtn = "Everybody"
    for key, value in c_dict.items():
        val = value['data'].decode('utf-8')
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
            if (user['data'].decode('utf-8') in clients_str):
                rejected_username = "Another client already has that username... Please choose another name"
                rejected_username = generate_message(rejected_username)
                client_socket.send(rejected_username['header'] + rejected_username['data'])
                break
            else:
                accepted_username = "username accepted :)"
                accepted_username = generate_message(accepted_username)
                client_socket.send(accepted_username['header'] + accepted_username['data'])
            sockets_list.append(client_socket)
            clients[client_socket] = user
            clients_str = generate_clients_str(clients)
            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))
            notfify_clients('client_joined', actor=user)
        else:
            remove_client = copy(clients[notified_socket])
            removed_client_encoded = clients[notified_socket]['data'].decode('utf-8')
            message = receive_message(notified_socket)
            if message is False:
                print('Closed connection from: {}'.format(removed_client_encoded))
                # worry about this later
                sockets_list.remove(notified_socket)

                # notify all the clients that someone just exited.
                del clients[notified_socket]
                clients_str = generate_clients_str(clients)

                notfify_clients('client_exited', remove_client)
                continue
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            clients_send = generate_message(clients_str)
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']
                                       + clients_send['header'] + clients_send['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
