from app_models import BudgetModel, LoginModel, RegisterModel, TransactionModel
from dbManager import *
from app_enums import *
from tkinter import *

'''In order not to create a monolith, I'm trying to seprate functionalities so other components could be replace/upgraded quickly.
   This class represents the GUI Layer and transfers all the DAL Layer. Since there is no complex logic I didn't add BL but, It is necessary otherwise.
   Due to lack of time I didn't create a logout button after login and I generated random numbers for transcation creation query 
'''
class GUIManager:
    '''Common Variables '''
    ''' ------------------ '''
    '''Main window '''
    window = None
    '''Operations and delegates dictionary '''
    dic = {}
    '''Secondary Toolbar '''
    toolbar = None
    '''Result Label '''
    resultLabel = None
    '''DAL Instance '''
    dbManager = None
    '''CurrentUser '''
    currentUser = None
    '''MainFrame '''
    mainFrame = None
    ''' ------------------ '''
    '''Inputs for Regiseration frame and Login frame'''
    INCOME = None
    USERNAME = None
    PASSWORD = None
    FIRSTNAME =None
    LASTNAME = None
    registerFrame = None
    loginFrame = None
    loginLabel = None
    ''' ------------------ '''
    '''Inputs for Budget frame'''
    BUDGET = None
    ''' ------------------ '''
    '''Inputs for "Transaction" frame'''
    AMOUNT = None
    ''' ------------------ '''

    '''Default C'tor'''
    def __init__(self):
        self.window = Tk()
        self.window.configure(bg= self._from_rgb((26, 68, 67)))
        self.dic = {
        "Set Budget" : self.buildBudgetFrame,
        "Add Transaction" : self.buildAmountFrame,
        "Reports" : self.show_report
        }
        self.dbManager = DBManager()
        self.INCOME = StringVar()
        self.PASSWORD = StringVar()
        self.FIRSTNAME = StringVar()
        self.LASTNAME = StringVar()
        self.USERNAME = StringVar()
        self.BUDGET = StringVar()
        self.AMOUNT = StringVar()
        self.window.title("BudgetApp")
        self.window.resizable(False, False)
        window_height =  self.window.winfo_screenheight()
        window_width = self.window.winfo_screenwidth()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.buildLoginFrame()
        self.window.mainloop()

    '''Convert int to rgb in order to set Background for all GUI Components'''
    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb 

    '''Clear main frame'''
    def clear(self, event):
        self.toolbar.pack_forget()


    def buildSecondaryToolbar(self):
        self.toolbar = Frame(self.window,width=500,height=300, background=self._from_rgb((26, 68, 67)))
        self.toolbar.pack()
        btns = []
        for key in self.dic:
            btns.append(Button(self.toolbar, background=self._from_rgb((26, 68, 67)), text= key, font= ('arial', 18), width = 20, activebackground=self._from_rgb((26, 68, 67))))
            btns[btns.__len__() - 1].pack(side=LEFT, padx=100, pady=20)
            btns[btns.__len__() - 1].bind('<Button-1>', self.dic[key]) 
    
    def buildRegisterationFrame(self):
        if self.mainFrame != None:
            self.mainFrame.destroy()
        self.registerFrame = Frame(self.window, background=self._from_rgb((26, 68, 67)))
        self.registerFrame.pack(side=TOP, pady=self.window.winfo_screenheight()/4)
        lbl_username = Label(self.registerFrame, text="Username:", font=('arial', 18), bd=18, background=self._from_rgb((26, 68, 67)))
        lbl_username.grid(row=1)
        lbl_password = Label(self.registerFrame, text="Password:", font=('arial', 18), bd=18, background=self._from_rgb((26, 68, 67)))
        lbl_password.grid(row=2)
        lbl_firstname = Label(self.registerFrame, text="Firstname:", font=('arial', 18), bd=18, background=self._from_rgb((26, 68, 67)))
        lbl_firstname.grid(row=3)
        lbl_lastname = Label(self.registerFrame, text="Lastname:", font=('arial', 18), bd=18, background=self._from_rgb((26, 68, 67)))
        lbl_lastname.grid(row=4)
        lbl_lastname = Label(self.registerFrame, text="Income:", font=('arial', 18), bd=18, background=self._from_rgb((26, 68, 67)))
        lbl_lastname.grid(row=5)
        self.resultLabel = Label(self.registerFrame, text="", font=('arial', 18), background=self._from_rgb((26, 68, 67)))
        self.resultLabel.grid(row=6, columnspan=2)
        username = Entry(self.registerFrame, font=('arial', 20), textvariable=self.USERNAME, width=15, background=self._from_rgb((26, 68, 67)))
        username.grid(row=1, column=1)
        password = Entry(self.registerFrame, font=('arial', 20), textvariable=self.PASSWORD, width=15, show="*", background=self._from_rgb((26, 68, 67)))
        password.grid(row=2, column=1)
        firstname = Entry(self.registerFrame, font=('arial', 20), textvariable=self.FIRSTNAME, width=15, background=self._from_rgb((26, 68, 67)))
        firstname.grid(row=3, column=1)
        lastname = Entry(self.registerFrame, font=('arial', 20), textvariable=self.LASTNAME, width=15, background=self._from_rgb((26, 68, 67)))
        lastname.grid(row=4, column=1)
        income = Entry(self.registerFrame, font=('arial', 20), textvariable=self.INCOME, width=15, background=self._from_rgb((26, 68, 67)))
        income.grid(row=5, column=1)
        btn_login = Button(self.registerFrame, text="Register", font=('arial', 18), width=35, command=self.Register, background=self._from_rgb((26, 68, 67)), activebackground=self._from_rgb((26, 68, 67)))
        btn_login.grid(row=7, columnspan=2, pady=20)
        lbl_login = Label(self.registerFrame, text="Login", fg="Blue", font=('arial', 12), background=self._from_rgb((26, 68, 67)))
        lbl_login.grid(row=0, sticky=W)
        lbl_login.bind('<Button-1>', self.ToggleToLogin)

    def buildLoginFrame(self):
        if self.mainFrame != None:
            self.mainFrame.destroy()
        self.loginFrame = Frame(self.window, background=self._from_rgb((26, 68, 67)))
        self.loginFrame.pack(side=TOP, pady=self.window.winfo_screenheight()/4)
        lbl_username = Label(self.loginFrame, text="Username:", font=('arial', 25), bd=18,background=self._from_rgb((26, 68, 67)))
        lbl_username.grid(row=1)
        lbl_password = Label(self.loginFrame, text="Password:", font=('arial', 25), bd=18,background=self._from_rgb((26, 68, 67)))
        lbl_password.grid(row=2)
        self.resultLabel = Label(self.loginFrame, text="", font=('arial', 18),background=self._from_rgb((26, 68, 67)))
        self.resultLabel.grid(row=3, columnspan=2)
        username = Entry(self.loginFrame, font=('arial', 20), textvariable=self.USERNAME, width=15,background=self._from_rgb((26, 68, 67)))
        username.grid(row=1, column=1)
        password = Entry(self.loginFrame, font=('arial', 20), textvariable=self.PASSWORD, width=15, show="*",background=self._from_rgb((26, 68, 67)))
        password.grid(row=2, column=1)
        btn_login = Button(self.loginFrame, text="Login", font=('arial', 18), width=35, command=self.Login,background=self._from_rgb((26, 68, 67)), activebackground=self._from_rgb((26, 68, 67)))
        btn_login.grid(row=4, columnspan=2, pady=20)
        lbl_register = Label(self.loginFrame, text="Register", fg="Blue", font=('arial', 12),background=self._from_rgb((26, 68, 67)))
        lbl_register.grid(row=0, sticky=W)
        lbl_register.bind('<Button-1>', self.ToggleToRegister)

    def buildBudgetFrame(self, event):
        if self.mainFrame != None:
            self.mainFrame.destroy()
        self.mainFrame = Frame(self.window, background=self._from_rgb((26, 68, 67)))
        self.mainFrame.pack(side=TOP, pady=self.window.winfo_screenheight()/4)
        lbl_budget = Label(self.mainFrame, text="Budget:", font=('arial', 25), bd=18,background=self._from_rgb((26, 68, 67)))
        lbl_budget.grid(row=1)
        self.resultLabel = Label(self.mainFrame, text="", font=('arial', 18),background=self._from_rgb((26, 68, 67)))
        self.resultLabel.grid(row=3, columnspan=2)
        budget = Entry(self.mainFrame, font=('arial', 20), textvariable=self.BUDGET, width=15,background=self._from_rgb((26, 68, 67)))
        budget.grid(row=1, column=1)
        btn_submit = Button(self.mainFrame, text="Submit", font=('arial', 18), width=35, command=self.set_budget,background=self._from_rgb((26, 68, 67)), activebackground=self._from_rgb((26, 68, 67)))
        btn_submit.grid(row=2, columnspan=2, pady=20)

    def buildAmountFrame(self, event):
        if self.mainFrame != None:
            self.mainFrame.destroy()
        self.mainFrame = Frame(self.window, background=self._from_rgb((26, 68, 67)))
        self.mainFrame.pack(side=TOP, pady=self.window.winfo_screenheight()/4)
        lbl_budget = Label(self.mainFrame, text="Amount:", font=('arial', 25), bd=18,background=self._from_rgb((26, 68, 67)))
        lbl_budget.grid(row=1)
        self.resultLabel = Label(self.mainFrame, text="", font=('arial', 18),background=self._from_rgb((26, 68, 67)))
        self.resultLabel.grid(row=3, columnspan=2)
        amount = Entry(self.mainFrame, font=('arial', 20), textvariable=self.AMOUNT, width=15,background=self._from_rgb((26, 68, 67)))
        amount.grid(row=1, column=1)
        btn_submit = Button(self.mainFrame, text="Submit", font=('arial', 18), width=35, command=self.add_transacation,background=self._from_rgb((26, 68, 67)), activebackground=self._from_rgb((26, 68, 67)))
        btn_submit.grid(row=2, columnspan=2, pady=20)


    def ToggleToLogin(self, event):
        self.registerFrame.destroy()
        self.clearAll()
        self.buildLoginFrame()       

    def set_budget(self):
       try:
         if DBManager.sqlHandler(Operations.Set_Budget, BudgetModel(user_id = self.currentUser, budget= int(self.BUDGET.get()))):
                                                                    self.resultLabel.config(text="Success", fg="Blue")
                                                                    self.clearAll()
         else:
           self.resultLabel.config(text="Failed To Set Budget!", fg="Red")
       except:
           self.resultLabel.config(text="Failed To Set Budget!", fg="Red")

    def add_transacation(self):
       try:
         if DBManager.sqlHandler(Operations.Add_Transaction, TransactionModel(user_id = self.currentUser, amount= int(self.AMOUNT.get()))):
                                                                    self.resultLabel.config(text="Success", fg="Blue")
                                                                    self.clearAll()
         else:
           self.resultLabel.config(text="Failed To Add Transcation!", fg="Red")
       except:
           self.resultLabel.config(text="Failed To Add Transaction!", fg="Red")

    def show_report(self, event):
       try:
           DBManager.sqlHandler(Operations.Show_Reports, self.currentUser)
       except:
           self.resultLabel.config(text="Couldn't Show Reports", fg="Red")



    def Register(self):
        try:
            if DBManager.sqlHandler(Operations.Register, RegisterModel(first_name= self.FIRSTNAME.get(), last_name= self.LASTNAME.get(), income= int(self.INCOME.get()),
                                                                    money_spent= 0, user_id= self.USERNAME.get(), password= self.PASSWORD.get())):
                                                                     self.resultLabel.config(text="Success", fg="Blue")
                                                                     self.clearAll()
            else:
                self.resultLabel.config(text="Failed To Register!", fg="Red")
        except:
            self.resultLabel.config(text="Failed To Register!", fg="Red")

    def Login(self):
         if not DBManager.sqlHandler(Operations.Login, LoginModel(user_id= self.USERNAME.get(), password= self.PASSWORD.get())):
             self.resultLabel.config(text="Failed To Login!", fg="Red")
         else:
            self.currentUser = self.USERNAME.get()
            self.clearAll()
            self.loginFrame.destroy()
            self.buildSecondaryToolbar()


    def ToggleToRegister(self, event):
        self.loginFrame.destroy()
        self.clearAll()
        self.buildRegisterationFrame()

    def clearAll(self):
        self.INCOME = StringVar()
        self.PASSWORD = StringVar()
        self.FIRSTNAME = StringVar()
        self.LASTNAME = StringVar()
        self.USERNAME = StringVar()
        self.BUDGET = StringVar()
        self.AMOUNT = StringVar()
