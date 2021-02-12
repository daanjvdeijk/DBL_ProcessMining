'''
Combination of two algorithms in other two files in this folder

The class SimplePredict combines the two different classes into one with relative
ease, the __init()__ function is the same and the other two functions can both
be in the class with no troubles.

The function init() runs the two algorithm functions on a certain inputted training
and test database, and puts the output in a third specified database. It creates
two dictionaries with the values from both the algorithms for each event and then
adds these values to the database.

Average runtime: 876.418s/14.6min
'''

#Imports all necessary modules
import csv
from csv import reader
from csv import writer
import pandas as pd
from datetime import datetime
import statistics
from statistics import mode

#Format used for reading the dates
format = '%d-%m-%Y %H:%M:%S.%f'

#Main class
class SimplePredict:
    #Initialization data
    def __init__(self, data, current_event):
        self.data = data
        self.current_event = current_event

    #First algorithm that calculates the most occuring event after the current event
    def calculate_nextevent(self):
        selected_data = self.data[['event_concept:name']]
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
        print(all_events)
        print("Event " + str(self.current_event) + " is most often followed by " + str(max_event))

        #Returns the value to be used later
        return max_event

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

        #Printing statements for testing
        #print(all_time)
        print("The time it takes between " + str(self.current_event) + " and " + next_event + " is on average " + str(avg_time) + " milliseconds")

        #Returns the value to be used later
        return avg_time

def init():
    #Input for the right results:
    #../databases/BPI_Challenge_2012-training.csv ../databases/BPI_Challenge_2012-test.csv ../databases/BPI_Challenge_2012-results.csv

    #Asks for input, then splits the input up in a list with the path to the three datasets separated
    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')
    print(chunks)

    #Opens the training database with pandas to be used in the algorithms
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    #Opens the test database file(chunks[1]) and creates or opens a result database file(chunks[2])
    with open(chunks[1], 'r', newline='') as read_obj, open(chunks[2], 'w', newline='') as write_obj:
        #The test database becomes the reader and the result database the writer
        csv_reader = reader(read_obj,delimiter=',')
        csv_writer = writer(write_obj)

        #Dictionaries that are used to add the calculated values to the database
        #Contains values for the top row, since these are not going to be calculated
        timedict = {'event concept:name':'avg time in milliseconds'}
        eventdict = {'event concept:name':'most occuring next event'}

        #For every unique possible event the two algorithms are ran
        for x in data['event_concept:name'].unique():
            object = SimplePredict(data, x)
            eventdict.update({x:object.calculate_nextevent()})
            timedict.update({x:object.calculate_avgtime(eventdict[x])})

        #For every row in the test file two rows are added with the new values
        #The new database with the new rows is written into the result file
        for row in csv_reader:
            row.append(eventdict[row[4]])
            row.append(timedict[row[4]])
            csv_writer.writerow(row)

#Runs the program
init()
