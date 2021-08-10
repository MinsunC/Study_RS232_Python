import serial
import time
from tkinter import *

# check 해보자
# git 기능 익히기
# Test 2

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
set1poscontrol = 'T10'
exitcondition = False
possiblecommand = ['O', 'C']
starttriger = 0
sendcommand = 0
textIndex = 0


class SerialCommunication:
    global cycle
    global tail
    global ser

    def __init__(self):
        global window
        global i
        global targetcycle

        # 초기 pop-up창 구성
        window = Tk()
        # window.geometry("640x400+200+200")
        window.title("Serial Communication")
        window.resizable(False, False)

        # Comport 번호 입력 창
        # inputcomport
        self.button1 = Button(window, text="Input comport number", command=lambda: self.inputcomport())
        self.button1.grid(row=0, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Commnad 입력창 띄우는 button
        self.button2 = Button(window, text="단일 command 입력", command=lambda: self.commandwindow())
        self.button2.grid(row=1, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # 구분선
        self.divide = Label(window, text="-------------------------------\n Cycle test")
        self.divide.grid(row=2, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Cycle 횟수 입력
        self.cyclenumber1 = Label(window, text="Cycle")
        self.cyclenumber1.grid(row=10, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.cyclenumber = Entry(window)
        self.cyclenumber.grid(row=10, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Cycle 입력 값 관련 설명
        self.caution = Label(window, text="(0: stop 누를 때까지 계속 반복)")
        self.caution.grid(row=11, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Sequence 명령어 사이 interval 입력
        self.delaytime1 = Label(window, text="Delay(ms)")
        self.delaytime1.grid(row=20, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.delaytime = Entry(window)
        self.delaytime.grid(row=20, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Sequence 명령어 list
        self.caution = Label(window, text="* 명령어 List\nopen: O\nclose: C\nPos.제어: 숫자로 입력")
        self.caution.grid(row=30, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Command 1
        self.command11 = Label(window, text="Command 1")
        self.command11.grid(row=40, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.command1 = Entry(window)
        self.command1.grid(row=40, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Command 2
        self.command21 = Label(window, text="Command 2")
        self.command21.grid(row=50, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.command2 = Entry(window)
        self.command2.grid(row=50, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Command 3
        self.command31 = Label(window, text="Command 3")
        self.command31.grid(row=60, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.command3 = Entry(window)
        self.command3.grid(row=60, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Command 4
        self.command41 = Label(window, text="Command 4")
        self.command41.grid(row=70, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.command4 = Entry(window)
        self.command4.grid(row=70, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # Command 5
        self.command51 = Label(window, text="Command 5")
        self.command51.grid(row=80, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.command5 = Entry(window)
        self.command5.grid(row=80, column=1, padx=5, pady=5, ipadx=5, ipady=5)

        # 현재 cycle 수 표기
        self.text3 = Label(window, text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
        self.text3.grid(row=90, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Target cycle 수 표기
        self.text4 = Label(window, text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
        self.text4.grid(row=91, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Sequence 진행 button
        # startcycle
        self.button2 = Button(window, text="Start cycle", command=lambda: self.startcycle())
        self.button2.grid(row=100, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Cycle stop button
        # close
        self.exit = Button(window, text="Stop cycle", command=lambda: self.close())
        self.exit.grid(row=110, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        # Reset button
        # resetcycle
        self.reset = Button(window, text="Reset", command=lambda: self.resetcycle())
        self.reset.grid(row=120, column=0, padx=5, pady=5, columnspan=2, ipadx=5, ipady=5)

        window.mainloop()

    # Command window
    def commandwindow(self):
        global tail
        global sendcommand

        com = Toplevel(window)
        com.title("Command window")
        com.resizable(False, False)

        # Command 입력
        sendcommand = Entry(com)
        sendcommand.grid(row=0, column=0, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)

        # Send 버튼 생성
        sendbutton = Button(com, text="Send", command=lambda: self.getcommand())
        sendbutton.grid(row=0, column=2, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)

        # Send, receive 명령어 출력 창
        scrollbar1 = Scrollbar(com)
        scrollbar2 = Scrollbar(com)
        
        # Send data 출력 창 생성
        senddata = Label(com, text="Send data")
        senddata.grid(row=1, column=0, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)
        self.senddata1 = Text(com, width=20, height=30, yscrollcommand=scrollbar1.set, state='disabled')
        self.senddata1.grid(row=2, column=0, padx=2, pady=2, ipadx=2, ipady=2)
        scrollbar1.grid(row=2, column=1)

        # Receive data 출력 창 생성
        receivedata = Label(com, text="Receive data")
        receivedata.grid(row=1, column=2, columnspan=2, padx=2, pady=2, ipadx=2, ipady=2)
        self.receivedata1 = Text(com, width=20, height=30, yscrollcommand=scrollbar2.set, state='disabled')
        self.receivedata1.grid(row=2, column=2, padx=2, pady=2, ipadx=2, ipady=2)
        scrollbar2.grid(row=2, column=3)
        
        # Clear 버튼 생성
        clearbutton = Button(com, text="Clear", command=lambda: self.clearCommand())
        clearbutton.grid(row=3, column=0, columnspan=4, padx=2, pady=5, ipadx=2, ipady=2)

    def clearCommand(self):
        self.senddata1["state"] = 'normal'
        self.receivedata1["state"] = 'normal'
        self.senddata1.delete(1.0, END)
        self.receivedata1.delete(1.0, END)
        self.senddata1["state"] = 'disabled'
        self.receivedata1["state"] = 'disabled'

    def getcommand(self):
        global sendcommand
        global textIndex
        global tail

        # Command 칸에 입력 된 명령어 읽은 후 비우기
        sendcommandData = str(sendcommand.get())
        sendcommand.delete(0, END)

        # 명령어 주고 받는 구간
        try:
            if sendcommandData:
                # Send data 창에 입력한 명령어 작성
                self.senddata1["state"] = 'normal'
                self.senddata1.insert(INSERT, sendcommandData + '\n')
                self.senddata1["state"] = 'disabled'

                buffertemp = sendcommandData + tail
                ser.write(buffertemp.encode('ascii'))
            else:
                self.senddata1["state"] = 'normal'
                self.senddata1.insert(INSERT, "No send data" + '\n')
                self.senddata1["state"] = 'disabled'
        # Serial 통신 끊긴 경우에 대한 예외 처리
        except AttributeError:
            self.receivedata1["state"] = 'normal'
            self.receivedata1.insert(INSERT, "Fail to write data" + '\n')
            self.receivedata1["state"] = 'disabled'
            textIndex += 1
        # 예외 없을 경우 진행
        else:
            try:
                if ser.readable():
                    # Receive data 처리 및 입력
                    receiveData = ser.readline().decode()[:-2]
                    self.receivedata1["state"] = 'normal'
                    if not receiveData:
                        self.receivedata1.insert(INSERT, "No receive data" + '\n')
                    else:
                        self.receivedata1.insert(INSERT, receiveData + '\n')
                    self.receivedata1["state"] = 'disabled'
                    textIndex += 1
            except:
                self.receivedata1["state"] = 'normal'
                self.receivedata1.insert(INSERT, "Fail to receive data" + '\n')
                self.receivedata1["state"] = 'disabled'
                textIndex += 1

    # Cycle 횟수 reset
    def resetcycle(self):
        global i
        global cycle
        global targetcycle
        global window2
        global textbox
        global comportnumber
        global delay
        global exitcondition
        global starttriger

        # startcycle 함수 재진행 위해 parameter 값 초기화
        i = 0
        cycle = 0
        targetcycle = 0
        window2 = 0
        textbox = 0
        delay = 0
        starttriger = 0

        # cycle 표기 관련 항목 초기화
        self.text3.config(text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
        self.text4.config(text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
        window.update()

        # stop 조건 빠져나가기 위한 stop trigger 변수 초기화
        exitcondition = False

    # cycle stop
    def close(self):
        global exitcondition

        exitcondition = True

    # sequence 시작 함수
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
        global set1poscontrol
        global possiblecommand
        global starttriger

        # 예외처리: 필요 parameter 입력 여부 filtering
        try:
            inputentry = [self.command1, self.command2, self.command3, self.command4, self.command5]
            command = []

            getcycle = int(str(self.cyclenumber.get()))
            delay = int(str(self.delaytime.get()))

            # 목표 cycle 수 입력 값에 맞게 업데이트
            targetcycle = getcycle
            if targetcycle == 0:
                self.text4.config(text="Target cycle: X")
                window.update()
            else:
                self.text4.config(text="Target cycle: " + str(targetcycle // 10000) + " x 10,000 + " + str(targetcycle % 10000))
                window.update()

            # 입력된 command 받아오기
            for k in range(len(inputentry)):
                # 대소문자 구분 없애기 위해 대문자로 변경
                j = str(inputentry[k].get()).upper()
                # commnad 입력이 없으면 skip
                if j:
                    command.append(j)

            # 입력된 command X
            if len(command) == 0:
                starttriger = 1
            # 입력 받은 명령어 처리 가능여부 check
            for i in range(len(command)):
                digi = self.decidedigit(command[i])
                if not command:
                    starttriger = 1
                if not command[i] in possiblecommand:
                    if not digi:
                        starttriger = 1
                if digi:
                    buffer = float(command[i])
                    if buffer < 0 or buffer > 100:
                        starttriger = 1

            if starttriger == 1:
                window4 = Toplevel(window)
                window4.title("Warning")
                if len(command) == 0:
                    warn4 = Label(window4, text="Command를 입력 해주세요.")
                else:
                    warn4 = Label(window4, text="아직 지원하지 않는 명령어 입니다.")
                warn4.pack()

                starttriger = 0
            else:
                # cycle 0 > 즉, 무한 반복
                cycle = int(getcycle)
                if cycle == 0:
                    while True:
                        # stop cycle 눌렸을 때 처리되는 code
                        if exitcondition:
                            ser.write(cl.encode('ascii'))
                            break

                        try:
                            # 입력된 command 진행
                            for m in range(len(command)):
                                # open 및 close 명령어 진행
                                if command[m] == 'C' or command[m] == 'O':
                                    buffer = command[m] + tail
                                    ser.write(buffer.encode('ascii'))
                                # T3B: set point 1에 position setting 한 뒤 set point 1 활성화
                                else:
                                    # set point 1 position control mode(T 1 0)
                                    buffer1 = set1poscontrol + tail
                                    ser.write(buffer1.encode('ascii'))
                                    # set point 1 position 값 setting(S 1 입력값)
                                    buffer = 'S1' + command[m] + tail
                                    ser.write(buffer.encode('ascii'))
                                    # set point 1 활성화(D1)
                                    buffer2 = set1activate + tail
                                    ser.write(buffer2.encode('ascii'))
                                # command 사이 delay
                                time.sleep(int(delay) / 1000)
                        # 위의 command 진행 중 에러 발생시 pass
                        except AttributeError:
                            pass

                        # 진행된 cycle 1회 추가하여 update
                        i += 1
                        self.text3.config(text="Current cycle: " + str(i // 10000) + " x 10,000 + " + str(i % 10000))
                        window.update()

                else:
                    # target cycle로 자연수가 입력 되었을 경우 진행하는 code (진행은 위와 동일)
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
                                    buffer1 = set1poscontrol + tail
                                    ser.write(buffer1.encode('ascii'))
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

                        # target cycle에 도달시 loop 종료
                        if i == targetcycle:
                            window5 = Toplevel(window)
                            window5.title("Finish")
                            warn5 = Label(window5, text="Cycle 종료.")
                            warn5.pack()

        # 필요 parameter 입력 되지 않아 위의 try 내부 코드 오류 발생 시 경고 메세지 표시
        except:
            window6 = Toplevel(window)
            window6.title("Warning")
            warn6 = Label(window6, text="필요 parameter들을 모두 입력 해주세요.")
            warn6.pack()

    # comport open
    def getcomport(self):
        global textbox
        global window2
        global comportnumber
        global ser

        comportnumber = str(textbox.get())
        try:
            # 입력 받은 comport number 사용하여 port 연결
            ser = serial.Serial(
                port='COM'+comportnumber,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.5
            )

            self.button1.configure(text='COM'+comportnumber+" connected")
            self.endtoplevel(window2)
        # error 발생 시 경고창 발생
        except:
            self.button1.configure(text="No connection")
            window2.destroy()

            window3 = Toplevel(window)
            window3.title("Warning")
            warn3 = Label(window3, text="해당 comport와 연결된 device가 없습니다.")
            warn3.pack()

    # pop-up창 닫기 위한 함수, valve flapper 닫는 명령어 포함
    def endtoplevel(self, win):
        global cl
        cl = 'C' + tail
        ser.write(cl.encode('ascii'))

        win.destroy()

    # 숫자 판단
    def decidedigit(self, str):
        try:
            tmp = float(str)
            return True
        except ValueError:
            return False

    # comport 번호 입력 창
    def inputcomport(self):
        global ser
        global window
        global textbox
        global comportnumber
        global window2

        # comport 입력 버튼, 연결되어 있는 상태에서 열렸을 경우 현재 연결된 port를 닫음
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
# 끝날 때 port 연결 되어 있으면 pos 0%로 보낸 뒤 serial port 닫는다.
try:
    cl = 'C' + tail
    ser.write(cl.encode('ascii'))
    ser.close()
except AttributeError:
    pass
