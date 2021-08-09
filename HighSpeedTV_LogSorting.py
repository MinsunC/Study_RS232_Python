list = []
count = 0
line1 = 0
temp = ""

with open("I:\\Sort.txt", 'r') as f:
    for line in f:
        list.append(line[:-1])
        count += 1
        if count > 3:
            for m in range(len(list)):
                temp += list[m] + " "
            print(temp)
            temp = ""
            list = []
            count = 0
            continue