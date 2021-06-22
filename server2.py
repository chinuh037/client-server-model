import socket
import threading

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# thread_list to store client connections
threadlist = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# functions to handle connected client requests
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] at {addr} connected")

    while True:
        req = conn.recv(1024).decode(FORMAT).strip()

        if req != 'quit()':
            print(f"Client {addr} sent -> {req}")
            response = ''
            try:
                q_res = eval(req)
                response = 'Answer is {}'.format(q_res)
            except Exception:
                response = 'Exception Occurred'
            print(response.encode(FORMAT))
            conn.sendall(response.encode(FORMAT))
            print(f'Response sent to {addr}')

        if req == 'quit()':
            conn.sendall('quit()'.encode(FORMAT))
            print(f"[CONNECTION CLOSED] at {addr}")
            break

    conn.close()

# function to handle connections
def start():
    server.listen()
    while True:

        # connection accepted
        conn, addr = server.accept()

        # created thread for connected clients
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        threadlist.append(thread)
        thread.start()

        # shows active connections
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
server.close()
