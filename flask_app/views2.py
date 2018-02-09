from flask import render_template
from flask import request
from flask_app import app
from flask_app.a_Model import ModelIt
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import requests
import pickle
from wunderground_api import key_id
import datetime
from flask_app.predict_z import z_calc
from sklearn.externals import joblib

# connect to Postgres
user = 'postgres' #add your Postgres username here      
host = '/var/run/postgresql/'
dbname = 'bart_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database=dbname, host=host, user=user, password="simon6toes")

@app.route('/')
# def cesareans_input():
def input():
    return render_template("input.html")

@app.route('/output')
def output():
  
    # pull 'data' from input fields and store it
    rain = request.args.get('rain')
    hour = request.args.get('hour')
    date_in = request.args.get('date')
    date = pd.to_datetime(date_in).date()
    #b4_hour = hour - 1
    #after_hour = hour + 1
    #selected_day = np.int(request.args.get('selected_day'))
    station = request.args.get('station')
    direction = request.args.get('direction')
    temp = request.args.get('temperature')
  
    # get day index from date
    if date == datetime.date.today():
        selected_day = 0        
    elif date == (datetime.date.today() + datetime.timedelta(days=1)):
        selected_day = 1
    elif date == (datetime.date.today() + datetime.timedelta(days=2)):
        selected_day = 2
    elif date == (datetime.date.today() + datetime.timedelta(days=3)):
        selected_day = 3
  
    # get name of day
    day = date.strftime("%A")
  
    # get month
    month = date.month
    
    # is it a weekday?
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    if day in weekdays:
        weekday = 1
    else:
        weekday = 0
    
    #Prepare the feature vector for prediction
    pkl_file = open('cat_updated.pkl', 'rb')
    index_dict = pickle.load(pkl_file)
    new_vector = np.zeros(len(index_dict))

    # get zipcode for current station
    sql_query = ("SELECT zipcode FROM bart_station_info WHERE abbr = '%s';" 
                 % station)
    query_results=pd.read_sql_query(sql_query,con)
    zip_str = query_results.loc[0, 'zipcode']
  
    # use zipcode to fetch weather forecast
    response = requests.get('http://api.wunderground.com/api/%s/forecast/q/%s.json'
                            % (key_id, zip_str)).json()
    forecast_df = json_normalize(
            response['forecast']['simpleforecast']['forecastday'])
    # get high temp
    temp = np.int(forecast_df.loc[selected_day, 'high.fahrenheit'])
    # if cumulative precipitation > 0.0 inches, rain = 1
    precip = forecast_df.loc[selected_day, 'qpf_allday.in']
    if precip > 0:
        rain = 1
    else:
        rain = 0
  
    try:
        new_vector[index_dict['max_temperature']] = temp
    except:
        pass
    try:
        new_vector[index_dict['rain']] = rain
    except:
        pass
    try:
        new_vector[index_dict['hour']] = hour
    except:
        pass
    try:
        new_vector[index_dict['month_' + str(month)]] = 1
    except:
        pass
    try:
        new_vector[index_dict['weekday']] = weekday
    except:
        pass
    try:
        new_vector[index_dict['station_' + str(station)]] = 1
    except:
        pass
    try:
        new_vector[index_dict['northbound']] = direction
    except:
        pass

    model = joblib.load('rf_reg_updated.pkl')
    #model = pickle.load(pkl_file)
    prediction = model.predict(new_vector.reshape(1, -1))
    
    # get z-score of predcition normalized to station
    pred_z = z_calc(prediction[0], station)
    if pred_z <= 1:
        pred_str = 'LOW'
        pred_color = 'green'
        suggest = 'You should have plenty of room!'
    elif (pred_z > 1) & (pred_z <=3):
        pred_str = 'MODERATE'
        pred_color = 'orange'
        suggest = 'The train should be moderately busy. There may or may not be seating.'
    elif pred_z > 3:
        pred_str = 'HIGH'
        pred_color = 'red'
        suggest = 'The train and platform will likely be very crowded! Consider checking crowd levels for either an earlier or later time, or check the crowd levels at a station up the line.'
    
    return render_template('output.html', prediction=pred_str, suggestion=suggest, col=pred_color)
  
