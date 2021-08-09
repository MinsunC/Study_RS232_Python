import serial
import time
from tkinter import *
from tkinter import messagebox

cycle = 0
tail = '\r\n'
cl = 'C' + tail
ser = 0
window = 0
window2 = 0
textbox = 0
comportnumber = 0
delay = 0
i = 0
set1activate = 'D1'
exitcondition = False


class SerialCommunication:
    global cycle
    global tail
    global ser

    def __init__(self):
        global window
        global i

        window = Tk()
        # window.geometry("640x400+200+200")
        window.title("Serial Communication")
        window.resizable(False, False)

        self.button1 = Button(window, text="Input comport number", command=lambda: self.inputcomport())
        self.button1.grid(row=0, column=0, padx=2, pady=2, columnspan=2, ipadx=2, ipady=2)

        self.cyclenumber1 = Label(window, text="Cycle")
        self.cyclenumber1.grid(row=10, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.cyclenumber = Entry(window)
        self.cyclenumber.grid(row=10, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.caution = Label(window, text="(0: stop 누를 때까지 계속 반복)")
        self.caution.grid(row=11, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        self.delaytime1 = Label(window, text="Delay(ms)")
        self.delaytime1.grid(row=20, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.delaytime = Entry(window)
        self.delaytime.grid(row=20, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.caution = Label(window, text="* 명령어 List\nopen: O\nclose: C\nPos.제어: 숫자로 입력")
        self.caution.grid(row=30, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        self.command11 = Label(window, text="command1")
        self.command11.grid(row=40, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command1 = Entry(window)
        self.command1.grid(row=40, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command21 = Label(window, text="command2")
        self.command21.grid(row=50, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command2 = Entry(window)
        self.command2.grid(row=50, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command31 = Label(window, text="command3")
        self.command31.grid(row=60, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command3 = Entry(window)
        self.command3.grid(row=60, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command41 = Label(window, text="command4")
        self.command41.grid(row=70, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command4 = Entry(window)
        self.command4.grid(row=70, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command51 = Label(window, text="command5")
        self.command51.grid(row=80, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command5 = Entry(window)
        self.command5.grid(row=80, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.text3 = Label(window, text="Current cycle: " + str(i))
        self.text3.grid(row=90, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        self.button2 = Button(window, text="Start cycle", command=lambda: self.startcycle())
        self.button2.grid(row=100, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        self.exit = Button(window, text="Stop cycle", command=lambda: self.close())
        self.exit.grid(row=110, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        self.reset = Button(window, text="Reset", command=lambda: self.resetcycle())
        self.reset.grid(row=120, column=0, padx=2, pady=2, ipadx=2, ipady=2, columnspan=2)

        window.mainloop()

    def resetcycle(self):
        global i
        global cycle

        i = 0
        cycle = 0
        self.text3.config(text="Current cycle: " + str(i))
        window.update()

    def close(self):
        global exitcondition

        exitcondition = True

    def startcycle(self):
        global cycle
        global tail
        global delay
        global i
        global cl
        global exitcondition
        global set1activate

        inputentry = [self.command1, self.command2, self.command3, self.command4, self.command5]
        command = []

        cycle = str(self.cyclenumber.get())
        delay = str(self.delaytime.get())

        for k in range(5):
            j = str(inputentry[k].get()).upper()
            if j:
                command.append(j)

        cycle = int(cycle)
        if cycle == 0:
            while True:
                try:
                    for m in range(len(command)):
                        if command[m] == 'C' or command[m] == 'O':
                            buffer = command[m] + tail
                            ser.write(buffer.encode('ascii'))
                        else:
                            buffer = 'S1' + command[m] + tail
                            ser.write(buffer.encode('ascii'))
                            buffer2 = set1activate + tail
                            ser.write(buffer2.encode('ascii'))
                        time.sleep(int(delay) / 1000)
                except:
                    pass
                i += 1
                self.text3.config(text="Current cycle: " + str(i))
                window.update()

                if exitcondition:
                    ser.write(cl.encode('ascii'))
                    break

        else:
            while i < cycle:
                try:
                    for m in range(len(command)):
                        if command[m] == 'C' or command[m] == 'O':
                            buffer = command[m] + tail
                            ser.write(buffer.encode('ascii'))
                        else:
                            buffer = 'S1' + command[m] + tail
                            ser.write(buffer.encode('ascii'))
                            buffer2 = set1activate + tail
                            ser.write(buffer2.encode('ascii'))
                        time.sleep(int(delay) / 1000)
                except:
                    pass

                i += 1
                self.text3.config(text="Current cycle: " + str(i))
                window.update()

                if exitcondition:
                    ser.write(cl.encode('ascii'))
                    break

    def getcomport(self):
        global textbox
        global window2
        global comportnumber
        global ser

        comportnumber = str(textbox.get())

        try:
            ser = serial.Serial(
                port='COM'+comportnumber,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0
            )

            # self.button1.configure(text=ser.portstr)
            self.button1.configure(text='COM'+comportnumber+"connected")
            self.endtoplevel(window2)
        except:
            # self.button1.configure(text=ser.portstr)
            ser.close()
            self.button1.configure(text="No connection")
            window2.destroy()

    def endtoplevel(self, win):
        global cl
        cl = 'C' + tail
        ser.write(cl.encode('ascii'))

        win.destroy()

    def inputcomport(self):
        global ser
        global window
        global textbox
        global comportnumber
        global window2

        window2 = Toplevel(window)
        window2.title("Comport number")

        text = Label(window2, text="Comport")
        text.grid(row=0, column=0)
        textbox = Entry(window2)
        textbox.grid(row=0, column=1)

        getcomport = Button(window2, text="OK", command=lambda: self.getcomport())
        getcomport.grid(row=1, column=1)


SerialCommunication()
try:
    cl = 'C' + tail
    ser.write(cl.encode('ascii'))
    ser.close()
except:
    ser.close()
