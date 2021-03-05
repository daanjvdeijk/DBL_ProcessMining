# %%
#This algorithm adapt the base database to add two columns:
# 1. Transforms the timestamp from string to an integer
# 2. Adds the total runtime of the current event in selected unit
#
#Change the directory path to the correct csv file (sometimes has to be entire path)
#Change the value of time_type to the unit of your choice
#Change the file name of the result at the bottom by changing the variable

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
from datetime import datetime

# %%
# Open CSV file to calculate time difference
with open('...\\Road_Traffic_Fine_Management_Process-training.csv', 'r') as file:
    data = pd.read_csv(file)
    #Replaces spaces with underscore, as python has a hard time working with spaces
    data.columns = ((data.columns.str).replace(" ","_"))

#select the unit of time needed milliseconds MS, seconds S and days D
time_type = 'D'
#Add new row with duration of event and sort the data based on the cases
data["total_time"] = 0
data['time_in_timestamp_' + time_type] = 0
data_sorted = data.sort_values(by=['eventID_']).reset_index(drop=True)
#format for datetime
format = '%d-%m-%Y %H:%M:%S.%f'


#%%
for index, row in data.iterrows():
    if  index < len(data) - 1:
        #Take the current timestamp and the timestamp of the next event
        event_time = data_sorted.at[index, 'event_time:timestamp']
        next_time = data_sorted.at[index+1, 'event_time:timestamp']
        #Select the time unit (MS, S or D)
        if time_type == 'MS':
            #Convert the current event to integer
            current_time = datetime.strptime(event_time, format).timestamp()*1000
            #Calculate the total duration of the current event
            time = datetime.strptime(next_time, format).timestamp()*1000 - current_time
        elif time_type == 'S':
            current_time = datetime.strptime(event_time, format).timestamp()
            time = datetime.strptime(next_time, format).timestamp() - current_time
        elif time_type == 'D':
            current_time = datetime.strptime(event_time, format).timestamp()/86400
            time = datetime.strptime(next_time, format).timestamp()/86400 - current_time
        rounded_time = round(time)
        #Insert the value in the dataframe
        data_sorted['total_time'].loc[index] = rounded_time
        data_sorted['time_in_timestamp_'+ time_type].loc[index] = current_time

# %%
#Export the dataframe to csv
#It is possible to change the name by changing the variable
data_sorted.to_csv('event_time_italy.csv')

# %%