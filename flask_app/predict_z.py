'''
Calculates z-score of predicted crowd level with respect to station mean 
and standard dev.
Raw_predict: predicted # of passengers entering during the hour
station: string of station appbreviation
 '''
import numpy as np
import pandas as pd

def z_calc(raw_predict, station):
    
    # load station stats
    csv_str = '/Users/bkhurley/git/insight/project/beat_the_crowd/data/stn_mean_std.csv'
    station_stats = pd.read_csv(csv_str)
    this_stn = station_stats.loc[station_stats['station'] == station, :]
    
    # calculate z-score and return
    z = np.float((raw_predict - this_stn['mean']) / this_stn['std'])
    return z