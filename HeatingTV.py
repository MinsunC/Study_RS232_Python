import numpy
from matplotlib import pyplot as plt

while True:
    graph_time = []
    graph_step = []
    graph_pressure = []
    dep_pos = []
    dep_pres = []
    nit_pos = []
    nit_pres = []
    buf_dep_pos = []
    buf_dep_pres = []
    buf_nit_pos = []
    buf_nit_pres = []
    result_dep = []
    result_nit = []
    temp = [[], []]

    # try:
    filename = input("""\n파일명(xlsx 확장자 포함 파일 이름)\nor 종료하려면 'exit'을 입력 해주세요: """)

    if filename.upper() == 'EXIT':
        break

    with open(filename, 'rt', encoding='UTF-8') as f:
        for line in f:
            line_list = line.replace(';', ' ').replace(',', ' ').split()
            if len(line_list) < 3:
                continue
            try:
                step = float(line_list[2])
            except ValueError:
                continue
            temp[0].append(float(line_list[61]))
            temp[1].append(float(line_list[62]))
            if step == 9:
                buf_dep_pos.append(float(line_list[4]))
                buf_dep_pres.append(float(line_list[5]))
            if step == 10 and buf_dep_pos:
                dep_pos.append(buf_dep_pos)
                dep_pres.append(buf_dep_pres)
                buf_dep_pos = []
                buf_dep_pres = []
            if step == 16:
                buf_nit_pos.append(float(line_list[4]))
                buf_nit_pres.append(float(line_list[5]))
            if step == 17 and buf_nit_pos:
                nit_pos.append(buf_nit_pos)
                nit_pres.append(buf_nit_pres)
                buf_nit_pos = []
                buf_nit_pres = []

        result_dep.append(numpy.mean(dep_pos[i]))
        result_dep.append(numpy.std(dep_pos[i]))
        result_dep.append(numpy.max(dep_pres[i]))
        result_dep.append(numpy.min(dep_pres[i]))

        result_nit.append(numpy.mean(nit_pos[i]))
        result_nit.append(numpy.std(nit_pos[i]))
        result_nit.append(numpy.max(nit_pres[i]))
        result_nit.append(numpy.min(nit_pres[i]))

        print("Dep:", end=" ")
        print(result_dep)
        print("Nit:", end=" ")
        print(result_nit)

    # print("Temp: (Body, flapper) = " + "(" + str(numpy.mean(temp[0])) + ", " + str(numpy.mean(temp[1])) + ")")

    # except:
    #     continue

print("Complete!")
