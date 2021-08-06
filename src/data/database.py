import mysql
import mysql.connector
import os
import json
from dotenv import load_dotenv
from common.logger import logger



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
        
    def total_distance(self):
        max_week_query = "SELECT max(Day) FROM RDS_MySql.mission_half_marathon;"
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(max_week_query)
        max_week = cursor.fetchone()
        max_week = max_week[0]

        # Compute the total distances of the latest week
        total_distance_query = "select sum(DistanceCovered) from RDS_MySql.mission_half_marathon  where Day=%s"
        cursor.execute(total_distance_query,(max_week,))
        total_distance = cursor.fetchone()
        total_distance = total_distance[0]
        return total_distance

    def goal_distance(self):
        max_week_query = "SELECT max(Day) FROM RDS_MySql.mission_half_marathon;"
        conn = self.connection
        cursor = conn.cursor()
        cursor.execute(max_week_query)
        max_week = cursor.fetchone()
        max_week = max_week[0]

        # fetch the latest goal distance
        goal_distance_query = "select goal_distance from RDS_MySql.mission_half_marathon  where Day=%s"
        cursor.execute(goal_distance_query, (max_week,))
        goal_distance = cursor.fetchall()
        # fetch the highest goal
        goal_distance = [goal_distance[i][0] for i in range(len(goal_distance))]
        Not_none_values = filter(None.__ne__, goal_distance)
        goal_distance_without_na = list(Not_none_values)
        goal_distance = max(goal_distance_without_na)
        return goal_distance

    def default_data(self):
        conn = self.connection
        cursor = conn.cursor()
        query = "select * from mission_half_marathon"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
