# Import socket module 
import socket

PORT = 5000
SERVER = "192.168.56.1"

# tuple
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# socket create
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# forever loop
while True:
    req_string = input('\nEnter request string : ')

    # if string is empty
    if req_string == '':
        req_string = 'HTTP/1.1\r\n'
        # req_string += 'connection: close\r\n'
    req_string += '\r\n'

    # send request
    client.sendall(req_string.encode(FORMAT))

    # receive response
    response = client.recv(1024)
    response = response.decode(FORMAT, errors='ignore')

    # close connection if response is quit()
    if response == 'quit()':
        client.close()
        print(f'Closing Connection {SERVER}')
        break
    # exit client if response is exit()
    elif response == 'exit()':
        client.close()
        print(f'Closing Connection {SERVER}')
        exit(0)

    # else print the response
    print(response, end='')

# close client connection
client.close()
