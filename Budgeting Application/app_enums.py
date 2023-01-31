from enum import Enum
'''This enum is used in order to handle dynamic data that is being transferred from GUI (GUIManager) to DAL(DBManager)'''
class Operations(Enum):
    Login = 1
    Register = 2
    Add_Transaction = 3
    Set_Budget = 4
    Show_Reports = 5