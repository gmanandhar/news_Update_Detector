from app.db import connection

class module(object):
    def __init__(self):
        self._db_connect = connection.connection()

    #  Method to create table
    def createTable(self):
        qry = "CREATE TABLE news (NID int NOT NULL AUTO_INCREMENT ,date VARCHAR(80), time VARCHAR(80), website_name VARCHAR(255), URL VARCHAR(255), content VARCHAR(255),PRIMARY KEY (NID)) "
        self._db_connect.query('CREATE',qry)
        self._db_connect.__del__()

    # Method to Insert into table news
    def insert(self,date,time,website_name,URL,content):
        qry = """INSERT INTO news (date, time,website_name, URL,content) VALUES (%s,%s,%s,%s,%s)"""
        value = (date,time,website_name,URL,content)
        self._db_connect.query('INSERT',qry,value)

    #Method to Update into news table
    def update(self,date, time, website_name, URL, content):
        qry = """UPDATE news SET date = %s,time = %s,website_name = %s, URL=%s,content=%s WHERE content=%s"""
        value = (date,time, website_name, URL, content,content)
        self._db_connect.query('UPDATE', qry, value)




