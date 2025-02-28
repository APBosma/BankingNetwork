class bankAccount:
    # Constructor for testing functions
    def __init__(self, dollars, cents, theId):
        self.dollars = dollars
        self.cents = cents
        self.id = theId
        self.userInfo = []

        
    # Reads in all accounts information
    # UserInfo format: (string) id, (string) username, (string) password, (string) account type, (string) balance
    def accounts(self):
        with open('accounts.txt') as infile:
            temp = infile.readlines()
    
            for i in range(0, len(temp)):
                self.userInfo.append((temp[i].rstrip()).split(" "))
            
                
    # Checks and sets username if found
    def checkLogin(self, username, password):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][1] == username):
                if (self.userInfo[i][2] == password):
                    self.id = self.userInfo[i][0]
                    return True
        return False
    
    #Checks if the id exists
    def checkId(self, idNum):
        for i in range(len(self.userInfo)):
            if self.userInfo[i][0] == idNum:
                return True
        return False
    
    # Lets teller see an account's balance
    def teller_balance(self, clientId):
        for i in range(len(self.userInfo)):
            if self.userInfo[i][0] == clientId:
                return self.userInfo[i][4]
        return "I messed up. Look at teller_balance function."
    
    # Allows teller to deposit money
    def teller_deposit(self, clientId, deposit):
        for i in range(len(self.userInfo)):
            if self.userInfo[i][0] == clientId:
                base = (self.userInfo[i][4]).split('.')
                depositBase = deposit.split('.')
                finalDollars = int(base[0]) + int(depositBase[0])
                finalCents = int(base[1]) + int(depositBase[1])
                
                if finalCents >= 100:
                    finalDollars += 1
                    finalCents -= 100
                
                if (finalCents == 0):
                    balance = str(finalDollars) + ".00"
                elif (finalCents >= 10):
                    balance = str(finalDollars) + "." + str(int(finalCents))
                elif (finalCents < 10):
                    balance = str(finalDollars) + "." + "0" + str(int(finalCents))
                    
                self.userInfo[i][4] = balance
    
    # Lets teller withdrawal 
    def teller_withdrawal(self, clientId, withdrawal):
        for i in range(len(self.userInfo)):
            if self.userInfo[i][0] == clientId:
                base = (self.userInfo[i][4]).split('.')
                withdrawalBase = withdrawal.split('.')
                finalDollars = int(base[0]) - int(withdrawalBase[0])
                finalCents = int(base[1]) - int(withdrawalBase[1])
                
                if finalCents < 0:
                    finalDollars -= 1
                    finalCents += 100
                
                if (finalCents == 0):
                    balance = str(finalDollars) + ".00"
                elif (finalCents >= 10):
                    balance = str(finalDollars) + "." + str(int(finalCents))
                elif (finalCents < 10):
                    balance = str(finalDollars) + "." + "0" + str(int(finalCents))
                    
                self.userInfo[i][4] = balance
                
    # Sets up users account
    def accountSetup(self):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][0] == self.id):
                base = (self.userInfo[i][4]).split('.')
                self.dollars = int(base[0])
                self.cents = int(base[1])
                break
            
    # Creates new account for tellers, tellers can not create new teller accounts
    def makeNewAccount(self, newUsername, newPassword, newBalance):
        temp = [str(len(self.userInfo)), newUsername, newPassword, "client", newBalance]
        self.userInfo.append(temp)
                
    # Deposits money
    def deposit(self, amount):
        if "." not in amount:
            amount += ".0"
        dollarsAndCents = amount.split('.')
        if int(dollarsAndCents[0]) < 0:
            return "Invalid amount"
        elif int(dollarsAndCents[1]) > 99:
            return "Invalid amount"
        else:
            self.dollars += int(dollarsAndCents[0])
            self.cents += int(dollarsAndCents[1])
            
        if (self.cents >= 100):
            self.cents -= 100
            self.dollars += 1
                
        return "done"
    
    # Withdrawals money for client
    def withdrawal(self, amount):
        if "." not in amount:
            amount += ".0"
        dollarsAndCents = amount.split('.')
        if (self.dollars < int(dollarsAndCents[0])):
            return "Invalid amount"
        elif (self.dollars == int(dollarsAndCents[0]) and self.cents < int(dollarsAndCents[1])):
            return "Invalid amount"
        elif int(dollarsAndCents[0]) < 0:
            return "Invalid amount"
        elif int(dollarsAndCents[1]) > 99:
            return "Invalid amount"
        else:
            self.dollars -= int(dollarsAndCents[0])
            self.cents -= int(dollarsAndCents[1])
            
            if (self.cents < 0):
                self.dollars -= 1
                self.cents += 100
            return "done"
               
    # Returns money in account as string
    def returnBalance(self):
        if (self.cents == 0):
            balance = str(self.dollars) + ".00"
        elif (self.cents >= 10):
            balance = str(self.dollars) + "." + str(int(self.cents))
        elif (self.cents < 10):
            balance = str(self.dollars) + "." + "0" + str(int(self.cents)) 
        
        return balance
    
    # Changes account password
    def changePassword(self, newPassword):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][0] == self.id):
                self.userInfo[i][2] = newPassword
                break
            
    # Returns the account type: Client or Teller
    def getAccountType(self):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][0] == self.id):
                return self.userInfo[i][3]
    
    # Checks if username exists
    def usernameExist(self, username):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][1] == username):
                return True
        return False
    
    # Records transactions for tellers
    def teller_transaction(self, clientId, transactionType, money):
        import datetime
        currTime = datetime.datetime.now()
        
        tracker = open("transactions.txt", "a")
        tracker.write(self.id)
        tracker.write(" ")
        tracker.write(clientId)
        tracker.write(" ")
        tracker.write(str(currTime))
        tracker.write(" ")
        tracker.write(transactionType)
        tracker.write(" ")
        tracker.write(money)
        tracker.write(" ")
        tracker.write(self.teller_balance(clientId))
        tracker.write("\n")
    
    # Records transactions made by clients (Or tellers in some cases)
    def client_transaction(self, transactionType, money):
        import datetime
        currTime = datetime.datetime.now()
        
        tracker = open("transactions.txt", "a")
        tracker.write(self.id)
        tracker.write(" ")
        tracker.write(str(currTime))
        tracker.write(" ")
        tracker.write(transactionType)
        tracker.write(" ")
        tracker.write(money)
        tracker.write(" ")
        tracker.write(self.returnBalance())
        tracker.write("\n")
        
    # Changes account information
    def allDone(self):
        for i in range(len(self.userInfo)):
            if (self.userInfo[i][0] == self.id):
                self.userInfo[i][4] = self.returnBalance()

        rewriteBalance = open("accounts.txt", "w")
        for i in range(len(self.userInfo)):
            for j in range(len(self.userInfo[i])):
                rewriteBalance.write(self.userInfo[i][j])
                rewriteBalance.write(" ")
            rewriteBalance.write("\n")
        rewriteBalance.close()
        

