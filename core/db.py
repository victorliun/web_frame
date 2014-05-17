import MySQLdb as mdb
import logging

class DBHelper(object):
    """docstring for DBHelper"""

    table = "url_short"
    def __init__(self, host='localhost', user='testdb', password='test123',default_db='testdb'):
        try:
            self.con = mdb.connect(host, user, password, default_db)
            self.cursor = self.con.cursor()
        except mdb.OperationalError, err:
            logging.error(err)
            self.con = None

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)
    
    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        one = self.cursor.fetchone()
        return one

    def rowcount(self):
        return self.cursor.rowcount

    def last_insert_id(self):
        return self.con.insert_id()

    def select(self, table, columns, where):
        return self.cursor.execute("SELECT %s from %s where %s" %(columns, table, where))

    def __del__(self):
        if self.con:
            self.con.close()


class  Table(DBHelper):
    """docstring for  Table"""
    def __init__(self, **kwargs):
        self.fields = self.get_fields()
        self.table_name = 'url_short'

    def get_fields(self):
        self.cursor.execute("desc %s" %self.table_name)
        columns = self.cursor.fetchall()
        fields = []
        for field in fields:
            if field[2] == "NO":
                null = False
            else:
                null = True
            fields.append(field[0], null)
    
    def fetchone(self):
        pass

db = DBHelper()
