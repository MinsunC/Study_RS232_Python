import openpyxl
import numpy
import pandas
import csv
import os
from tkinter import *
from tkinter import filedialog
from os.path import basename

loglists = []
savedirectory = 0
window = 0
window2 = 0
columnlists = []
df = 0
listbox = 0

pandas.options.display.float_format = '{:.3f}'.format


class LogFilter:
    global loglists

    def __init__(self):
        global window
        global columnlists

        window = Tk()
        window.resizable(False, False)
        window.title("Log Filter")

        self.button1 = Button(window, text="Selection: Log files", command=lambda: self.logfiles())
        self.button1.grid(row=0, column=0, padx=17, pady=7, ipadx=3, ipady=3)

        self.button2 = Button(window, text="Selection: Save directory", command=lambda: self.savedir())
        self.button2.grid(row=10, column=0, padx=17, pady=7, ipadx=3, ipady=3)

        self.button3 = Button(window, text="Select column", command=lambda: self.selectcolumn())
        self.button3.grid(row=20, column=0, padx=17, pady=7, ipadx=3, ipady=3)

        self.button4 = Button(window, text="Start data filtering", command=lambda: self.startfilter(columnlists))
        self.button4.grid(row=30, column=0, padx=17, pady=7, ipadx=3, ipady=3)

        window.mainloop()

    def logfiles(self):
        global loglists
        global df
        global columnlists
        buffer = []
        abc = []

        try:
            if loglists:
                self.button1.configure(text="Selection: Log files")
                self.button2.configure(text="Selection: Save directory")
                self.button3.configure(text="Select column")
                self.button4.configure(text="Start data filtering")

            loglists = filedialog.askopenfilename(initialdir="C:/", title="Choose your file")
            self.button1.configure(text=str(loglists))

            fileext = os.path.splitext(loglists)[1]
            if fileext == '.xls' or fileext == '.xlsx':
                df = pandas.read_excel(loglists)
            else:
                with open(loglists, 'r') as f:
                    for line in f:
                        line_list = line.replace(';', ' ').replace(',', ' ').split()
                        if len(line_list) < 2:
                            continue
                        buffer.append(line_list)

                if len(buffer[0]) != len(buffer[1]):
                    abc.append('Date')
                    abc.append('Time')
                    for i in range(len(buffer[0])-1):
                        abc.append(buffer[0][i+1])
                    buffer[0] = abc

                for i in range(len(buffer)-1):
                    try:
                        buffer[i+1] = list(map(str, buffer[i+1]))
                    except ValueError:
                        continue
                df = pandas.DataFrame(data=buffer[1:], columns=buffer[0])
            abc = []
            buffer = []
            columnlists = list(df)
        except FileNotFoundError:
            self.button1.configure(text="No file")

    def savedir(self):
        global savedirectory

        savedirectory = filedialog.askdirectory(title="Choose file directory for saving files")
        self.button2.configure(text=str(savedirectory))

    def columnname(self):
        global window
        global window2
        global loglists
        global columnlists
        global listbox
        global df

        window2 = Toplevel(window)
        window2.resizable(False, False)
        window2.title("Choose column")

        scrollbar = Scrollbar(window2)
        scrollbar.grid(row=0, column=1, padx=7, pady=7, rowspan=4, ipadx=3, ipady=3)

        listbox = Listbox(window2, yscrollcommand=scrollbar.set, selectmode="extended")

        for i in range(len(columnlists)):
            listbox.insert(END, columnlists[i])

        listbox.grid(row=0, column=0, padx=7, pady=7, ipadx=3, ipady=3)
        scrollbar.config(command=listbox.yview)

        buttondel = Button(window2, text="Delete selected items", command=lambda: self.deletelists())
        buttondel.grid(row=10, column=0, padx=7, pady=7, ipadx=3, ipady=3)

        buttonquit = Button(window2, text="Finish", command=lambda: self.endtoplevel(window2))
        buttonquit.grid(row=20, column=0, padx=7, pady=7, ipadx=3, ipady=3)

    def endtoplevel(self, win):
        win.destroy()
        self.button3.configure(text="Columns are selected")

    def deletelists(self):
        global columnlists
        global listbox

        selection = listbox.curselection()
        if len(selection) == 0:
            return

        for i in range(len(selection)):
            value = listbox.get(selection[0])
            ind = columnlists.index(value)
            del columnlists[ind]
            listbox.delete(selection[0])

    def selectcolumn(self):
        global loglists

        self.button3.configure(text="Please wait")
        self.columnname()

    def startfilter(self, col):
        global loglists
        global savedirectory
        global df

        # print(col)
        # temp3 = list(set(list(df)) - set(col))
        # for element in temp3:
        #     df = df.drop(element, axis=1)

        select_df = df[col]

        logname = os.path.basename(loglists)
        fn = os.path.splitext(logname)

        # select_df.to_excel(savedirectory + fn[0] + "_filtering" + ".xlsx", index=False)
        select_df.to_csv(savedirectory + fn[0] + "_filtering" + ".csv", index=False, float_format='%3f')
        self.button4.configure(text="Finish")


a = LogFilter()
