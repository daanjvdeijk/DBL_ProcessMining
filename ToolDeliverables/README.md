# DBL_ProcessMining_Group 2
This code has been created for the course DBL Process Mining.
For the course we need to create a tool to analyse company process data to predict when and what event occurs next.

## How to run the train/test split tool (optional)
1. Run train-test-split.exe and insert the filepath(s) to all the database(s) q that have to be merged into a train and test split. This can be any amount of .csv files. Make sure to separate the different filepaths with spaces. 
2. The tool outputs two databases called 'testDataCorrected.csv' and 'trainingDataCorrected.csv' in the folder that the tool was ran on. These can be loaded in to the prediction tool.
 
## How to run the prediction tool
1. Run main.py and insert the filepath to the train and test data, with an optional third argument for the results, as follows: path/to/train.csv path/to/test.csv path/to/results.csv
2. Main.py will run all algorithms in order and output the current task it is performing. Wait untill the terminal indicates that the tool has finished before opening the results csv file. Do not exit the tool whilst it is running. This will result in all data being lost.

### Features
* Our tool consists of 3 different algorithms. A baseline algorithm:
    1. A baseline algorithm with predicts the time and event based on the average of the values.
    2. A sequence algorithm, which uses the previous events from the same sequence to predict the next likely event and the average time for the same sequences.
    3. A combined algorithm which uses clustering for the time untill the next event and a neural network to predict the next event based on the prevous two in the same sequence.
* The results file will consists of the provided test file with added columns for each individual prediction for time and next event.
* We have supplied 3 pre-sorted train-test splits, as well as a small version of every training set. These can be used to quickly check how the algorithm runs. The results of these small training databases are not representative of the accuracy of the algorithms.

### Commands
A list of commands that will work with the presupplied databases:

* Small training database versions:
    * databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results-small.csv
    * databases/BPI_Challenge_2012/BPI_Challenge_2012-small.csv /databases/BPI_Challenge_2012/BPI_Challenge_2012-test.csv databases/BPI_Challenge_2012/BPI_Challenge_2012-results-small.csv
    * databases/BPI_Challenge_2017/BPI_Challenge_2017-small.csv databases/BPI_Challenge_2017/BPI_Challenge_2017-test.csv databases/BPI_Challenge_2017/BPI_Challenge_2017-results-small.csv
* Full training database version:
    * databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-training.csv databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-test.csv databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-results.csv
    * databases/BPI_Challenge_2012/BPI_Challenge_2012-training.csv databases/BPI_Challenge_2012/BPI_Challenge_2012-test.csv databases/BPI_Challenge_2012/BPI_Challenge_2012-results.csv
    * databases/BPI_Challenge_2017/BPI_Challenge_2017-training.csv databases/BPI_Challenge_2017/BPI_Challenge_2017-test.csv databases/BPI_Challenge_2017/BPI_Challenge_2017-results.csv
