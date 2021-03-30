all_traces_val = []
eventSeqTempTraining = [[1], [1, 2], [1, 2, 3], []]

for index, x in enumerate(eventSeqTempTraining):
    if index == len(eventSeqTempTraining) - 1:
        all_traces_val.insert(index, ["ENDOFTRACE"])
    else:
        try:
            all_traces_val.insert(index, [eventSeqTempTraining[index+1][-1]])
        except IndexError:
            all_traces_val.insert(index, ["ENDOFTRACE"])

print(all_traces_val)
