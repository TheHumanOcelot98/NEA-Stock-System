import matplotlib as mpl
import pyodbc as pdb
from prettytable import from_db_cursor
import os
import sys

class ItemsManager(object): #Manages actions inside the Items table

    def __init__(self):
        self.cursor = Database.DatabaseHandler().connectToDb().cursor()

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
