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
os.listdir(os.path.join(main_dir,'auth'))
from decrypt import *

db_auth = {'dbname.txt':'key_dbname.txt',
           'db_pass.txt':'key_db_pass.txt',
           'host.txt':'key_host.txt',
           'dbuser.txt':'key_dbuser.txt'}
filename = {}
for i in db_auth.keys():
    with open(r'auth/' +i, 'r') as readfile:
        filename['{}'.format(i.split('.')[0])]= json.load(readfile)

file_key = {}
for i in db_auth.keys():
    with open(r'auth/' +db_auth[i], 'r') as readfile:
        file_key['{}'.format(db_auth[i].split('.')[0])]= json.load(readfile)

db_auth = {}
for i in filename.keys():
    db_auth[i] = decrypt(eval(filename[i]),eval(file_key['key_'+i])).decode("utf-8")

app = Flask(__name__)
app.config['DEBUG'] = True

# load the environement variables

load_dotenv('.env')

""" read the list of users"""
@app.route("/")        
def homepage():
    return render_template("user_form.html")



@app.route('/addDetails', methods=['POST'])
def addDetails():
    connection = mysql.connector.connect(host=db_auth['host'], 
                                         user=db_auth['dbuser'],
                                         port=3306,
                                         passwd=db_auth['db_pass'], 
                                         db=db_auth['dbname'])
    
    cursor = connection.cursor()
    data = request.form
    
    start_time = datetime.strptime(data['StartTime'],'%H:%M')
    end_time = datetime.strptime(data['EndTime'],'%H:%M')
    
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
    OxygenLevel, PulseRate, Day,StartTime,EndTime)
    VALUES (%s, %s, %s,%s,%s,%s,%s)"""
    
    cursor.execute(query,(refined_duration,data['Distance'],data['Oxygen'],
                              data['PulseRate'],data['Day'],
                              data['StartTime'],data['EndTime']))
    connection.commit()
    
    # close the cursor and connection
    cursor.close()
    connection.close()    
    
    return render_template('user_form_response.html')
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True,port=5002)



