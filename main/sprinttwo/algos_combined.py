'''
Combination of three algorithms, two in sprintone and the other in this folder

The class SimplePredict combines the three different functions into one with relative
ease, the __init()__ function is the same and the other three functions can both
be in the class with no troubles.

The function init() runs the three algorithm functions on a certain inputted training
and test database, and puts the output in a third specified database. It creates
three dictionaries with the values from all threes the algorithms for each event and then
adds these values to the database.

Average runtime on Road_Traffic_Fines: 944.043s/15.8min
'''

#Imports all necessary modules
import csv
from csv import reader
from csv import writer
import pandas as pd
import numpy as np
from datetime import datetime
import statistics
from statistics import mode

#Format used for reading the dates
format = '%m/%d/%Y'

#Main class
class SimplePredict:
    #Initialization data
    def __init__(self, data, current_event = "None"):
        self.data = data
        self.current_event = current_event

    def addEventSeq(self, filepath):
        list = []
        listAllSeq = []

        for x in self.data['event_concept:name']:
            if x != "ENDOFTRACE":
                list.append(x)
            else:
                list = []

            listAllSeq.append(list[:])

        self.data['eventSeq'] = listAllSeq
        self.data.to_csv(filepath, index=False)

        return listAllSeq

    def calculate_nextevent(self, list):
        selected_data = self.data[['event_concept:name']]
        all_events = []

        for index, row in self.data.iterrows():
            #print(row['eventSeq'])
            if (row['eventSeq'] == list) and index < len(self.data) - 1:
                next_event = selected_data.at[index+1, 'event_concept:name']
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

    #Second algorithm that calculates the average time between a certain event and the next one
    def calculate_avgtime(self, next_event, list):
        selected_data = self.data[['event_concept:name', 'event_time:timestamp']]
        avg_time = 0
        all_time = []

        #Gets the time between the current specified event and all other following events
        for index, row in self.data.iterrows():
            if index < len(self.data) - 1:
                upcoming_event = selected_data.at[index + 1, 'event_concept:name']
            else:
                upcoming_event = "ENDOFTRACE"

            #Second condition is added to prevent indexOutOfBounds errors
            if (row['eventSeq'] == list) and (upcoming_event == next_event) and index < len(self.data) - 1:
                event_time = selected_data.at[index, 'event_time:timestamp']
                next_time = selected_data.at[index+1, 'event_time:timestamp']
                if not event_time or not next_time or isinstance(event_time, float) or isinstance(next_time, float):
                    time = 0
                else:
                    time = datetime.strptime(next_time, format).timestamp()*1000 - datetime.strptime(event_time, format).timestamp()*1000
                all_time.append(time)

        #Calculates the average time in the set of all durations between the current specified and next event
        avg_time = sum(all_time) / len(all_time)
        avg_time_days = avg_time/86400000
        avg_time_days_round = round(avg_time_days, 0)

        #Printing statements for testing
        #print(all_time)
        #print("The time it takes between " + str(self.current_event) + " and " + next_event + " is on average " + str(avg_time_days_round) + " days")

        #Returns the value to be used later
        return avg_time_days_round

    def addEndOfTrace(self, filepath):
        if "ENDOFTRACE" in self.data.any() == False:
            y = 0
            a = 0

            allCases = self.data['case_concept:name'].unique()

            caseList = self.data['case_concept:name'].values.tolist()
            eventList = self.data['event_concept:name'].values.tolist()
            allList = self.data.values.tolist()

            for x in allCases:
                #temp = next(i for i in reversed(range(len(caseEventList))) if caseEventList[i] == x)
                print(x)
                temp = self.lastOcurring(caseList, x, y, a)
                eventList.insert(temp + 1, "ENDOFTRACE")
                caseList.insert(temp + 1,"ENDOFTRACE")
                allList.insert(temp + 1,["ENDOFTRACE","ENDOFTRACE","ENDOFTRACE","ENDOFTRACE","ENDOFTRACE"])
                y = temp + 1
                a += 10

                #traceTemp = self.data[self.data['case_concept:name'] == x].index.to_numpy()
                #indexTemp = traceTemp[len(traceTemp) - 1] + 1

                #line = pd.DataFrame({"event_concept:name": "ENDOFTRACE"}, index=[indexTemp])
                #data = pd.concat([self.data.iloc[:indexTemp], line,self.data.iloc[indexTemp:]]).reset_index(drop=True)

            #dataTemp = pd.DataFrame(eventList, columns=['event_concept:name'])
            #dataTemp2 = pd.DataFrame(columns=['eventID_','case_concept:name','event_lifecycle:transition','event_time:timestamp'])
            #dataTemp3 = dataTemp.merge(self.data, how='left', left_on='event_concept:name', right_on='eventID_')
            #print(allList)
            self.data = pd.DataFrame(allList, columns=["eventID","case concept:name","event concept:name","event lifecycle:transition","event time:timestamp"])
            self.data.to_csv(filepath, index=False)
            print("Success!")

    def lastOcurring(self, li, x, y, a):
        #z = int(int(len(li)) - 0.90*int(len(li)) + a)
        #if z > len(li):
        #    z = int(len(li))
        #    print("maxZ")

        try:
            for i in reversed(range(y, y + 15)):
                if li[i] == x:
                    return i
        except IndexError:
            for i in reversed(range(y, len(li))):
                if li[i] == x:
                    return i
        raise ValueError("{} is not in list".format(x))

def init():
    #Input for the right results:
    #../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-training.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results.csv
    #../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results.csv

    #Asks for input, then splits the input up in a list with the path to the three datasets separated
    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')

    #Opens the training database with pandas to be used in the algorithms
    with open(chunks[1], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    object = SimplePredict(data)
    object.addEndOfTrace(chunks[1])
    eventSeqTemp2 = object.addEventSeq(chunks[1])

    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    object = SimplePredict(data)
    object.addEndOfTrace(chunks[0])

    eventSeqTemp = object.addEventSeq(chunks[0])
    unique_data = [list(x) for x in set(tuple(x) for x in eventSeqTemp)]

    #Opens the test database file(chunks[1]) and creates or opens a result database file(chunks[2])
    with open(chunks[1], 'r', newline='') as read_obj, open(chunks[2], 'w', newline='') as write_obj:
        #The test database becomes the reader and the result database the writer
        csv_reader = reader(read_obj,delimiter=',')
        csv_writer = writer(write_obj)

        #Dictionaries that are used to add the calculated values to the database
        #Contains values for the top row, since these are not going to be calculated
        timedict = {'event concept:name':'avg time in milliseconds'}
        eventdict = {('eventSeq',):'most occuring next event'}
        eventchancedict = {('eventSeq',):'chance of most occuring next event to take place'}

        for x in unique_data:
            max_event, all_events = object.calculate_nextevent(x)
            y = object.calculate_nexteventchance(max_event, all_events)
            z = object.calculate_avgtime(max_event, x)

            eventdict.update({tuple(x):max_event})
            eventchancedict.update({tuple(x):y})
            timedict.update({tuple(x):z})

        #For every row in the test file two rows are added with the new values
        #The new database with the new rows is written into the result file
        i = -1

        for row in csv_reader:
            if i > -1:
                try:
                    row.append(eventdict[tuple(eventSeqTemp2[i])])
                    row.append(eventchancedict[tuple(eventSeqTemp2[i])])
                    row.append(timedict[tuple(eventSeqTemp2[i])])
                except KeyError:
                    row.append("No Information Available")
            else:
                row.append('most occuring next event in trace')
                row.append('chance of most occuring next event taking place')
                row.append('average time in days')

            if i < len(eventSeqTemp2) - 1:
                i += 1

            csv_writer.writerow(row)

#Runs the program
init()
