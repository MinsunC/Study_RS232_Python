import serial
import time
from tkinter import *
from tkinter import messagebox

cycle = 0
targetcycle = 0
getcycle = 0
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
        global targetcycle

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

        self.command11 = Label(window, text="Command 1")
        self.command11.grid(row=40, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command1 = Entry(window)
        self.command1.grid(row=40, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command21 = Label(window, text="Command 2")
        self.command21.grid(row=50, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command2 = Entry(window)
        self.command2.grid(row=50, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command31 = Label(window, text="Command 3")
        self.command31.grid(row=60, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command3 = Entry(window)
        self.command3.grid(row=60, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command41 = Label(window, text="Command 4")
        self.command41.grid(row=70, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command4 = Entry(window)
        self.command4.grid(row=70, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.command51 = Label(window, text="Command 5")
        self.command51.grid(row=80, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        self.command5 = Entry(window)
        self.command5.grid(row=80, column=1, padx=2, pady=2, ipadx=2, ipady=2)

        self.text3 = Label(window, text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
        self.text3.grid(row=90, column=0, padx=1, pady=1, ipadx=1, ipady=1, columnspan=2)

        self.text4 = Label(window, text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
        self.text4.grid(row=91, column=0, padx=1, pady=1, ipadx=1, ipady=1, columnspan=2)

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
        global targetcycle
        global window2
        global textbox
        global comportnumber
        global delay
        global exitcondition

        i = 0
        cycle = 0
        targetcycle = 0
        window2 = 0
        textbox = 0
        delay = 0
        self.text3.config(text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
        self.text4.config(text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
        window.update()

        exitcondition = False

    def close(self):
        global exitcondition

        exitcondition = True

    def startcycle(self):
        global cycle
        global getcycle
        global targetcycle
        global tail
        global delay
        global i
        global cl
        global exitcondition
        global set1activate
        starttriger = 1

        try:
            inputentry = [self.command1, self.command2, self.command3, self.command4, self.command5]
            command = []

            getcycle = str(self.cyclenumber.get())
            delay = str(self.delaytime.get())

            targetcycle = int(getcycle)
            if targetcycle == 0:
                self.text4.config(text="Target cycle: X")
                window.update()
            else:
                self.text4.config(text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
                window.update()

            for k in range(len(inputentry)):
                j = str(inputentry[k].get()).upper()
                if j:
                    command.append(j)

            # start 조건: 처리할 수 없는 명령어.... 들어오면 어쩔까
            # if

            if starttriger == 1:
                window4 = Toplevel(window)
                window4.title("Warning")
                warn4 = Label(window4, text="아직 지원하지 않는 명령어 입니다.")
                warn4.pack()
            else:
                cycle = int(getcycle)
                if cycle == 0:
                    while True:
                        if exitcondition:
                            ser.write(cl.encode('ascii'))
                            break

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
                        except AttributeError:
                            pass
                        i += 1
                        self.text3.config(text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
                        window.update()

                else:
                    while i < cycle:
                        if exitcondition:
                            ser.write(cl.encode('ascii'))
                            break

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
                        except AttributeError:
                            pass

                        i += 1
                        self.text3.config(text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
                        window.update()

                        if i == targetcycle:
                            window5 = Toplevel(window)
                            window5.title("Finish")
                            warn5 = Label(window5, text="Cycle 종료.")
                            warn5.pack()

        except:
            window6 = Toplevel(window)
            window6.title("Warning")
            warn6 = Label(window6, text="필요 parameter들을 입력 해주세요.")
            warn6.pack()

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

            self.button1.configure(text='COM'+comportnumber+" connected")
            self.endtoplevel(window2)
        except:
            self.button1.configure(text="No connection")
            window2.destroy()

            window3 = Toplevel(window)
            window3.title("Warning")
            warn3 = Label(window3, text="해당 comport와 연결된 device가 없습니다.")
            warn3.pack()

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

        if self.button1["text"] != "Input comport number":
            try:
                ser.close()
            except AttributeError:
                pass
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
except AttributeError:
    pass
