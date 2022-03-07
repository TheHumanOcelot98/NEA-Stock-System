import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

SELECTALLTX = ('SELECT * FROM Transactions')

import Database, Stock, Providers, Items, Transactions, Graph

class GraphDatabaseManager(object):

    def __init__(self):
        self.txm = TransactionsManager()
        self.dbh = DatabaseHandler()

    def txGetGraphData(self):
        connect = self.dbh.connectToDb()
        cursor = connect.cursor()
        cursor.execute(SELECTALLTX)
        cursor.fetchall()
        printTx = self.dbh.connectToDb(SELECTALLTX)
        print(printTx)

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

class ItemsManager(object): #Manages actions inside the Items table

    def __init__(self):
        pass

    def itemsAccess(self):
        self.cursor.execute('SELECT itemName, stockType, stockProvider FROM Items, Types, Providers WHERE Providers.providerID = Items.providerID AND Types.typeID = Items.typeID')
        return self.cursor

    def getBuyPrices(self):
        self.cursor.execute('SELECT itemBuyCost FROM Items')
        fullPrice = self.cursor.fetchall()
        return self.makePrice(fullPrice)

    def getSellPrices(self):
        self.cursor.execute('SELECT itemSellCost FROM Items')
        fullPrice = self.cursor.fetchall()
        return self.makePrice(fullPrice)

    def showItemsTable(self):
        print("")
        tableOutput = from_db_cursor(self.itemsAccess())
        tableOutput.field_names = ["Stock Name", "Item Type", "Provider"]
        tableOutput.add_column("Item Cost (Buy)", self.getBuyPrices())
        tableOutput.add_column("Item Cost (Sell)", self.getSellPrices())
        print(tableOutput)
        print("")

    def itemsVoid(self, itemToVoid):
        self.cursor.execute('UPDATE Items SET Voided = 1 WHERE itemName = {}'.format(itemToVoid))
        return self.cursor

    def itemsInsert(self, newItemName, newItemType, newItemProvider, newItemBuyCost, newItemSellCost):
        self.cursor.execute('INSERT INTO Items (itemName, typeID, providerID, itemBuyCost, itemSellCost) VALUES (\'{}\', \'{}\', {}, {}, {})'.format(newItemName, newItemType, newItemProvider, newItemBuyCost, newItemSellCost))
        return self.cursor

class StockManager(object): #Manages actions for the Stock table

    def __init__(self):
        pass

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

class TransactionMenu(object): #Creates the menu for transactions

    def __init__(self):
        pass

    def txMainMenu(self):
        txInput = input("What would you like to do with the table? (Edit, Add, Remove, Graph, Back) ")
        match txInput:
            case "Edit":
                print("")
                print("Edit") #Edit info on a sell transaction
                print("")
                self.TxMainMenu()
            case "Add":
                print("")
                print("Add") #Record a new sell transaction
                print("")
                self.TxMainMenu()
            case "Remove":
                print("")
                print("Remove") #Remove a transaction
                print("")
                self.TxMainMenu()
            case "Graph":
                print("")
                print("Graph") #Outputs the graph of sales of different items over time
                gr = GraphDatabaseManager().txGetGraphData
                print(gr)
                print("")
                self.TxMainMenu()
            case "Back":
                print("")
                main.accessTable()
            case _:
                print("")
                print("That is not a valid option")
                print("")
                self.TxMainMenu()

class ItemsMenu(object): #Creates a menu for the Items table

    def __init__(self):
        pass

    def itemsMainMenu(self):
        itemInput = input("What would you like to do with the table? (Edit, Add, Remove, Back) ")
        match itemInput:
            case "Edit":
                print("")
                editItemRow = input("Which row would you like to edit? (Please enter the row's 'Stock Name') ")
                print("")
                editItemColumn = input("Which column would you like to edit? (Please enter the Column's Header) ")
                print("")
                print(editItemRow)      #In this section we should ask the user what they would like to edit
                print(editItemColumn)   #
                print("")
                self.itemsMainMenu()
            case "Add":
                print("")
                newItemName = input("What is the name of the new item? ")
                newItemType = input("What type of product is this (Beer, Cider, Soft Drink, Snack)? ")
                match newItemType:
                    case "Beer":
                        newItemType = int(1)
                    case "Cider":
                        newItemType = int(2)
                    case "Soft Drink":
                        newItemType = int(3)
                    case "Snack":
                        newItemType = int(4)
                newItemProvider = input("Who provides this item? ")
                self.cursor.execute('SELECT providerID FROM Providers WHERE stockProvider = \'{}\''.format(newItemProvider))
                newItemProviderID = self.cursor.fetchall()
                newItemProvider = newItemProviderID[0][0]
                newItemBuyCost = float(input("How much does this cost to buy per unit? GBP "))
                newItemSellCost = float(input("How much does this cost to sell per unit? GBP "))
                self.cursor.execute('INSERT INTO Items (itemName, typeID, providerID, itemBuyCost, itemSellCost) VALUES (\'{}\', \'{}\', {}, {}, {})'.format(newItemName, newItemType, newItemProvider, newItemBuyCost, newItemSellCost))
                print("")
                print("Item Added!")
                print("")
                self.itemsMainMenu()
            case "Remove":
                print("")
                print("Remove") #Removes a row (stock item)
                print("")
                self.itemOptions()
            case "Back":
                print("")
                main.accessTable()
            case _:
                print("")
                print("That is not a valid option")
                print("")
                self.itemsMainMenu()

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

class mainMenu(object):

    def __init__(self):
        self.dbh = DatabaseHandler()
        self.txm = TransactionsManager()
        self.itm = ItemsManager()
        self.stm = StockManager()
        self.pvm = ProvidersManager()

    def accessTable(self):
        resultCheck = 0
        tableRetrieve = input("Would you like to retrieve a table (Transactions, Providers, Stock, or Items), or Quit? ")

        match tableRetrieve:
            case "Providers":
                main.buyAccess()
            case "Transactions":
                tm = TransactionsManager()
                print(tm.showTxTable)
            case "Stock":
                main.stockAccess()
            case "Items":
                main.itemsAccess()
            case "Test":
                self.txm.txGetGraphData()
            case "Quit":
                sys.exit("Quitting...")
            case _:
                print("")
                print("That is not a valid option")
                print("")

        if resultCheck == 0:
            self.accessTable()
            
main = mainMenu()
main.accessTable()

"""
Functions of each menu
1)Level 1 MAIN MENU: Asks the user which table they want to access
2)Level 2 menu: Once the table is displayed, the user is asked how they want to interact with it
  Each table will have different functions:
    - Items: The user can add, edit and delete items. Deleting items only sets their status to VOIDED in the table, so that any transaction history of it will still make sense.
      Editing the price of an item here will create another version of it with a new stock id, so that past purchases with a different price won't affect the
      total profit made from an item.
    - Transactions: The user can add, edit or void a transaction. Any edit here will impact the stock table. The user can also generate a graph of
      different kinds of transactions, e.g., seeing how a certain product has sold over time
    - Stock: This table can only be displayed, as the stock table simply shows how much of an item there is. Edits to it will be made via the transactions table
    - Providers: The user can Add, Edit or Delete providers. As with the items table, deleting a provider will only 'void' them in the table, so that any previous transactions
      using that provider's products still works
"""