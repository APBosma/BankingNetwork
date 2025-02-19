import socket
from bankClass import bankAccount


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #allow reusing the address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_ip = "127.0.0.1"
    port = 8000

    server.bind((server_ip, port))
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")
    account = bankAccount(0,0)
    account.fileBalance()

    while True: 
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        # receive data from the client
        while True:
            request = client_socket.recv(1024)
            request = request.decode("utf-8") 
                    
            if request == "4":
                client_socket.send("closed".encode("utf-8"))
                account.allDone()
                break
            elif request == "1":
                client_socket.send((account.returnBalance()).encode("utf-8"))
            elif request == "2":
                amount = client_socket.recv(1024)
                amount = amount.decode("utf-8")
                client_socket.send((account.withdrawal(amount)).encode("utf-8"))
            elif request == "3":
                amount = client_socket.recv(1024)
                amount = amount.decode("utf-8")
                client_socket.send((account.deposit(amount)).encode("utf-8"))

            print(f"Received: {request}")


        client_socket.close()
        print("Connection to client closed")
        
run_server()
