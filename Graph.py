import Transactions
import Database

SELECTALLTX = ('SELECT * FROM Transactions')

class GraphDatabaseManager(object):

    def __init__(self):
        self.txm = TransactionsManager()
        self.dbh = DatabaseHandler()
        self.cursor = Database.DatabaseHandler().connectToDb().cursor()

    def txGetGraphData(self):
        connect = self.dbh.connectToDb()
        cursor = connect.cursor()
        cursor.execute(SELECTALLTX)
        cursor.fetchall()
        printTx = self.dbh.connectToDb(SELECTALLTX)
        print(printTx)
