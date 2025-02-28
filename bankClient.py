import socket

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"
    server_port = 8000
    client.connect((server_ip, server_port))
    loggedIn = False
    accountType = None
    
    print("Welcome to the Scambarino Scambino Bank!\n")
    while True:
        while loggedIn == False:
            print("Please log in.")
            username = input("Username: ")
            password = input("Password: ")
            client.send(username.encode("utf-8")[:1024])
            client.send(password.encode("utf-8")[:1024])
            
            loginCheck = client.recv(1024)
            loginCheck = loginCheck.decode("utf-8")
            if (loginCheck == "Close"):
                print("Please stop hacking. Don't come back.")
                break
            elif (loginCheck == "Good"):
                loggedIn = True
                break 
        if loginCheck == "Close":    
            client.close()
            break
        
        accountType = client.recv(1024)
        accountType = accountType.decode("utf-8")
        while (loggedIn == True):
            if accountType == "client":
                # Menu 
                print("What would you like to do", username + "?")
                print("1. Check balance")
                print("2. Make a withdrawal")
                print("3. Make a deposit")
                print("4. Change password")
                print("5. Log out")
                msg = input("Please enter the number corresponding with what you'd like to do: \n")
                
                if msg == "1" or msg == "2" or msg == "3" or msg == "4" or msg == "5":
                    client.send(msg.encode("utf-8")[:1024])
                else:
                    print("Whoops, that's not an option! Please try again!")
                    
            elif accountType == "teller":
                # Menu
                print("What would you like to do", username + "?")
                print("1. Create new account")
                print("2. Check client's balance")
                print("3. Deposit money in client account")
                print("4. Withdrawal money from client account")
                print("5. Change password")
                print("6. Log out")
                msg = input("Please enter the number corresponding with what you'd like to do: \n")
                
                if msg == "1":
                    msg = "6"
                    client.send(msg.encode("utf-8")[:1024])
                elif msg == "2":
                    msg = "7"
                    client.send(msg.encode("utf-8")[:1024])
                elif msg == "3":
                    msg = "8"
                    client.send(msg.encode("utf-8")[:1024])
                elif msg == "4":
                    msg = "9"
                    client.send(msg.encode("utf-8")[:1024])
                elif msg == "5":
                    msg = "4"
                    client.send(msg.encode("utf-8")[:1024])
                elif msg == "6":
                    msg = "5"
                    client.send(msg.encode("utf-8")[:1024])
                else:
                    print("Whoops, that's not an option! Please try again!")
                    
            # Shows account balance
            if msg == "1" and accountType == "client":
                response = client.recv(1024) # Recieves balance
                response = response.decode("utf-8")
                print("Balance: $" + response + "\n\n")
            # Withdrawal money
            elif msg == "2" and accountType == "client":
                amount = input("How much would you like to take out?\n")
                client.send(amount.encode("utf-8")[:1024]) # Sends amount
                response = client.recv(1024) # Recieves done or invalid amount
                response = response.decode("utf-8")
                if (response == "done"):
                    print("All done!\n\n")
                else:
                    print("Whoops! you can't withdrawal more money than you have in your account or negative money!\n")
            # Deposit money
            elif msg == "3" and accountType == "client":
                amount = input("How much would you like to deposit?\n")
                client.send(amount.encode("utf-8")[:1024]) # Sends amount
                response = client.recv(1024) # Recieves done or invalid amount
                response = response.decode("utf-8")
                if (response == "done"):
                    print("All done!\n\n")
                else:
                    print("Whoops! you can't deposit negative money!\n")
            # Change password
            elif msg == "4":
                passwordReset = False
                while passwordReset == False:
                    firstPassword = input("Please type your new password: ")
                    secondPassword = input("Please type your new password again to verify: ")
                    
                    if firstPassword == secondPassword:
                        client.send(firstPassword.encode("utf-8")[:1024])
                        print("Your password has been changed!\n\n")
                        passwordReset = True
                    else:
                        print("Uh oh! Your passwords don't match! Please try again!")
            # Leave
            elif msg == "5":
                response = client.recv(1024) #Recieves close
                response = response.decode("utf-8")
                print("Goodbye!\n\n")
                loggedIn = False;
            # Create new account
            elif msg == "6" and accountType == "teller":
                while True:
                    newUsername = input("Please enter the username for the new account: ")
                    client.send(newUsername.encode("utf-8")[:1024])
                    check = client.recv(1024)
                    check = check.decode("utf-8")
                    if check == "good":
                        break
                    else:
                        print("Please try again.")
                newPassword = input("Please enter the new password: ")
                client.send(newPassword.encode("utf-8")[:1024])
                newBalance = input("Please enter the balance with cents: ")
                client.send(newBalance.encode("utf-8")[:1024])
                print("All done.\n\n")
            # Get an account's balance
            elif msg == "7" and accountType == "teller":
                while True:
                    clientId = input("Please enter the ID of the account: ")
                    client.send(clientId.encode("utf-8")[:1024])
                    exists = client.recv(1024)
                    exists = exists.decode("utf-8")
                    if exists == "bad":
                        print("No user exists with that ID. Please try again.")
                    else:
                        break
                balance = client.recv(1024)
                balance = balance.decode("utf-8")
                print("The client's balance is $" + balance + "\n\n")
            # Deposit into an account
            elif msg == "8" and accountType == "teller":
                while True:
                    clientId = input("Please enter the ID of the account: ")
                    client.send(clientId.encode("utf-8")[:1024])
                    exists = client.recv(1024)
                    exists = exists.decode("utf-8")
                    if exists == "bad":
                        print("No user exists with that ID. Please try again.")
                    else:
                        break
                while True:
                    deposit = input("How much is being deposited? Please include cents.\n")
                    if (deposit[0] == '-') or ('.' not in deposit):
                        print("That amount is invalid, please try again.")
                    else:
                        client.send(deposit.encode("utf-8")[:1024])
                        break
                print("Amount deposited.\n\n")
            # Withdrawl from an account
            elif msg == "9" and accountType == "teller":
                while True:
                    clientId = input("Please enter the ID of the account: ")
                    client.send(clientId.encode("utf-8")[:1024])
                    exists = client.recv(1024)
                    exists = exists.decode("utf-8")
                    if exists == "bad":
                        print("No user exists with that ID. Please try again.")
                    else:
                        break
                balance = client.recv(1024)
                balance = balance.decode("utf-8")
                while True:
                    withdrawal = input("How much is being withdrawn? Please include cents.\n")
                    if (withdrawal[0] == '-') or ('.' not in withdrawal) or (float(withdrawal) > float(balance)):
                        print("That amount is invalid, please try again.")
                    else:
                        client.send(withdrawal.encode("utf-8")[:1024])
                        break
                print("Amount withdawn.\n\n")



run_client()

