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
window3 = 0
columnlists = []
columnlists2 = []
columnlists3 = []
listdf = []
df = 0
listbox = 0
listbox2 = 0
interval = 0

pandas.options.display.float_format = '{:.3f}'.format


class LogFilter:
    global loglists

    def __init__(self):
        global window
        global columnlists

        window = Tk()
        window.resizable(False, False)
        window.title("Log Filter")

        # 초기 화면 구성
        self.buttonreset = Button(window, text="Reset", command=lambda: self.reset())
        self.buttonreset.grid(row=0, column=0, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)

        self.button1 = Button(window, text="Selection: Log files", command=lambda: self.logfiles())
        self.button1.grid(row=1, column=0, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)

        self.button2 = Button(window, text="Selection: Save directory", command=lambda: self.savedir())
        self.button2.grid(row=10, column=0, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)

        self.explain1 = Label(window, text="원하는 column만 남기기")
        self.explain1.grid(row=11, column=0, padx=2, pady=2, ipadx=2, ipady=2)

        self.button3 = Button(window, text="Select columns want to remain", command=lambda: self.selectcolumn(1))
        self.button3.grid(row=20, column=0, padx=2, pady=2, ipadx=2, ipady=2)

        self.button4 = Button(window, text="Start", command=lambda: self.startfilter(columnlists))
        self.button4.grid(row=30, column=0, padx=2, pady=2, ipadx=2, ipady=2)

        self.explain2 = Label(window, text="Cycle data\n원하는 column cycle수에 따라 정리")
        self.explain2.grid(row=11, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.button5 = Button(window, text="Select a column want to save", command=lambda: self.selectcolumn(2))
        self.button5.grid(row=20, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.button6 = Button(window, text="Start", command=lambda: self.startcyclearrange(columnlists2, columnlists3))
        self.button6.grid(row=30, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        window.mainloop()

    def reset(self):
        global loglists
        global savedirectory
        global columnlists
        global columnlists2
        global columnlists3
        global df
        global listbox
        global listbox2
        global interval

        # reset 필요한 변수들 초기화
        loglists = []
        savedirectory = 0
        columnlists = []
        columnlists2 = []
        columnlists3 = []
        df = 0
        listbox = 0
        listbox2 = 0
        interval = 0

        self.button1.config(text="Selection: Log files")
        self.button2.config(text="Selection: Save directory")
        self.button3.config(text="Select columns want to remain")
        self.button4.config(text="Start")
        self.button5.config(text="Select a column want to save")
        self.button6.config(text="Start")

    def logfiles(self):
        global loglists
        global df
        global columnlists
        global listdf
        buffer = []
        abc = []

        try:
            # Log files 선택 창
            loglists = filedialog.askopenfilenames(initialdir="D:\\", title="Choose your file")
            self.button1.configure(text="The number of selected files: " + str(len(loglists)))

            # 선택한 파일들 확장자에 따라 적절한 상태로 구분
            for loglist in loglists:
                df = []
                fileext = os.path.splitext(loglist)[1]
                if fileext == '.xls' or fileext == '.xlsx':
                    df = pandas.read_excel(loglist)
                else:
                    # excel 파일 아닐 경우
                    with open(loglist, 'rt', encoding='UTF-8') as f:
                        for line in f:
                            line_list = line.replace(';', ' ').replace(',', ' ').split()
                            # 의미있는 data가 아닌 행 필터링
                            if len(line_list) < 3:
                                continue
                            buffer.append(line_list)

                    # Log에 기록된 날짜와 시간이 나뉠 경우 처리
                    # 첫 행의 label도 data와 시간으로 나눠준다
                    if len(buffer[0]) != len(buffer[1]):
                        abc.append('Date')
                        abc.append('Time')
                        for i in range(len(buffer[0])-1):
                            abc.append(buffer[0][i+1])
                        buffer[0] = abc

                    # list의 각 요소들 string으로 변환
                    for i in range(len(buffer)-1):
                        try:
                            buffer[i+1] = list(map(str, buffer[i+1]))
                        except ValueError:
                            continue
                    df = pandas.DataFrame(data=buffer[1:], columns=buffer[0])

                # listdf의 요소에 각 log file의 data 추가
                listdf.append(df)
                abc = []
                buffer = []

            # columnlists가 비어있으면 log의 label 추가
            if not columnlists:
                columnlists = list(df)

        except FileNotFoundError:
            self.button1.configure(text="No file")

    # 저장 위치 설정
    def savedir(self):
        global savedirectory

        savedirectory = filedialog.askdirectory(title="Choose file directory for saving files")
        self.button2.configure(text=str(savedirectory))

    # Column list에서 원하는 column만 남기기
    def deletecolumns(self):
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

    # cycle filtering 위한 parameter 값 받아오기
    def choosecolumn(self):
        global window
        global window3
        global loglists
        global columnlists
        global columnlists2
        global listbox
        global listbox2
        global listdf

        window3 = Toplevel(window)
        window3.resizable(False, False)
        window3.title("Choose column")

        scrollbar = Scrollbar(window3)
        scrollbar.grid(row=0, column=1, padx=7, pady=7, rowspan=4, ipadx=3, ipady=3)

        listbox = Listbox(window3, yscrollcommand=scrollbar.set, selectmode="single")

        for i in range(len(columnlists)):
            listbox.insert(END, columnlists[i])

        listbox.grid(row=0, column=0, padx=7, pady=7, ipadx=3, ipady=3)
        scrollbar.config(command=listbox.yview)

        self.explain = Label(window3, text="Data interval(ms)")
        self.explain.grid(row=8, column=0, columnspan=2, padx=2, pady=2, ipadx=3, ipady=3)

        self.command = Entry(window3)
        self.command.grid(row=9, column=0, columnspan=2, padx=2, pady=2, ipadx=3, ipady=3)

        self.buttonselect1 = Button(window3, text="Select column\nrepresent process step", command=lambda: self.selectlist())
        self.buttonselect1.grid(row=10, column=0, columnspan=2, padx=7, pady=7, ipadx=3, ipady=3)

        buttonselect2 = Button(window3, text="Select column to remain\n and finish", command=lambda: self.selectlist2())
        buttonselect2.grid(row=20, column=0, columnspan=2,  padx=7, pady=7, ipadx=3, ipady=3)

    def endtoplevel(self, win):
        win.destroy()
        self.button3.configure(text="Columns are selected")

    def selectlist(self):
        global columnlists
        global columnlists3
        global listbox

        columnlists3_temp = list(listbox.curselection())
        columnlists3 = columnlists[columnlists3_temp[0]]
        self.buttonselect1.configure(text=columnlists3)

    def selectlist2(self):
        global columnlists
        global columnlists2
        global listbox
        global interval

        interval = int(self.command.get())
        columnlists2_temp = list(listbox.curselection())
        columnlists2 = columnlists[columnlists2_temp[0]]
        if len(columnlists2) == 0:
            window4 = Toplevel(window)
            window4.title("Warning")
            warn = Label(window4, text="Column을 선택해 주세요.")
            warn.pack()
        else:
            self.endtoplevel(window3)

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

    def selectcolumn(self, mode):
        global loglists

        if mode == 1:
            self.button3.configure(text="Please wait")
            self.deletecolumns()
        elif mode == 2:
            self.button5.configure(text="Please wait")
            self.choosecolumn()

    def startfilter(self, col):
        global loglists
        global savedirectory
        global listdf

        for temp in range(len(loglists)):
            select_df = listdf[temp][col]

            logname = os.path.basename(loglists[temp])
            fn = os.path.splitext(logname)

            # select_df.to_csv(savedirectory + fn[0] + "_filtering" + ".csv", index=False, float_format='%3f')
            select_df.to_csv(savedirectory + "\\" + fn[0] + ".csv", index=False, float_format='%3f')
        self.button4.configure(text="Finish")

    def startcyclearrange(self, col, stepcol):
        global loglists
        global savedirectory
        global listdf
        global interval

        print(col)
        for temp in range(len(loglists)):
            tempdf = listdf[temp]
            previousstep = 1
            cyclecount = 0
            cycle = []
            steps = []
            steps_buffer = []
            columndata = []
            columndata_buffer = []
            j = 0
            index1 = []

            for row in range(tempdf.shape[0]):
                if j == 0:
                    if tempdf[stepcol][row] == 1:
                        j = 1
                    continue

                if tempdf[stepcol][row] == 1 and tempdf[stepcol][row] != previousstep:
                    cyclecount += 1
                    cycle.append(cyclecount)
                    columndata.append(columndata_buffer)
                    columndata_buffer = []
                    steps_buffer = []

                columndata_buffer.append(tempdf[col][row])
                previousstep = tempdf[stepcol][row]

            cyclecount += 1
            cycle.append(cyclecount)
            columndata.append(columndata_buffer)
            columndataT = [[element for element in t] for t in zip(*columndata)]
            cycle_df = pandas.DataFrame(data=columndataT, columns=cycle)
            for i in range(cycle_df.shape[0]):
                index1.append(i * interval)
            cycle_df.index = index1
            logname = os.path.basename(loglists[temp])
            fn = os.path.splitext(logname)

            # cycle_df.to_csv(savedirectory + fn[0] + "_filtering" + ".csv", float_format='%3f')
            cycle_df.to_csv(savedirectory + "\\" + fn[0] + ".csv", float_format='%3f')
        self.button6.configure(text="Finish")


a = LogFilter()
