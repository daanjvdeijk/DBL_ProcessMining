'''
Algorithm that determines the time between two events

Concept 1: look at the current step n and look at the time difference between current step n and step n+1
Concept 2: Look at the current event and average the time of all the times this event takes.
Preference for second concept as it is easier to add features and improve accuracy.

Elements needed:
1. Method that calculates the average time for all events
2. Method that detect the current event
3. Main method that combines the two; look at the current time and current event, and return the average time for the given event

To find the average time we have to take a few steps:
1. For each current state do the following:
2. Compare the current time x+y with the time x of the next step
3. Add all the values and divide them by the total amount
'''
import csv
import pandas as pd
from datetime import datetime

#Change the quotation to your own directory path
with open('\\YourPath\\BPI_Challenge_2012-test.csv', 'r') as file:
    data = pd.read_csv(file)
    data.columns = ((data.columns.str).replace(" ","_"))


format = '%d-%m-%Y %H:%M:%S.%f'

class SimpleTimePredict:

    def __init__(self, data, current_event):
        self.data = data
        self.current_event = current_event

    def calculate_avgtime(self):
        selected_data = data[['event_concept:name', 'event_time:timestamp']]
        avg_time = 0
        all_time = []

        for index, row in data.iterrows():
            if (row['event_concept:name'] == self.current_event):
                event_time = selected_data.at[index, 'event_time:timestamp']
                prev_time = selected_data.at[index-1, 'event_time:timestamp']
                time = datetime.strptime(event_time, format).timestamp()*1000 - datetime.strptime(prev_time, format).timestamp()*1000
                all_time.append(time)

        avg_time = sum(all_time) / len(all_time)
        print(all_time)
        print("Event " + str(self.current_event) + " takes on average " + str(avg_time) + " milliseconds")

    def return_event(self):
        print("The current event is " + str(self.current_event))

object = SimpleTimePredict(data, 'A_PREACCEPTED')
object.calculate_avgtime()