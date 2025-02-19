import socket

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000
    client.connect((server_ip, server_port))
    
    print("Welcome to the Scambarino Scambino Bank!\n")
    while True:
        while True:
            # Menu
            print("What would you like to do?")
            print("1. Check balance")
            print("2. Make a withdrawal")
            print("3. Make a deposit")
            print("4. Leave")
            msg = input("Please enter the number corresponding with what you'd like to do: \n")
            
            if msg == "1" or msg == "2" or msg == "3" or msg == "4":
                break
            else:
                print("Whoops, that's not an option! Please try again!")
        client.send(msg.encode("utf-8")[:1024])
        
            # Shows account balance
        if msg == "1":
            response = client.recv(1024) # Recieves balance
            response = response.decode("utf-8")
            print("Balance: $" + response + "\n")
                
            # Withdrawal money
        elif msg == "2":
            amount = input("How much would you like to take out?\n")
            client.send(amount.encode("utf-8")[:1024]) # Sends amount
            response = client.recv(1024) # Recieves done or invalid amount
            response = response.decode("utf-8")
            if (response == "done"):
                print("All done!\n")
            else:
                print("Whoops! you can't withdrawal more money than you have in your account or negative money!\n")
                    
            # Deposit money
        elif msg == "3":
            amount = input("How much would you like to deposit?\n")
            client.send(amount.encode("utf-8")[:1024]) # Sends amount
            response = client.recv(1024) # Recieves done or invalid amount
            response = response.decode("utf-8")
            if (response == "done"):
                print("All done!\n")
            else:
                print("Whoops! you can't deposit negative money!\n")
                    
        # Leave
        elif msg == "4":
            response = client.recv(1024) #Recieves close
            response = response.decode("utf-8")
            print("Goodbye!")
            break;
        
        else:
            print("Whoops! That's not an option! Please try again.")


    client.close()

run_client()
