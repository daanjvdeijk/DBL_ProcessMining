# DBL_ProcessMining_Group 2
This code has been created for the course DBL Process Mining.
For the course we need to create a tool to analyse company process data to predict when and what event occurs next.

## How to run the visualization tool
1. When provided with a single dataset, insert this dataset in the split_train_test.py.
2. Run main.py and insert the path to the train and test data, with an optional third argument for the results, as follows: path/to/train.csv path/to/test.csv path/to/results.csv
3. main.py will run all algorithms in order and output the current task it is performing. Wait till the terminal indicates that the tool has finished before opening the results csv file.

### Features
* Our tool consists of 3 different algorithms. A baseline algorithm:
    1. A baseline algorithm with predicts the time and event based on the average of the values.
    2. A sequence algorithm, which uses the previous events from the same sequence to predict the next likely event and the average time for the same sequences.
    3. A combined algorithm which uses clustering for the time till the next event and a neural network to predict the next event based on the prevous two in the same sequence.
* The results file will consists of the original (test??) file with added columns for each individual prediction for time and next event.
