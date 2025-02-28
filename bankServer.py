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
    account = bankAccount(0,0, "nothing")
    account.accounts()

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        signedIn = False
        loginAttempts = 0

         # receive data from the client
        while True:
             while (signedIn == False and loginAttempts < 3):
                 username = client_socket.recv(1024)
                 username = username.decode("utf-8")
                 password = client_socket.recv(1024)
                 password = password.decode("utf-8")
                 check = account.checkLogin(username, password)
                 
                 if check == True:
                     account.accountSetup()
                     client_socket.send("Good".encode("utf-8"))
                     signedIn = True
                 elif (check == False and (loginAttempts+1) >= 3):
                     loginAttempts += 1
                     client_socket.send("Close".encode("utf-8"))
                 else:
                     loginAttempts += 1
                     client_socket.send("Bad".encode("utf-8"))
                     
             if (loginAttempts >= 3):
                 break
                
             client_socket.send((account.getAccountType()).encode("utf-8"))   
                
             while signedIn == True:
                  request = client_socket.recv(1024)
                  request = request.decode("utf-8")
                  
                  # Client get balance
                  if request == "1":
                      client_socket.send((account.returnBalance()).encode("utf-8"))
                      account.client_transaction("Balance", "0")
                  # Client withdrawal
                  elif request == "2":
                      amount = client_socket.recv(1024)
                      amount = amount.decode("utf-8")
                      client_socket.send((account.withdrawal(amount)).encode("utf-8"))
                      account.client_transaction("Withdrawal", amount)
                  # Client deposit
                  elif request == "3":
                      amount = client_socket.recv(1024)
                      amount = amount.decode("utf-8")
                      client_socket.send((account.deposit(amount)).encode("utf-8"))
                      account.client_transaction("Deposit", amount)
                  # Change account password
                  elif request == "4":
                      password = client_socket.recv(1024)
                      password = password.decode("utf-8")
                      account.changePassword(password)
                      account.client_transaction("Password Change", "0")
                  # Log out
                  elif request == "5":
                      client_socket.send("closed".encode("utf-8"))
                      signedIn = False
                      account.allDone()
                      break
                  # Create new account
                  elif request == "6":
                      while True:
                          newUsername = client_socket.recv(1024)
                          newUsername = newUsername.decode("utf-8")
                          if (account.usernameExist(newUsername) == True):
                              client_socket.send("bad".encode("utf-8"))
                          else:
                              client_socket.send("good".encode("utf-8"))
                              break
                      newPassword = client_socket.recv(1024)
                      newPassword = newPassword.decode("utf-8")
                      newBalance = client_socket.recv(1024)
                      newBalance = newBalance.decode("utf-8")
                      account.makeNewAccount(newUsername, newPassword, newBalance)
                  # Check client's account balance
                  elif request == "7":
                      while True:
                          clientId = client_socket.recv(1024)
                          clientId = clientId.decode("utf-8")
                          checker = account.checkId(clientId)
                          if checker == True:
                              client_socket.send("good".encode("utf-8"))
                              break
                          else:
                              client_socket.send("bad".encode("utf-8"))
                      client_socket.send((account.teller_balance(clientId)).encode("utf-8"))
                      account.teller_transaction(clientId, "Balance", "0")
                 # Teller deposit
                  elif request == "8":
                      while True:
                          clientId = client_socket.recv(1024)
                          clientId = clientId.decode("utf-8")
                          checker = account.checkId(clientId)
                          if checker == True:
                              client_socket.send("good".encode("utf-8"))
                              break
                          else:
                              client_socket.send("bad".encode("utf-8"))
                      deposit = client_socket.recv(1024)
                      deposit = deposit.decode("utf-8")
                      account.teller_deposit(clientId, deposit)
                      account.teller_transaction(clientId, "deposit", deposit)
                  # Teller withdrawal
                  elif request == "9":
                      while True:
                          clientId = client_socket.recv(1024)
                          clientId = clientId.decode("utf-8")
                          checker = account.checkId(clientId)
                          if checker == True:
                              client_socket.send("good".encode("utf-8"))
                              break
                          else:
                              client_socket.send("bad".encode("utf-8"))
                      client_socket.send((account.teller_balance(clientId)).encode("utf-8"))
                      withdrawal = client_socket.recv(1024)
                      withdrawal = withdrawal.decode("utf-8")
                      account.teller_withdrawal(clientId, withdrawal)
                      account.teller_transaction(clientId, "Withdrawal", withdrawal)
        
        
run_server()
