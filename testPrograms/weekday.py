import csv
from csv import reader
from csv import writer
import pandas as pd
from datetime import datetime
import statistics
from statistics import mode

filepath = "../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv"
data = pd.read_csv(filepath)

format = '%m/%d/%Y'

class SimplePredict:

    #Initialization data
    def __init__(self, data, current_event = "none"):
        self.data = data
        self.current_event = current_event

    def addDayOfWeek(self):
        try:
            self.data['weekday']
        except KeyError:
            selected_data = self.data[['event_concept:name', 'event_time:timestamp']]
            weekDaysStr = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
            dayOfWeek = []

            for index, row in self.data.iterrows():
                if selected_data.at[index, 'event_time:timestamp'] != "ENDOFTRACE":
                    date = datetime.strptime(selected_data.at[index, 'event_time:timestamp'], format)
                    weekdayInt = date.date().weekday()
                    dayOfWeek.append(weekDaysStr[weekdayInt])
                else:
                    dayOfWeek.append("ENDOFTRACE")

            self.data['weekday'] = dayOfWeek
            self.data.to_csv("weekday.csv", index=False)

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
        #print(all_events)
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

                #Hardcoded exception for when one of the two values that is being compared is ENDOFTRACE
                if event_time == "ENDOFTRACE" or next_time == "ENDOFTRACE":
                    time = 0
                else:
                    time = datetime.strptime(next_time, format).timestamp()*1000 - datetime.strptime(event_time, format).timestamp()*1000

                all_time.append(time)

        #Calculates the average time in the set of all durations between the current specified and next event
        avg_time = sum(all_time) / len(all_time)

        #Printing statements for testing
        #print(all_time)
        print("The time it takes between " + str(self.current_event) + " and " + next_event + " is on average " + str(avg_time) + " milliseconds")

        #Returns the value to be used later
        return avg_time

    def findFreeDays(self):
        #monday, tuesday, wednesday, thursday, friday, saturday, sunday = 0
        weekdayOccuranceDict = {"Monday":0, "Tuesday":0, "Wednesday":0, "Thursday":0, "Friday":0, "Saturday":0, "Sunday":0}

        for x in self.data['weekday']:
            if x != "ENDOFTRACE":
                weekdayOccuranceDict[x] += 1

        for x in self.data["event concept:name"].unique():

        print(weekdayOccuranceDict)

def init():
    #Input for the right results:
    #../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv ../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv ../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results-small.csv
    #../databases\Road_Traffic_Fines\Road_Traffic_Fine_Management_Process-training.csv ../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv ../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results-small2.csv

    #Asks for input, then splits the input up in a list with the path to the three datasets separated
    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')

    #Opens the training database with pandas to be used in the algorithms
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    object = SimplePredict(data)
    object.addDayOfWeek()
    object.findFreeDays()

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
            try:
                row.append(eventdict[row[4]])
                row.append(timedict[row[4]])
            except KeyError:
                row.append("No information available")
                row.append("No information available")
            csv_writer.writerow(row)

init()
