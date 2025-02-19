import unittest
from bankClass import bankAccount

class TestingBank(unittest.TestCase):
    
    def setUp(self):
        self.account = bankAccount(42, 69)
        
    def test_Balance(self):
        self.assertEqual(self.account.returnBalance(), "42.69")
        
    #Desposit testing
    def test_DepositReg(self):
        self.account.deposit("18.00")
        self.assertEqual(self.account.returnBalance(), "60.69")
    
    def test_DepositNoDecimal(self):
        self.account.deposit("18")
        self.assertEqual(self.account.returnBalance(), "60.69")
        
    def test_DepositNegative(self):
        self.assertEqual(self.account.deposit("-18.00"), "Invalid amount")
    
    def test_DepositCents(self):
        self.assertEqual(self.account.deposit("20.999"), "Invalid amount")
    
    def test_DepositExactCents(self):
        self.account.deposit("0.31")
        self.assertEqual(self.account.returnBalance(), "43.00")
        
    def test_DepositOverCents(self):
        self.account.deposit("0.35")
        self.assertEqual(self.account.returnBalance(), "43.04")
        
        
    # Withdrawal testing
    def test_WithdrawalReg(self):
        self.account.withdrawal("12.69")
        self.assertEqual(self.account.returnBalance(), "30.00")
        
    def test_WithdrawalNoCents(self):
        self.account.withdrawal("12")
        self.assertEqual(self.account.returnBalance(), "30.69")
        
    def test_WithdrawalNegative(self):
        self.assertEqual(self.account.withdrawal("-12"), "Invalid amount")
        
    def test_WithdrawalCents(self):
        self.assertEqual(self.account.withdrawal("12.999"), "Invalid amount")
        
    def test_WithdrawalExactCents(self):
        self.account.withdrawal("0.69")
        self.assertEqual(self.account.returnBalance(), "42.00")
        
    def test_WithdrawalOverCents(self):
        self.account.withdrawal("0.70")
        self.assertEqual(self.account.returnBalance(), "41.99")
        
        
if __name__ == '__main__':
    unittest.main()