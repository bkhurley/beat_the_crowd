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

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                                       
                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean';          
                """
    query_results = pd.read_sql_query(sql_query,con)
    births = ""
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births

@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
    return render_template('cesareans.html',births=births)

@app.route('/input')
def cesareans_input():
    return render_template("input.html")

@app.route('/output')
def cesareans_output():
  # get feature names
  # feat_names = ['mean_temperature', 'rain', 'hour_0', 'hour_1', 
  # 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 
  # 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_2', 'hour_20', 'hour_21', 
  # 'hour_22', 'hour_23', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 
  # 'hour_8', 'hour_9', 'direction_northbound', 'direction_southbound',
  # 'station_12TH', 'station_16TH', 'station_19TH', 'station_24TH',
  # 'station_BALB', 'station_CIVC', 'station_COLM', 'station_CONC',
  # 'station_DALY', 'station_EMBR', 'station_GLEN', 'station_LAFY',
  # 'station_MCAR', 'station_MONT', 'station_NCON', 'station_ORIN',
  # 'station_PHIL', 'station_POWL', 'station_ROCK', 'station_SBRN',
  # 'station_SFIA', 'station_SSAN', 'station_WCRK', 'station_WOAK',
  # 'day_Friday', 'day_Monday', 'day_Saturday', 'day_Sunday',
  # 'day_Thursday', 'day_Tuesday', 'day_Wednesday', 'month_1', 'month_10',
  # 'month_11', 'month_12', 'month_2', 'month_3', 'month_4', 'month_5',
  # 'month_6', 'month_7', 'month_8', 'month_9']
  # feature_names = pd.Series(feat_names)
  # # initialize feature vector
  # X = np.zeros(len(feature_names))

  #pull 'data' from input fields and store it
  #result = request.form

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

  pkl_file = open('lm.pkl', 'rb')
  regmodel = pickle.load(pkl_file)
  prediction = regmodel.predict(new_vector)
  
  return render_template('output.html',prediction=str(np.round(prediction)))  
  #X =  np.zeros(71) # 71 features

  # transform inputs into a feature vector that we can pass into the regression model


  #the_result = [temp, rain, hour, day, month, station, direction]
  #return render_template("output.html", the_result = the_result)
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
  # query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
  # print(query)
  # query_results=pd.read_sql_query(query,con)
  # print(query_results)
  # births = []
  # for i in range(0,query_results.shape[0]):
  #     births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
  #     the_result = ''
  #     the_result = ModelIt(patient,births)
  #     return render_template("output.html", births = births, the_result = the_result)