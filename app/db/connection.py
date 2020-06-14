import mysql.connector

# specify database configurations
config = {
    'host': 'localhost',
    'user': 'news',
    'password': 'toor',
    'database': 'news_scrap_db'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_name = config.get('database')


class connection(object):

    #Constructor
    def __init__(self):
        try:
            self._db_connect =mysql.connector.connect(host = db_host,
                    user = db_user,
                    password = db_pwd,
                    database = db_name)
            self._db_cur = self._db_connect.cursor()
        except Exception as e:
            print(e)

    # Function for Database operation
    def query(self,operation, query, params=""):
        self._db_cur.execute(query,params)
        if operation == 'UPDATE' or operation == 'DELETE' or operation == 'INSERT':
            return self._db_connect.commit()
        elif operation == 'READ':
            return self._db_cur.fetchall()

    # Function to close connection
    def __del__(self):
        self._db_connect.close()

