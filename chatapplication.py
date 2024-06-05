
import socket
import sys
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")

"""
Creating a client socket and providing the address family (socket.AF_INET) and type of connection (socket.SOCK_STREAM), i.e. using TCP connection.
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

"""
Setting the connection to a non-blocking state so that the recv() function call will not get blocked. It will return some exceptions only.
"""
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

"""
Here, we have encoded the username into bytes, counted the number of bytes, and then prepared a header of fixed size, that we have encoded to bytes as well.
"""

client_socket.send(username_header + username)
while True:
    message = input(f'{my_username} > ')
    if message:
        """
        encode the message into bytes, counted the number of bytes, and then prepared a header of fixed size, that we have encoded to bytes as well.
        """
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        
        client_socket.send(message_header + message)

    try:
        
        while True:
            
            username_header = client_socket.recv(HEADER_LENGTH)

            
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            
            username_length = int(username_header.decode('utf-8').strip())

            
            username = client_socket.recv(username_length).decode('utf-8')

            
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            
            print(f'{username} > {message}')

    except IOError as e:
        
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        
        continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()
