import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

class StockManager(object): #Manages actions for the Stock table

    def __init__(self):
        self.cursor = Database.DatabaseHandler().connectToDb().cursor()

    def stockAccess(self):
        self.cursor.execute('SELECT itemID, itemName, stockAmount FROM Items')
        return self.cursor

    def showStockTable(self):
        print("")
        tableOutput = from_db_cursor(self.stockAccess())
        tableOutput.field_names = ["Stock ID", "Item Name", "Stock Quantity"]
        print(tableOutput.get_string(fields=["Item Name", "Stock Quantity"]))
        print("")

    def graphStock(self):
        print("Graph")
