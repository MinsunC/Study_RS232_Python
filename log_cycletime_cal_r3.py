import numpy
import pandas
import csv
import os
from os.path import basename

startIndex = 0
cycleIndex = 0
movingTime = 0
cycleTime = 0
check = 0
cycle = 0
cal = 0
ALDcheck = 0

loglist = "I:\CPA_210701.xlsx"

df = pandas.read_excel(loglist)

for row_index, row in df.iterrows():
    if row_index == 0:
        continue
    if row["Target pos"] == 100:
        startIndex = 0
        cycleIndex = 0
        movingTime = 0
        cycleTime = 0
        check = 0
        cycle = 0
        cal = 0
        ALDcheck = 0
    if row["Pos"] != df.loc[row_index-1, "Pos"] and check == 0:
        startIndex = row_index-1
        check = 1
        if df.loc[row_index-1, "Pos"] == 10:
            if row["Target pos"] == 60:
                cycleTime = row["Time"] - df.loc[cycleIndex, "Time"]
                df.loc[cycleIndex, "Cycle time"] = cycleTime
                cycleIndex = row_index-1

    if row["Target pos"] == row["Pos"] and check == 1:
        if df.loc[startIndex, "Pos"] == row["Target pos"]:
            movingTime = 0
            check = 0
            continue
        movingTime = row["Time"] - df.loc[startIndex, "Time"]
        df.loc[startIndex, "Moving time"] = movingTime
        movingTime = 0
        check = 0

fn = os.path.splitext(loglist)

with pandas.ExcelWriter(fn[0] + "_rev" + ".xlsx") as writer:
    df.to_excel(writer, index=False)
