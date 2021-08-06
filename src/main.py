
import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
import mysql
import mysql.connector
import os
import sys
import pandas as pd
from datetime import datetime
import plotly
import plotly.express as px
from data.database import db_conn
from common.logger import logger

""" decrypt the database details"""
main_dir = os.getcwd()
#os.listdir(os.path.join(main_dir,'auth'))
#from decrypt import *

with open(r'database_auth.json','r') as readfile:
    db_auth = json.load(readfile)

app = Flask(__name__)
app.config['DEBUG'] = True

# load the environment variables

load_dotenv('.env')

""" read the list of users"""
@app.route("/")        
def homepage():
    with open(r'workout_type.txt','r') as readfile:
        workout_type = readfile.readlines()
    
    return render_template("user_form.html", workout_type = workout_type)



@app.route('/addDetails', methods=['POST'])
def addDetails():
    connection = mysql.connector.connect(host=db_auth['host'], 
                                         user=db_auth['user'],
                                         port=3306,
                                         passwd=db_auth["password"], 
                                         db=db_auth['dbname'])
    
    cursor = connection.cursor()
    data = request.form
    
    start_time = datetime.strptime(data['StartTime'],'%H:%M')
    end_time = datetime.strptime(data['EndTime'],'%H:%M')
    work_out_type = str(data['workout_type'])
    # Convert total seconds into days, hours, minutes and, seconds.
    duration = end_time - start_time
    time_delta = pd.to_timedelta(duration.total_seconds(), unit='s')
    #days = time_delta.components.days
    hour = time_delta.components.hours
    minutes = time_delta.components.minutes
    secs = time_delta.components.seconds                
    temp_duration = ("{}:{}:{}".format(hour,minutes,secs))
    refined_duration = datetime.strptime(temp_duration,'%H:%M:%S')
    
    query = """ INSERT INTO mission_half_marathon (Duration,DistanceCovered, 
    OxygenLevel, PulseRate, Day,goal_distance,StartTime,EndTime,work_out_type)
    VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s)"""
    
    cursor.execute(query,(refined_duration,data['Distance'],data['Oxygen'],
                              data['PulseRate'],data['Day'],data["Goal"],
                              data['StartTime'],data['EndTime'],
                              work_out_type))
    connection.commit()
    
    # close the cursor and connection
    cursor.close()
    connection.close()    
    
    return render_template('user_form_response.html')

@app.route('/Dashboard', methods=['GET','POST'])
def Dashboard():
    if request.method == 'GET':
        with open(r'workout_type.txt','r') as readfile:
            workout_type = readfile.readlines()
        db = db_conn()
        df = db.default_data()
        col_list = db.column_list()
        default_df = pd.DataFrame(columns=col_list)
        col_map = {'Day': 4, 'DistanceCovered': 1, 'Duration': 0, 'EndTime': 7, 'OxygenLevel': 2, 'PulseRate': 3,
                   'StartTime': 6, 'work_out_type': 8, 'goal_distance': 5}

        for col_index in range(len(col_list)):
            default_df[col_list[col_index]] = [df[i][col_map[col_list[col_index]]] for i in range(len(df))]
        # filtering data
        default_df = default_df[default_df["work_out_type"] == "Walk"]

        fig = px.bar(default_df, x=default_df["Day"], y = default_df["DistanceCovered"], color='DistanceCovered',
                     labels={"Day": "Weeks"}, title="Total Distance Each Week 2020-21")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        template= "dashboard.html"
        fetch_workout_type = "NA"
        total_distance = db.total_distance()
        goal_distance = db.goal_distance()
        

    elif request.method == 'POST':
        data = request.form
        with open(r'workout_type.txt','r') as readfile:
            workout_type = readfile.readlines()
        db = db_conn()
        df = db.default_data()
        col_list = db.column_list()
        default_df = pd.DataFrame(columns=col_list)
        col_map = {'Day': 4, 'DistanceCovered': 1, 'Duration': 0, 'EndTime': 7, 'OxygenLevel': 2, 'PulseRate': 3,
                   'StartTime': 6, 'work_out_type': 8, 'goal_distance': 5}

        for col_index in range(len(col_list)):
            default_df[col_list[col_index]] = [df[i][col_map[col_list[col_index]]] for i in range(len(df))]
        # filtering data
        default_df = default_df[default_df["work_out_type"] == data["workout_type"]]
        if len(default_df) == 0:
            template = "user_form_msg.html"
            graphJSON = "NA"
            fetch_workout_type = data["workout_type"]
            total_distance = 0
            goal_distance = 0
        else:
            df1 = default_df[["Day", "DistanceCovered"]].groupby(by=["Day"]).sum()
            fig = px.bar(default_df, x=default_df["Day"], y = default_df["DistanceCovered"], color='DistanceCovered',
                         labels={"Day": "Weeks"}, title="Total Distance Each Week 2020-21")
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            template = "dashboard.html"
            fetch_workout_type = "NA"
            # todo compute the distance as per the work out mode
            total_distance = db.total_distance()
            goal_distance = db.goal_distance()


    return render_template(template,
                           graphJSON=graphJSON,
                           workout_type = workout_type,
                           fetch_workout_type = fetch_workout_type,
                           total_distance = total_distance,
                           goal_distance = goal_distance)



    
if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5002)



