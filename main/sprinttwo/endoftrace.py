import csv
import pandas as pd

filepath = "../../databases/Road_Traffic_Fines/Road_Traffic_Fine_Management_Process-small.csv"
data = pd.read_csv(filepath)

if data.isnull().values.any() == False:
    for x in data['case concept:name'].unique():
        traceTemp = data[data['case concept:name'] == x].index.to_numpy()
        indexTemp = traceTemp[len(traceTemp) - 1] + 1
        print(indexTemp)

        line = pd.DataFrame({"event concept:name": "ENDOFTRACE"}, index=[indexTemp])
        data = pd.concat([data.iloc[:indexTemp], line, data.iloc[indexTemp:]]).reset_index(drop=True)

    data.to_csv(filepath)
