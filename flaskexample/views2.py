from flask import render_template
from flask import request
from flaskexample import app
from flaskexample.a_Model import ModelIt
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import numpy as np
import pickle

# connect to Postgres
user = 'bkhurley' #add your Postgres username here      
host = 'localhost'
dbname = 'birth_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database=dbname, user=user)

@app.route('/input')
# def cesareans_input():
def input():
    return render_template("input.html")

@app.route('/output')
def output():
  
  # pull 'data' from input fields and store it
  temp = request.args.get('temperature')
  rain = request.args.get('rain')
  hour = request.args.get('hour')
  day = request.args.get('day')
  month = request.args.get('month')
  station = request.args.get('station')
  direction = request.args.get('direction')

  #Prepare the feature vector for prediction
  pkl_file = open('cat.pkl', 'rb')
  index_dict = pickle.load(pkl_file)
  new_vector = np.zeros(len(index_dict))

  try:
    new_vector[index_dict['mean_temperature']] = temp
  except:
    pass
  try:
    new_vector[index_dict['rain']] = rain
  except:
    pass
  try:
    new_vector[index_dict['hour_'+str(hour)]] = 1
  except:
    pass
  try:
    new_vector[index_dict['day_'+str(day)]] = 1
  except:
    pass
  try:
    new_vector[index_dict['month_'+str(month)]] = 1
  except:
    pass
  try:
    new_vector[index_dict['station_'+str(station)]] = 1
  except:
    pass
  try:
    new_vector[index_dict['direction_'+str(direction)]] = 1
  except:
    pass

  pkl_file = open('rf_reg.pkl', 'rb')
  regmodel = pickle.load(pkl_file)
  prediction = regmodel.predict(new_vector)
  
  return render_template('output.html',prediction=str(np.round(prediction)))  
  