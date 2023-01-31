from app_enums import *
import sqlite3
from sqlite3 import Error
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import random


class DBManager:
    mainConnection = None
    mainCursor = None

    '''Default C'tor'''

    def __init__(self):
        self.mainConnection, self.mainCursor = self.create_db()
        global this
        this = self

    '''Data handling from GUI (GUIManager) to DAL (DBManager)'''

    def sqlHandler(operation, data):
        self = this
        match operation:
            case Operations.Register:
                return self.insert_into_user(data.user_id, data.password, data.first_name, data.last_name, data.income,
                                             data.money_spent, self.mainConnection, self.mainCursor)

            case Operations.Login:
                return self.verify_user_and_pswd(data.user_id, data.password)

            case Operations.Set_Budget:
                return self.set_budget_goal(data.user_id, data.budget, self.mainConnection, self.mainCursor)

            case Operations.Add_Transaction:
                storeId = random.randint(1, 6)
                date = datetime.datetime.now()
                return self.insert_into_transactions(data.user_id, storeId, data.amount, date, self.mainConnection,
                                                     self.mainCursor)

            case Operations.Show_Reports:
                self.generate_spending_chart(data, self.mainConnection)

    ''' function for creating a database object in our program and establishing connection'''

    def create_db_connection(self, db_file):
        DBconnection = None
        try:
            DBconnection = sqlite3.connect(db_file)
            return DBconnection
        except Error as dbError:
            print(dbError)

        return DBconnection

    ''' function to execute querry'''

    def execute_query(self, cursor, query):
        try:
            return cursor.execute(query)  # Executing the querry
        except Error as cursorError:
            print(cursorError)
            return None

    ''' the main function where we create the exact database we need'''

    def create_db(self):
        db_name = r"BudgetApp.db"  # creates a db with this name in the working directory

        budgetAppConnection = self.create_db_connection(db_name)  # Connection to the DB

        cursorApp = budgetAppConnection.cursor()  # Creating a cursor to be able to execute queries

        ''' the querry for creating the user table(columns): we store an user id, his first name and last name, he sets his income,
         and there is another column for how much money he spent'''
        user_table_querry = """ CREATE TABLE IF NOT EXISTS userTable (
                                            user_id text NOT NULL,
                                            password text NOT NULL,
                                            first_name text NOT NULL,
                                            last_name text NOT NULL,
                                            income integer NOT NULL,
                                            money_spent integer 
                                        ); """

        ''' the querry for creating the store table: the columns are: a store id, the name of the store and a category of what products are sold by this store'''
        store_table_querry = """ CREATE TABLE IF NOT EXISTS storeTable (
                                                    store_id integer PRIMARY KEY AUTOINCREMENT,
                                                    store_name text NOT NULL,
                                                    category text
                                                ); """

        ''' the querry for creating the transactions table: the foreign keys are related to the user_id and store_id to establish the relation between these 3 table,
        and there are also the amount of the transaction and the date time of it columns'''
        transactions_table_querry = """ CREATE TABLE IF NOT EXISTS transactionsTable (
                                                trans_user_id text NOT NULL,
                                                trans_store_id integer NOT NULL,
                                                amount integer NOT NULL,
                                                time_transaction text,
                                                FOREIGN KEY (trans_user_id) REFERENCES userTable (user_id),
                                                FOREIGN KEY (trans_store_id) REFERENCES storeTable (store_id)
                                            ); """

        self.select_statement('userTable', cursorApp)
        self.select_statement('transactionsTable', cursorApp)
        self.select_statement('storeTable', cursorApp)
        self.select_statement('budgetGoalTable', cursorApp)

        if budgetAppConnection is not None:
            # create user table
            self.execute_query(cursorApp, user_table_querry)

            # create store table
            self.execute_query(cursorApp, store_table_querry)

            # create transactions table
            self.execute_query(cursorApp, transactions_table_querry)

            budgetAppConnection.commit()

            return budgetAppConnection, cursorApp

        else:
            print("Error: Could not create the database!")

    ''' Verify user and password for login'''

    def verify_user_and_pswd(self, user_id, user_password):
        try:
            statement = f"SELECT user_id from userTable WHERE user_id='{user_id}' AND password = '{user_password}';"
            if not self.execute_query(self.mainCursor, statement).fetchone():
                print("Login failed")
                return False
            else:
                print("Welcome")
                return True
        except:
            print("There was a problem with the credentials")
            return False

    ''' function to insert into the user table'''

    def insert_into_user(self, insert_user_id, insert_user_password, insert_user_firstName, insert_user_lastName,
                         insert_user_income, insert_user_moneySpent, connection, cursor):

        try:
            insert_user_querry = """ INSERT INTO userTable(first_name, last_name, income, money_spent, user_id, password) VALUES ('{}', '{}', {}, {}, '{}', '{}'); 
                                """.format(insert_user_firstName, insert_user_lastName, insert_user_income,
                                           insert_user_moneySpent, insert_user_id, insert_user_password)

            self.execute_query(cursor, insert_user_querry)
            connection.commit()
            return True
        except:
            print("There was a problem with one of the fields")
            return False

    ''' function to insert into the store table'''

    def insert_into_store(self, insert_store_name, insert_store_category, connection, cursor):

        insert_store_querry = """ INSERT INTO storeTable(store_name, category) VALUES ('{}', '{}'); 
                            """.format(insert_store_name, insert_store_category)

        self.execute_query(cursor, insert_store_querry)
        connection.commit()

    ''' function to insert into the transactions table'''

    def insert_into_transactions(self, insert_user_id, insert_store_id, insert_trans_amount, insert_trans_date,
                                 connection, cursor):
        try:
            insert_trans_querry = """ INSERT INTO transactionsTable VALUES ('{}', {}, {}, '{}'); 
                                """.format(insert_user_id, insert_store_id, insert_trans_amount, insert_trans_date)

            self.execute_query(cursor, insert_trans_querry)
            cursor.execute("UPDATE userTable SET money_spent = money_spent + ? WHERE user_id = ?""",
                           (insert_trans_amount, insert_user_id))

            connection.commit()

            cursor.execute("SELECT money_spent FROM userTable WHERE user_id = ?", (insert_user_id,))
            money_spent = cursor.fetchone()

            cursor.execute("SELECT budget_goal FROM budgetGoalTable WHERE budget_user_id = ?", (insert_user_id,))
            budget_goal = cursor.fetchone()

            if (money_spent > budget_goal):
                print("You have surpassed your budget goal!")
            return True
        except:
            print("There was a problem with the amount")
            return False

    ''' function to see the rows in a table'''

    def select_statement(self, wantedTable, cursor):

        see_table = f"SELECT * FROM {wantedTable}"  # Using f-string to concatenate the variable into a string
        cursor.execute(see_table)
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    def set_budget_goal(self, insert_user_id, insert_goal, connection, cursor):
        try:
            cursor.execute(""" CREATE TABLE IF NOT EXISTS budgetGoalTable (
                                                budget_user_id text,
                                                budget_goal integer,
                                                FOREIGN KEY (budget_user_id) REFERENCES userTable (user_id)
                                            ); """)

            cursor.execute("SELECT budget_goal FROM budgetGoalTable WHERE budget_user_id = ?", (insert_user_id,))
            goal = cursor.fetchone()
            if goal is None:
                cursor.execute("INSERT INTO budgetGoalTable (budget_user_id, budget_goal) VALUES (?,?)",
                               (insert_user_id, insert_goal))
            else:
                cursor.execute("UPDATE budgetGoalTable SET budget_goal = ? WHERE budget_user_id = ?",
                               (insert_goal, insert_user_id))

            connection.commit()
            return True
        except:
            print("There was a problem with the budget")
            return False

    def generate_spending_chart(self, user_id, connection):

        spending_query = """SELECT category, SUM(amount) as money_spent, user_id 
            FROM transactionsTable 
            JOIN storeTable ON transactionsTable.trans_store_id = storeTable.store_id
            JOIN userTable ON transactionsTable.trans_user_id = userTable.user_id
            WHERE user_id = ?
            GROUP BY category, user_id;"""

        data = pd.read_sql(spending_query, connection, params=(user_id,))
        data = data[data['user_id'] == user_id]

        data.plot.pie(y='money_spent', labels=data['category'], legend=False)
        plt.title("Money Spent by Category for user: " + str(user_id))
        plt.xlabel("Category")
        plt.ylabel("Money Spent")
        plt.show()