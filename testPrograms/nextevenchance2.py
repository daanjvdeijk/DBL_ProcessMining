import statistics
from statistics import mode
import csv
from csv import reader
from csv import writer
import pandas as pd

class SimplePredict:
    #Initialization data
    def __init__(self, data, current_event = "none"):
        self.data = data
        self.current_event = current_event

    def addEventSeq(self):
        list = []
        listAllSeq = []

        for x in data['eventID']:
            if x != "ENDOFCASE":
                list.append(x)
            else:
                list = []

            listAllSeq.append(list[:])

        data['eventSeq'] = listAllSeq
        data.to_csv("nexteventchance.csv", index=False)

        return listAllSeq

    def calculate_nextevent(self, list):
        selected_data = data[['eventID']]
        all_events = []

        for index, row in data.iterrows():
            #print(row['eventSeq'])
            if (row['eventSeq'] == list) and index < len(self.data) - 1:
                next_event = selected_data.at[index+1, 'eventID']
                all_events.append(next_event)

        max_event = mode(all_events)

        #print(all_events)
        print(str(max_event) + " is the event that most often takes place after ")
        print(list)

        return max_event, all_events

    def calculate_nexteventchance(self, max_event, all_events):
        percentageOccurring = all_events.count(max_event)/len(all_events) * 100
        percentageOccurringRound = round(percentageOccurring, 2)

        print("The chance of event " + str(mode(all_events)) + " to occur next is: " + str(percentageOccurringRound) + "%")
        print(' ')

        return percentageOccurring

with open('nexteventchance.csv', newline='') as csv_file:
    data = pd.read_csv(csv_file)
    csv_writer = writer(csv_file)
    csv_reader = reader(csv_file,delimiter=',')

    object = SimplePredict(data)
    temp = object.addEventSeq()

    eventdict = {'eventID':'most occuring next event'}
    eventchancedict = {'eventID':'chance of most occuring next event to take place'}

    unique_data = [list(x) for x in set(tuple(x) for x in temp)]

    for x in unique_data:
        temptemp, temptemptemp = object.calculate_nextevent(x)
        y = object.calculate_nexteventchance(temptemp, temptemptemp)

        eventdict.update({tuple(x):temptemp})
        eventchancedict.update({tuple(x):y})

    for row in csv_reader:
        print(x)
        row.append(eventdict[row[1]])
        row.append(eventchancedict[row[1]])
        csv_writer.writerow(row)
