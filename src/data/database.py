import mysql
import mysql.connector
import os
import json
from dotenv import load_dotenv




class db_conn():

    def __init__(self):
        with open(r'database_auth.json', 'r') as readfile:
            db_auth = json.load(readfile)
        # load the environment variables
        load_dotenv('.env')
        self.connection = mysql.connector.connect(host=db_auth['host'],
                                             user=db_auth['user'],
                                             port=3306,
                                             passwd=db_auth["password"],
                                             db=db_auth['dbname'])

    def conn_adapter(self):
        return self.connection
    
    def column_list(self):
        column_query = """SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_SCHEMA=%s 
                        AND TABLE_NAME=%s;"""
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(column_query,("RDS_MySql","mission_half_marathon",))
        col_list = cursor.fetchall()
        col_list = [col_list[i][0] for i in range(len(col_list))]
        return col_list
        
        

    def default_data(self):
        conn = self.connection
        cursor = conn.cursor()
        query = "select * from mission_half_marathon"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
