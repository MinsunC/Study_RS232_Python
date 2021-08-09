import pandas
import os
from os.path import basename

loglist = "I:\CPA_result_1.xlsx"

result = []
buffer = []
stepTime = []
cycleTime = 0
blank = []
prevTime = 0
check = 0
count = 0

df = pandas.read_excel(loglist)

for row_index, row in df.iterrows():
    if row["step"] != 0 and row["cycle"] == 0 and check == 1:
        stepTime.append(row["step"])
        continue
    if row["step"] != 0 and row["cycle"] != 0:
        if stepTime:
            buffer.append(prevTime)
            for i in range(len(stepTime)):
                buffer.append(stepTime[i])
            buffer.append(row["step"])
            buffer.append(cycleTime)
            result.append(buffer)
            buffer = []
            stepTime = []
            check = 0
        check = 1
        stepTime.append(row["step"])
        cycleTime = row["cycle"]
        prevTime = row["time"]    
        continue
    

fn = os.path.splitext(loglist)

df2 = pandas.DataFrame(result)
with pandas.ExcelWriter(fn[0] + "_rev" + ".xlsx") as writer:
    df2.to_excel(writer, index=False)