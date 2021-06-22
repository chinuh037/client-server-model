import socket

# function to handle client
def handle_client(conn, addr):
    while state == "running":
        print(f"[NEW CONNECTION] {addr} connected.")

        # receive request
        req = conn.recv(1024).decode(FORMAT).strip()

        # continue until server reaches quit
        while req != 'quit()':
            print('Client sent : {}'.format(req))
            response = ''
            try:
                # evaluate client request
                q_res = eval(req)
                # prepare a response
                response = 'Answer is {}'.format(q_res)
            except Exception:
                response = 'Exception Occurred'

            # print response
            print(response.encode(FORMAT))
            # send response
            conn.sendall(response.encode(FORMAT))
            print('response sent')

            # server open for further requests
            req = conn.recv(1024).decode(FORMAT).strip()

        # if req is quit(), break connection
        if req == 'quit()':
            conn.sendall('quit()'.encode(FORMAT))
            break


PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

print("[STARTING] server is starting....")

# loop
while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    # server is listening
    server.listen(1)
    print("[LISTEN] server is listening on {}:{}".format(SERVER, PORT))

    state = "running"

    # connection accepted
    conn, addr = server.accept()

    # server closed because another client must not connect.
    server.close()

    # function called
    handle_client(conn, addr)
    conn.close()


# socket.close()
