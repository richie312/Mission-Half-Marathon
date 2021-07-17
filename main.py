import flask
from flask import Flask, request, json,render_template,redirect,url_for,jsonify,json
from dotenv import load_dotenv
import mysql
import mysql.connector
import os
import sys
import pandas as pd
from datetime import datetime

""" decrypt the database details"""
main_dir = os.getcwd()
#os.listdir(os.path.join(main_dir,'auth'))
from decrypt import *

with open(r'database_auth.json','r') as readfile:
    db_auth = json.load(readfile)

app = Flask(__name__)
app.config['DEBUG'] = True

# load the environement variables

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
    OxygenLevel, PulseRate, Day,StartTime,EndTime,work_out_type)
    VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"""
    
    cursor.execute(query,(refined_duration,data['Distance'],data['Oxygen'],
                              data['PulseRate'],data['Day'],
                              data['StartTime'],data['EndTime'],
                              work_out_type))
    connection.commit()
    
    # close the cursor and connection
    cursor.close()
    connection.close()    
    
    return render_template('user_form_response.html')
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5002)



