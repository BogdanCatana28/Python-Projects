'''This modules is used in order to build differnet models in order to send it from GUI (GUIManager) to DAL(DBManager)'''
class RegisterModel():

    first_name = None
    last_name = None
    income = None
    money_spent = None
    user_id = None
    password = None

    def __init__(self, first_name, last_name, income, money_spent, user_id, password):
        self.first_name = first_name
        self.last_name = last_name
        self.income = income
        self.money_spent = money_spent
        self.user_id = user_id
        self.password = password

class LoginModel():

    user_id = None
    password = None

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password 

class BudgetModel():

    user_id = None
    budget = None

    def __init__(self, user_id, budget):
        self.user_id = user_id
        self.budget = budget 

class TransactionModel():

    user_id = None
    amount = None

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount 
