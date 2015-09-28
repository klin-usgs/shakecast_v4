import sqlite3
import random
import os

class Data_Layer(object):
    
    """
    Data Layer is used to abstract our choice of database    
    """
    
    def __init__(self):
        self.directory = ""
        self.get_path()
        
        self.conn = sqlite3.connect('%s/test.db' % self.directory)
        self.cursor = self.conn.cursor()
        self.name = 'test.db'
        
    def get_path(self):
        # get the path to the database
        
        path = os.path.dirname(os.path.abspath(__file__))
        
        if os.name == 'nt':
            delim = '\\'
        else:
            delim = '/'
            
        path = path.split(delim)
        
        path[-2] = 'db'
        del path[-1]
        
        self.directory = delim.join(path)
        
    def close(self):
        # close connection to the database
        self.conn.commit()
        self.conn.close()
        
    def query(self, sql):
        # SQL query to the DB
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception, e:
            result = 'Query Failed: %s \nException: %s' % (sql, str(e))
            
        return result
