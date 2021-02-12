import csv
from csv import reader
from csv import writer
import pandas as pd
from datetime import datetime
import statistics
from statistics import mode

format = '%d-%m-%Y %H:%M:%S.%f'

class SimplePredict:

    def __init__(self, data, current_event):
        self.data = data
        self.current_event = current_event

    def calculate_nextevent(self):
        selected_data = self.data[['event_concept:name']]
        all_events = []

        for index, row in self.data.iterrows():
            if row['event_concept:name'] == self.current_event and index < len(self.data) - 1:
                next_event = selected_data.at[index+1, 'event_concept:name']
                all_events.append(next_event)

        max_event = mode(all_events)

        #print(all_events)
        print("Event " + str(self.current_event) + " is most often followed by " + str(max_event))
        return max_event

    def calculate_avgtime(self):
        selected_data = self.data[['event_concept:name', 'event_time:timestamp']]
        avg_time = 0
        all_time = []

        for index, row in self.data.iterrows():
            if (row['event_concept:name'] == self.current_event) and index > 1:
                event_time = selected_data.at[index, 'event_time:timestamp']
                prev_time = selected_data.at[index-1, 'event_time:timestamp']
                time = datetime.strptime(event_time, format).timestamp()*1000 - datetime.strptime(prev_time, format).timestamp()*1000
                all_time.append(time)

        avg_time = sum(all_time) / len(all_time)
        #print(all_time)
        print("Event " + str(self.current_event) + " takes on average " + str(avg_time) + " milliseconds")
        return avg_time

    def return_event(self):
        print("The current event is " + str(self.current_event))

def init():
    #BPI_Challenge_2012-training.csv BPI_Challenge_2012-test.csv BPI_Challenge_2012-results.csv

    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')
    print(chunks)

    #Change the quotation to your own directory path
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    with open(chunks[1], 'r', newline='') as read_obj, open(chunks[2], 'w', newline='') as write_obj:
        csv_reader = reader(read_obj,delimiter=',')
        csv_writer = writer(write_obj)
        timedict = {'event concept:name':'avg time in milliseconds'}
        eventdict = {'event concept:name':'most occuring next event'}

        for x in data['event_concept:name'].unique():
            object = SimplePredict(data, x)
            eventdict.update({x:object.calculate_nextevent()})
            timedict.update({x:object.calculate_avgtime()})

        for row in csv_reader:
            row.append(eventdict[row[4]])
            row.append(timedict[row[4]])
            csv_writer.writerow(row)

init()
