import csv
import pandas as pd
from datetime import datetime
import statistics
from statistics import mode

#Change the quotation to your own directory path
with open('../databases/BPI_Challenge_2012-test.csv', 'r') as file:
    data = pd.read_csv(file)
    data.columns = ((data.columns.str).replace(" ","_"))


class SimpleEventPredict:

    def __init__(self, data, current_event):
        self.data = data
        self.current_event = current_event

    def calculate_nextevent(self):
        selected_data = data[['event_concept:name']]
        all_events = []

        for index, row in data.iterrows():
            if (row['event_concept:name'] == self.current_event):
                next_event = selected_data.at[index+1, 'event_concept:name']
                all_events.append(next_event)

        max_event = mode(all_events)

        #print(all_events)
        print(str(max_event) + " is the event that most often takes place after " + str(self.current_event))


    def return_event(self):
        print("The current event is " + str(self.current_event))

object = SimpleEventPredict(data, 'A_PARTLYSUBMITTED')
object.calculate_nextevent()
