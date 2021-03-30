'''
Combination of three algorithms, two in sprintone and the other in this folder

The class SimplePredict combines the three different functions into one with relative
ease, the __init()__ function is the same and the other three functions can both
be in the class with no troubles.

The function init() runs the three algorithm functions on a certain inputted training
and test database, and puts the output in a third specified database. It creates
three dictionaries with the values from all threes the algorithms for each event and then
adds these values to the database.

Average runtime on Road_Traffic_Fines: >24 hours
'''

#Imports all necessary modules
from csv import reader
from csv import writer
import pandas as pd
from datetime import datetime
import statistics
from dateutil import parser
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import pairwise_distances
import sys

#Main class
class SimplePredict:
    #Initialization data
    def __init__(self, data, current_event = "None"):
        self.data = data
        self.data['event_time:timestamp'] = pd.to_datetime(self.data['event_time:timestamp'])
        self.data = data.sort_values(['case_concept:name', 'event_time:timestamp'], ascending = [True, True])
        self.current_event = current_event
        self.selected_data = self.data[['event_concept:name', 'event_time:timestamp']].values.tolist()

    #First algorithm that calculates the most occuring event after the current event
    def calculate_nextevent_Baseline(self):
        all_events = []

        #Gets all events in the database which follow on the specified event
        for index, row in self.data.iterrows():
            #Second condition is added to prevent indexOutOfBounds errors
            if row['event_concept:name'] == self.current_event and index < len(self.data) - 1:
                next_event = self.selected_data[index+1][0]
                all_events.append(next_event)

        #Takes the most occuring event out of the list of next_events
        try:
            max_event = statistics.mode(all_events)
        except:
            max_event = 0

        #Printing statements for testing
        #print(all_events)
        #print("Event " + str(self.current_event) + " is most often followed by " + str(max_event))

        #Returns the value to be used later
        return max_event

    #Second algorithm that calculates the average time between a certain event and the next one
    def calculate_avgtime_Baseline(self, next_event):
        avg_time = 0
        all_time = []

        #Gets the time between the current specified event and all other following events
        for index, row in self.data.iterrows():
            if index < len(self.data) - 1:
                upcoming_event = self.selected_data[index + 1][0]
            else:
                upcoming_event = "A_ACCEPTED"

            #Second condition is added to prevent indexOutOfBounds errors
            if (row['event_concept:name'] == self.current_event) and (upcoming_event == next_event) and index < len(self.data) - 1:
                if not isinstance(self.selected_data[index][1], datetime) or not isinstance(self.selected_data[index + 1][1], datetime):
                    event_time = parser.parse(self.selected_data[index][1])
                    next_time = parser.parse(self.selected_data[index + 1][1])
                else:
                    event_time = self.selected_data[index][1]
                    next_time = self.selected_data[index + 1][1]

                #Hardcoded exception for when one of the two values that is being compared is ENDOFTRACE
                if event_time == pd.Timestamp.max or next_time == pd.Timestamp.max or isinstance(event_time, float) or isinstance(next_time, float):
                    time = 0
                else:
                    time = next_time.timestamp()*1000 - event_time.timestamp()*1000

                all_time.append(time)

        #Calculates the average time in the set of all durations between the current specified and next event
        try:
            avg_time = sum(all_time) / len(all_time)
        except ZeroDivisionError:
            avg_time = 0
        #Printing statements for testing
        #print(all_time)
        #print("The time it takes between " + str(self.current_event) + " and " + next_event + " is on average " + str(avg_time_days) + " days")

        #Returns the value to be used later
        return avg_time

    #Functions that adds a row after the end of every trace to prevent the last and first event of two
    #different traces being compared
    def addEndOfTrace(self, filepath, datasetType):
        if "ENDOFTRACE" not in self.data.values:
            #Iterable variable being used in the for loop
            y = 0

            #Four lists that are used in the calculations
            allCases = self.data['case_concept:name'].unique()
            caseList = self.data['case_concept:name'].values.tolist()
            allList = self.data.values.tolist()

            #For loop that goes over every case
            for index, x in enumerate(allCases):
                print("Preparing " + datasetType +  " dataset (1/2): " + str(index + 1) + "/" + str(len(allCases)), end="\r")

                #Location of the last occuring event is searched
                temp = self.lastOcurring(caseList, x, y)

                insertTemp = []
                for z in self.data.columns.tolist():
                    if z == "case_concept:name":
                        insertTemp.append(x)
                    elif z == "event_time:timestamp":
                        insertTemp.append(pd.Timestamp.max)
                    else:
                        insertTemp.append("ENDOFTRACE")

                #ENDOFTRACE is added after the location of the last event
                caseList.insert(temp + 1,"ENDOFTRACE")
                allList.insert(temp + 1, insertTemp)

                #Updates the iterable to the value after the last-added ENDOFTRACE
                y = temp + 1

            #Gets column names in the dataframe
            cols = self.data.columns.tolist()

            print(" ")
            #Updates self.data and writes the new dataframe to the specified filepath
            self.data = pd.DataFrame(allList, columns=cols)
            self.data.to_csv(filepath, index=False)

    #Function that adds a temporary column to a specified file which stores all events
    #in a trace up until a certain point. This column is removed at the end
    def addEventSeq(self, filepath, datasetType = "This shouldn't show up"):
        #Lists used in the function
        list = []
        listAllSeq = []

        #Adds events up to and including the current event to a list and appends
        #it to a list which contains all traces. Resets when it sees ENDOFTRACE
        for index, x in enumerate(self.data['event_concept:name']):
            print("Preparing " + datasetType +  " dataset (2/2): " + str(index + 1) + "/" + str(len(self.data['event_concept:name'])), end="\r")

            if x == "ENDOFTRACE":
                list = []
            elif pd.isnull(x):
                list = []
            else:
                list.append(x)

            listAllSeq.append(list[:])

        #Writes new column to file
        self.data['eventSeq'] = listAllSeq
        self.data.to_csv(filepath, index=False)

        #Returns the list with all traces for later use
        return listAllSeq

    #Updated function that calculates the next event based on the current trace
    def calculate_nextevent_EventSeq(self, list):
        #Lists used in the function
        all_events = []

        #Looks up all next events for a certain trace and adds them to all_events
        for index, row in self.data.iterrows():
            if row['eventSeq'] == str(list) and index < len(self.data) - 1:
                next_event = self.selected_data[index + 1][0]
                all_events.append(next_event)

        #Takes the most occuring next event
        try:
            max_event = statistics.mode(all_events)
        except:
            max_event = 0

        #Prints which event takes place most often after the specified trace
        #print(str(max_event) + " is the event that most often takes place after ")
        #print(list)

        #Returns both the most occuring and all next events for later use
        return max_event, all_events

    #Second algorithm that calculates the average time between a certain event and the next one
    def calculate_avgtime_EventSeq(self, next_event, list):
        #Lists used in the function
        avg_time = 0
        all_time = []

        #Gets the time between the current specified event trace and all other following events
        for index, row in self.data.iterrows():
            if index < len(self.data) - 1:
                upcoming_event = self.selected_data[index + 1][0]
            else:
                upcoming_event = "ENDOFTRACE"

            #Third condition is added to prevent indexOutOfBounds errors
            if (row['eventSeq'] == list) and (str(upcoming_event) == next_event) and index < len(self.data) - 1:
                event_time = self.selected_data[index][1]
                next_time = self.selected_data[index + 1][1]

                #Hardcoded exception for when one of the two values that is being compared is ENDOFTRACE
                if event_time == "ENDOFTRACE" or next_time == "ENDOFTRACE" or isinstance(event_time, float) or isinstance(next_time, float) or pd.isnull(event_time) or pd.isnull(next_time):
                    time = 0
                else:
                    time = next_time.timestamp()*1000 - event_time.timestamp()*1000

                all_time.append(time)

        #Calculates the average time in the set of all durations between the current specified and next event
        try:
            avg_time = sum(all_time) / len(all_time)
        except ZeroDivisionError:
            avg_time = 0

        #Prints the value
        #print("The time it takes between the event trace and " + next_event + " is on average " + str(avg_time) + " milliseconds")
        #print(' ')

        #Returns the value to be used later
        return avg_time

    #Supplementary function for addEndOfTrace()
    #Finds the index of the last event in the trace
    def lastOcurring(self, li, x, y):
        try:
            #Since no trace is longer than 15 events, only the next 15 events are
            #checked. This massively reduces the runtime
            for i in reversed(range(y, y + 150)):
                #print(li[i])

                if li[i] == x:
                    return i

        #Catches IndexErrors if the last event is not in the range, this happens for the last trace
        except IndexError:
            for i in reversed(range(y, len(li))):
                if li[i] == x:
                    return i

    def addClusteringColumns(self, filepath, current_event, next_event):
        #Lists used in this functions
        totalTimeList = []
        timeTillNextEvent = []

        #Adds events up to and including the current event to a list and appends
        #it to a list which contains all traces. Resets when it sees ENDOFTRACE
        for index, row in self.data.iterrows():
            try:
                if self.selected_data[index][0] == "ENDOFTRACE" or self.selected_data[index + 1][0] == "ENDOFTRACE":
                    totalTimeList.append(None)
                    timeTillNextEvent.append(None)
                elif pd.isnull(self.selected_data[index][0]) or pd.isnull(self.selected_data[index + 1][0]):
                    totalTimeList.append(None)
                    timeTillNextEvent.append(None)
                elif self.selected_data[index][0] == current_event:
                    totalTimeList.append(self.selected_data[index][1].timestamp()*1000)

                    if next_event == self.selected_data[index + 1][0]:
                        timeTillNextEvent.append(self.selected_data[index + 1][1].timestamp()*1000 - self.selected_data[index][1].timestamp()*1000)
                    else:
                        timeTillNextEvent.append(None)
                else:
                    totalTimeList.append(None)
                    timeTillNextEvent.append(None)
            except IndexError:
                totalTimeList.append(None)
                timeTillNextEvent.append(None)

        #Writes new column to file
        self.data['total_time:timestamp'] = totalTimeList
        self.data['time_till_next_event:timestamp'] = timeTillNextEvent
        self.data.to_csv(filepath, index=False)

    #Second algorithm that calculates the average time between a certain event and the next one
    def calculate_avgtime_Clustering(self):
        try:
            selected_data_clustering = self.data[['total_time:timestamp', 'time_till_next_event:timestamp',]].dropna()

            n_clusters_range = [2,3,4,5,6,7,8,9,10]
            n_clusters_range_silhouetteScore = {}

            for x in n_clusters_range:
                kmeans = KMeans(n_clusters=x).fit(selected_data_clustering)
                n_clusters_range_silhouetteScore[x] = metrics.silhouette_score(selected_data_clustering, kmeans.labels_, sample_size = 1000)

            #print(max(n_clusters_range_silhouetteScore, key=n_clusters_range_silhouetteScore.get))
            kmeans = KMeans(n_clusters = max(n_clusters_range_silhouetteScore, key=n_clusters_range_silhouetteScore.get)).fit(selected_data_clustering)
            cluster_means = kmeans.cluster_centers_.ravel()

            cluster_means_all = []
            for x in range(1, len(cluster_means), 2):
                cluster_means_all.append(cluster_means[x])

            avg_time = statistics.mean(cluster_means_all)

            #print("The average time is " + str(avg_time) + " milliseconds")

        except ValueError:
            avg_time = 0

        print(avg_time)
        return avg_time

def init():
    #Input for the right results:
    #../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv ../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results-small.csv
    #../../databases/BPI_Challenge_2012/BPI_Challenge_2012-test.csv ../../databases/BPI_Challenge_2012/BPI_Challenge_2012-test.csv ../../databases/BPI_Challenge_2012/BPI_Challenge_2012-results-small.csv
    #../../databases/BPI_Challenge_2017/BPI_Challenge_2017-test.csv ../../databases/BPI_Challenge_2017/BPI_Challenge_2017-test.csv ../../databases/BPI_Challenge_2017/BPI_Challenge_2017-results-small.csv

    #Asks for input, then splits the input up in a list with the path to the three datasets separated
    temp = input("Please enter a training set, a test set and a result file location: ")
    chunks = temp.split(' ')
    print(" ")

    #Opens the test set with pandas
    with open(chunks[1], 'r') as file:
        data = pd.read_csv(file)
        data.columns = ((data.columns.str).replace(" ","_"))

    #Adds ENDOFTRACE and the eventseq to the test set
    object = SimplePredict(data)
    object.addEndOfTrace(chunks[1], "test")
    eventSeqTempTest = object.addEventSeq(chunks[1], "test")

    print("\n ")

    #Opens the training set with pandas to be used in later algorithms
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file, low_memory=True)
        data.columns = ((data.columns.str).replace(" ","_"))

    #Adds ENDOFTRACE and the eventseq to the training set
    object = SimplePredict(data)
    object.addEndOfTrace(chunks[0], "training")
    eventSeqTempTraining = object.addEventSeq(chunks[0], "training")
    print("\n")

    #Opens the training set with pandas to be used in later algorithms
    with open(chunks[0], 'r') as file:
        data = pd.read_csv(file, low_memory=True)
        data.columns = ((data.columns.str).replace(" ","_"))
    object = SimplePredict(data)

    #Finds all unique event sequences in the training set
    unique_data = [list(x) for x in set(tuple(x) for x in eventSeqTempTraining)]

    #Opens the test database file(chunks[1]) and creates or opens a result database file(chunks[2])
    with open(chunks[1], 'r', newline='') as read_obj, open(chunks[2], 'w', newline='') as write_obj:
        #The test database becomes the reader and the result database the writer
        csv_reader = reader(read_obj,delimiter=',')
        csv_writer = writer(write_obj)

        #Dictionaries for the baseline that are used to add the calculated values to the database
        #Contains values for the top row, since these are not going to be calculated
        timedictBaseline = {'event concept:name':'avg time in milliseconds'}
        eventdictBaseline = {'event concept:name':'most occuring next event'}

        #Dictionaries for the eventseq-temp algorithm that are used to add the calculated values to the database
        timedictEventSeq = {'event concept:name':'avg time in milliseconds'}
        eventdictEventSeq = {'eventSeq':'most occuring next event'}

        #Dictionaries for the eventseq-temp algorithm that are used to add the calculated values to the database
        timedictClustering = {('event concept:name', 'cluster_labels:name'):'avg time in milliseconds'}
        #eventdictBaseline = {'eventSeq':'most occuring next event'}

        #For every unique possible event the two algorithms are ran (BASELINE)
        for x in data['event_concept:name'].unique():
            print("BASELINE event " + str(np.where(data['event_concept:name'].unique() == x)[0][0] + 1) + " out of " + str(len(data['event_concept:name'].unique())))
            object = SimplePredict(data, x)

            eventdictBaseline.update({x:object.calculate_nextevent_Baseline()})
            timedictBaseline.update({x:object.calculate_avgtime_Baseline(eventdictBaseline[x])})

        '''
        print(" ")
        #Runs the algorithms for every unique event sequence and adds their result to a dictionary (EVENTSEQ)
        for x in unique_data:
            print("EVENTSEQ event " + str(unique_data.index(x) + 1) + " out of " + str(len(unique_data)))

            max_event, all_events = object.calculate_nextevent_EventSeq(x)
            z = object.calculate_avgtime_EventSeq(max_event, x)

            eventdictEventSeq.update({tuple(x):max_event})
            timedictEventSeq.update({tuple(x):z})
        '''

        print(" ")
        #For every unique possible event the two algorithms are ran (CLUSTERING)
        for x in data['event_concept:name'].unique():
            print("CLUSTERING event " + str(np.where(data['event_concept:name'].unique() == x)[0][0] + 1) + " out of " + str(len(data['event_concept:name'].unique())))

            object = SimplePredict(data, x)
            next_event = object.calculate_nextevent_Baseline()
            eventdictBaseline.update({x:next_event})

            object.addClusteringColumns(chunks[0], x, next_event)
            timedictClustering.update({x:object.calculate_avgtime_Clustering()})

        #Iterable variable that is used in the for loop for indexing
        i = -1

        #For every row in the test file two rows are added with the new values
        #The new database with the new rows is written into the result file
        for row in csv_reader:
            #Skips the first row since it contains column names and not values
            if i > -1:
                try:
                    row.append(eventdictBaseline[row[data.columns.get_loc("event_concept:name")]])
                    row.append(timedictBaseline[row[data.columns.get_loc("event_concept:name")]])
                except KeyError:
                    row.append("No Information Available (BASELINE)")
                    row.append("No Information Available (BASELINE)")

                '''
                try:
                    row.append(eventdictEventSeq[tuple(eventSeqTempTest[i])])
                    row.append(timedictEventSeq[tuple(eventSeqTempTest[i])])

                #If there is no existing trace in the dictionary there is no information available
                except KeyError:
                    row.append("No Information Available (EVENTSEQ)")
                    row.append("No Information Available (EVENTSEQ)")
                '''

                try:
                    row.append(eventdictBaseline[row[data.columns.get_loc("event_concept:name")]])
                    row.append(timedictClustering[row[data.columns.get_loc("event_concept:name")]])
                #If there is no existing trace in the dictionary there is no information available
                except KeyError:
                    row.append("No Information Available (CLUSTERING)")
                    row.append("No Information Available (CLUSTERING)")
            #Manually put in column names
            else:
                row.append('most occuring next event in trace (BASELINE)')
                row.append('average time in milliseconds (BASELINE)')
                '''
                row.append('most occuring next event in trace (EVENTSEQ)')
                row.append('average time in milliseconds (EVENTSEQ)')
                '''
                row.append('most occuring next event in trace (CLUSTERING)')
                row.append('average time in milliseconds (CLUSTERING)')

            #Updates the iterable variable
            if i < len(eventSeqTempTest) - 1:
                i += 1

            #Deletes the event sequence row since it isn't supposed to be in the end result
            #Since 3 rows are appended after we can always locate it's position regardless of the dataset
            del row[len(row) - 7]

            #Writes the new rows to the file
            csv_writer.writerow(row)

#Runs the program
init()
