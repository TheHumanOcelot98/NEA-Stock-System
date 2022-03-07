import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

class ProvidersManager(object):

    def __init__(self):
        pass

    def providersAccess(self):
        self.cursor.execute('SELECT * FROM Providers')
        return self.cursor

    def showProviderTable(self):
        print("")
        tableOutput = from_db_cursor(self.providersAccess())
        tableOutput.field_names = ["Provider ID", "Provider Name"]
        print(tableOutput.get_string(fields=["Provider ID", "Provider Name"]))
        print("")
