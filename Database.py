import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

class DatabaseHandler(object):

    def __init__(self):
        pass

    def connectToDb(self, sql):
        cwd = os.getcwd()
        databasePath = (cwd + "\\stockDatabase.accdb")
        return pdb.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + databasePath + ';')

    def makePrice(self, price):
        k = []
        for row in price:
            k.append("GBP " + str(round(row[0], 2)))
        return k

    def transformDate(self, newDate):
        k = []
        for row in newDate:
            k.append(row[0].strftime("%d/%m/%Y"))
        return k
