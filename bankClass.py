class bankAccount:
    # Constructor for testing functions
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents
    
    # Reads in starting balance
    def fileBalance(self):
        toe = open("BankBalance.txt", "r")
        original = toe.readline()
        dollarsAndCents = original.split('.')
        self.dollars = int(dollarsAndCents[0])
        self.cents = int(dollarsAndCents[1])
        toe.close()
        
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
    
    # Withdrawals money
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
        
    # Writes final balance in file
    def allDone(self):
        rewriteBalance = open("BankBalance.txt", "w")
        rewriteBalance.write(self.returnBalance())
        rewriteBalance.close()
        
