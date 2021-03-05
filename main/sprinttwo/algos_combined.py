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

    #First algorithm that calculates the most occuring event after the current event
    def calculate_nextevent(self):
        selected_data = self.data[['event_concept:name']]
        global all_events
        all_events = []

        #Gets all events in the database which follow on the specified event
        for index, row in self.data.iterrows():
            #Second condition is added to prevent indexOutOfBounds errors
            if row['event_concept:name'] == self.current_event and index < len(self.data) - 1:
                next_event = selected_data.at[index+1, 'event_concept:name']
                all_events.append(next_event)

        #Takes the most occuring event out of the list of next_events
        max_event = mode(all_events)

        #Printing statements for testing
        #print(all_events)
        print("Event " + str(self.current_event) + " is most often followed by " + str(max_event))

        #Returns the value to be used later
        return max_event

    #Calculates the percentage chance of an occurance of the mode event
    def calculate_nexteventchance(self):
        modeEvent = mode(all_events)
        percentageOccurring = all_events.count(modeEvent)/len(all_events) * 100
        percentageOccurringRound = round(percentageOccurring, 2)

        print("The chance of event " + str(mode(all_events)) + " to occur next is: " + str(percentageOccurringRound) + "%")

        return percentageOccurringRound

    #Second algorithm that calculates the average time between a certain event and the next one
    def calculate_avgtime(self, next_event):
        selected_data = self.data[['event_concept:name', 'event_time:timestamp']]
        avg_time = 0
        all_time = []

        #Gets the time between the current specified event and all other following events
        for index, row in self.data.iterrows():
            if index < len(self.data) - 1:
                upcoming_event = selected_data.at[index + 1, 'event_concept:name']
            else:
                upcoming_event = "A_ACCEPTED"

            #Second condition is added to prevent indexOutOfBounds errors
            if (row['event_concept:name'] == self.current_event) and (upcoming_event == next_event) and index < len(self.data) - 1:
                event_time = selected_data.at[index, 'event_time:timestamp']
                next_time = selected_data.at[index+1, 'event_time:timestamp']
                time = datetime.strptime(next_time, format).timestamp()*1000 - datetime.strptime(event_time, format).timestamp()*1000
                all_time.append(time)

        #Calculates the average time in the set of all durations between the current specified and next event
        avg_time = sum(all_time) / len(all_time)
        avg_time_days = avg_time/86400000
        avg_time_days_round = round(avg_time_days, 0)

        #Printing statements for testing
        #print(all_time)
        print("The time it takes between " + str(self.current_event) + " and " + next_event + " is on average " + str(avg_time_days_round) + " days")

        #Returns the value to be used later
        return avg_time_days_round

    def addEndOfTrace(self, filepath):
        if self.data[['event_concept:name','event_concept:name']].isnull().values.any() == False:
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
            self.data = pd.DataFrame(allList)
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

    #Asks for input, then splits the input up in a list with the path to the three datasets separated
    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')

    #Opens the training database with pandas to be used in the algorithms
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    object = SimplePredict(data)
    print(chunks[0])
    object.addEndOfTrace(chunks[0])


    #Opens the test database file(chunks[1]) and creates or opens a result database file(chunks[2])
    with open(chunks[1], 'r', newline='') as read_obj, open(chunks[2], 'w', newline='') as write_obj:
        #The test database becomes the reader and the result database the writer
        csv_reader = reader(read_obj,delimiter=',')
        csv_writer = writer(write_obj)

        #Dictionaries that are used to add the calculated values to the database
        #Contains values for the top row, since these are not going to be calculated
        timedict = {'event concept:name':'avg time in milliseconds'}
        eventdict = {'event concept:name':'most occuring next event'}
        eventchancedict = {'event concept:name':'chance of most occuring next event to take place'}

        #For every unique possible event the two algorithms are ran
        for x in data['event_concept:name'].unique():
            object = SimplePredict(data, x)
            eventdict.update({x:object.calculate_nextevent()})
            eventchancedict.update({x:object.calculate_nexteventchance()})
            timedict.update({x:object.calculate_avgtime(eventdict[x])})

        #For every row in the test file two rows are added with the new values
        #The new database with the new rows is written into the result file
        for row in csv_reader:
            row.append(eventdict[row[2]])
            row.append(eventchancedict[row[2]])
            row.append(timedict[row[2]])
            csv_writer.writerow(row)

#Runs the program
init()
