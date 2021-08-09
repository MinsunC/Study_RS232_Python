import openpyxl
import numpy
import pandas
import csv
import os
from tkinter import *
from tkinter import filedialog
from os.path import basename

buffer = []

with open("I:\PythonCode\\W09_ALL", 'r') as f:
    for line in f:
        line_list = line.replace(';', ' ').replace(',', ' ').split()
        if len(line_list) < 2:
            continue
        buffer.append(line_list)

df = pandas.DataFrame(data=buffer[1:], columns=buffer[0])

print(df)

buffer = []