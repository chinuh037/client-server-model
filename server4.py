import socket, select
import sys

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set socket to non-blocking
server.setblocking(False)

FORMAT = 'utf-8'

server.bind(ADDR)
server.listen(10)

print(f"[SERVER LISTNING] at {ADDR}")

# initialize list of inputs and outputs
inputs = [server]
outputs = []

# forever loop until quit()
while True:
    # Select ready files using select
    read_ready, writ_reeady, errored = select.select(inputs, outputs, inputs)

    # traversing input files
    for file in read_ready:

        # If server is ready for reading
        if file == server:
            conn, addr = server.accept()
            print(f"[INCOMMING CONNECITON] fron {addr}")
            inputs.append(conn)

        # If the input stream is stdin
        elif file == sys.stdin:
            cmd = sys.stdin.readline().strip()
            if cmd in ('exit()'):
                print('Closing SERVER')
                exit(0)
        # Otherwise the file is a client socket
        elif file:
            req = file.recv(1024).decode(FORMAT).strip()
            if req:
                print(f"Client {addr} sent -> {req}")

                if req == 'quit()':
                    response = 'quit()'
                    print(f'[Closing connection] on client {addr} request')
                    inputs.remove(file)
                else:
                    response = ''
                    try:
                        # evaluation of request
                        q_res = req
                        response = f'Request Evaluates to : {q_res}'
                    except Exception:
                        response = "Exception Occurred"

                file.sendall(response.encode(FORMAT))
            else:
                file.close()
                inputs.remove(file)