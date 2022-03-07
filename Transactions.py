
import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

import DatabaseHandler



class TransactionsManager(object): #Manages actions inside the Transactions table

    def __init__(self):
        self.dbh = DatabaseHandler()
    
    def txAccess(self):
        self.cursor.execute('SELECT transactionID, itemName, transactionType, Quantity FROM Transactions, Items, TransactionTypes WHERE Items.itemID = Transactions.itemID AND Transactions.transactionTypeID = TransactionTypes.transactionTypeID')
        return self.cursor

    def getTxDate(self):
        self.cursor.execute('SELECT transactionDate FROM Transactions')
        newDate = self.cursor.fetchall()
        return self.dbh.transformDate(newDate)

    def txInsert(self, txToInsert, txDate, txType, quantity):
        self.cursor.execute('INSERT INTO Transactions (itemID, transactionDate, transactionTypeID, Quantity) VALUES (\'{}\', \'{}\', \'{}\', {})'.format(txToInsert, txDate, txType, quantity))
        return self.cursor

    def txVoid(self, txToVoid):
        self.cursor.execute('UPDATE Transactions SET Voided = 1 WHERE transactionID = {}'.format(txToVoid))
        return self.cursor

    def txGetGraphData(self):
        printTx = self.dbh.connectToDb(SELECTALLTX)
        print(printTx)

    def showTxTable(self):
        print("")
        tableOutput = from_db_cursor(self.txAccess())
        tableOutput.add_column("Transaction Date", self.getTxDate())
        tableOutput.field_names = ["Transaction ID", "Stock Name", "Transaction Type", "Quantity Bought/Sold", "Transaction Date"]
        print(tableOutput.get_string(fields=["Transaction ID", "Stock Name", "Transaction Date", "Transaction Type", "Quantity Bought/Sold"]))
        print("")
