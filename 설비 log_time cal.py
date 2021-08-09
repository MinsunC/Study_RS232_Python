buffer = []
abc = []

def time_cal(temp):
    time_list = temp.replace(':', ' ').split()

    hour = float(time_list[0])
    min = float(time_list[1])
    sec = float(time_list[2])

    timeC = round(hour * 3600 + min * 60 + sec, 3)

    return timeC

loglist = "I:\WB01_ALL"

with open(loglist, 'rt', encoding='UTF-8') as f:
    for line in f:
        line_list = line.replace(';', ' ').replace(',', ' ').split()
        if len(line_list) < 3:
            continue
        buffer.append(line_list)

if len(buffer[0]) != len(buffer[1]):
    abc.append('Date')
    abc.append('Time')
    for i in range(len(buffer[0])-1):
        abc.append(buffer[0][i+1])
    buffer[0] = abc

for i in range(len(buffer)-1):
    for j in range(len(buffer[i])-1):
        try:
            buffer[i+1][j] = float(buffer[i+1][j])
        except ValueError:
            continue

start = time_cal(buffer[1][1])

for z in range(len(buffer)):
    try:
        current = time_cal(buffer[z+1][1])
        print(current - start)
    except IndexError:
        continue
