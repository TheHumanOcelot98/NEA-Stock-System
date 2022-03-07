import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

import Database, Stock, Providers, Items, Transactions, Graph

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


class mainMenu(object):

    def accessTable(self):
        resultCheck = 0
        tableRetrieve = input("Would you like to retrieve a table (Transactions, Providers, Stock, or Items), or Quit? ")

        match tableRetrieve:
            case "Providers":
                Providers.ProvidersManager().showProviderTable
            case "Transactions":
                tm = Transactions.TransactionsManager()
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