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

        self.button1 = Button(window, text="Input comport number", command=lambda: self.inputcomport())
        self.button1.grid(row=0, column=1)

        self.cyclenumber1 = Label(window, text="Cycle\n(0: stop 누를 때까지 계속 반복)")
        self.cyclenumber1.grid(row=2, column=0)
        self.cyclenumber = Entry(window)
        self.cyclenumber.grid(row=2, column=1)

        self.delaytime1 = Label(window, text="Delay(ms)\n")
        self.delaytime1.grid(row=3, column=0)
        self.delaytime = Entry(window)
        self.delaytime.grid(row=3, column=1)

        self.command11 = Label(window, text="command1\n")
        self.command11.grid(row=4, column=0)
        self.command1 = Entry(window)
        self.command1.grid(row=4, column=1)

        self.command21 = Label(window, text="command2\n")
        self.command21.grid(row=5, column=0)
        self.command2 = Entry(window)
        self.command2.grid(row=5, column=1)

        self.command31 = Label(window, text="command3\n")
        self.command31.grid(row=6, column=0)
        self.command3 = Entry(window)
        self.command3.grid(row=6, column=1)

        self.command41 = Label(window, text="command4\n")
        self.command41.grid(row=7, column=0)
        self.command4 = Entry(window)
        self.command4.grid(row=7, column=1)

        self.command51 = Label(window, text="command5\n")
        self.command51.grid(row=8, column=0)
        self.command5 = Entry(window)
        self.command5.grid(row=8, column=1)

        self.text3 = Label(window, text="Current cycle: " + str(i))
        self.text3.grid(row=9, column=0)

        self.button2 = Button(window, text="Start cycle", command=lambda: self.startcycle())
        self.button2.grid(row=10, column=1)

        self.exit = Button(window, text="Stop cycle", command=lambda: self.close())
        self.exit.grid(row=11, column=1)

        self.reset = Button(window, text="Reset", command=lambda: self.resetcycle())
        self.reset.grid(row=12, column=1)

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

        inputentry = [self.command1, self.command2, self.command3, self.command4, self.command5]
        command = []

        cycle = str(self.cyclenumber.get())
        delay = str(self.delaytime.get())

        for k in range(5):
            j = str(inputentry[k].get())
            if j:
                command.append(j)

        cycle = int(cycle)
        if cycle == 0:
            while True:
                print(i)
                for m in range(len(command)):
                    buffer = command[m] + tail
                    ser.write(buffer.encode('ascii'))
                    time.sleep(int(delay)/1000)
                i += 1
                self.text3.config(text="Current cycle: " + str(i))
                window.update()

                if exitcondition:
                    ser.write(cl.encode('ascii'))
                    break

        else:
            while i < cycle:
                print(i)
                for m in range(len(command)):
                    buffer = command[m] + tail
                    ser.write(buffer.encode('ascii'))
                    time.sleep(int(delay)/1000)
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
            self.button1.configure(text="No connection")
            self.endtoplevel(window2)

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
cl = 'C' + tail
ser.write(cl.encode('ascii'))
ser.close()
