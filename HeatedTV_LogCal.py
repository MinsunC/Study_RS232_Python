import numpy
import os
# from matplotlib import pyplot as plt

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
    heaterpwr = [[], [], [], []]
    result_pwr = [[], [], [], []]
    stageheater = [[], [], []]
    result_stage = [[], [], []]

    try:
        foldername = input("""\n폴더명 or 종료하려면 'exit'을 입력 해주세요: """)

        if foldername.upper() == 'EXIT':
            break

        file_list = os.listdir(foldername)

        for file in file_list:
            pres = []
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
            heaterpwr = [[], [], [], []]
            result_pwr = [[], [], [], []]
            time = []
            stageheater = [[], [], []]
            result_stage = [[], [], []]

            z = 0
            filename = foldername + "\\" + file
            with open(filename, 'rt', encoding='UTF-8') as f:
                for line in f:
                    line_list = line.replace(';', ' ').replace(',', ' ').split()

                    if len(line_list) < 3:
                        continue
                    try:
                        step = float(line_list[2])
                    except ValueError:
                        continue
                    if step != 1 and z == 0:
                        continue
                    if step == 1 and z == 0:
                        z = 1
                    # pres.append(float(line_list[5]))
                    # heaterpwr[0].append(float(line_list[61]))
                    # heaterpwr[1].append(float(line_list[62]))
                    # heaterpwr[2].append(float(line_list[109]))
                    # heaterpwr[3].append(float(line_list[110]))
                    # stageheater[0].append(float(line_list[13]))
                    # stageheater[1].append(float(line_list[14]))
                    # stageheater[2].append(float(line_list[15]))
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

                print()
                print("Name: ", file)
                # try:
                for j in range(len(dep_pos)):
                    if len(dep_pos) != 1:
                        print("cycle", j+1)
                        result_dep.append(numpy.mean(dep_pos[j]))
                        result_dep.append(numpy.std(dep_pos[j]))
                        result_dep.append(numpy.max(dep_pres[j]))
                        result_dep.append(numpy.min(dep_pres[j]))

                        result_nit.append(numpy.mean(nit_pos[j]))
                        result_nit.append(numpy.std(nit_pos[j]))
                        result_nit.append(numpy.max(nit_pres[j][10:]))
                        result_nit.append(numpy.min(nit_pres[j][10:]))

                    else:
                        result_dep.append(numpy.mean(dep_pos[j]))
                        result_dep.append(numpy.std(dep_pos[j]))
                        result_dep.append(numpy.max(dep_pres[j]))
                        result_dep.append(numpy.min(dep_pres[j]))

                        result_nit.append(numpy.mean(nit_pos[j]))
                        result_nit.append(numpy.std(nit_pos[j]))
                        result_nit.append(numpy.max(nit_pres[j][10:]))
                        result_nit.append(numpy.min(nit_pres[j][10:]))

                    print("Dep:", end=" ")
                    for m in range(len(result_dep)):
                        print(result_dep[m], end=" ")
                    print()
                    print("Nit:", end=" ")
                    for n in range(len(result_nit)):
                        print(result_nit[n], end=" ")
                    print()

                    result_dep = []
                    result_nit = []
                # except:
                #     continue

                # result_pwr[0].append(numpy.mean(heaterpwr[0]))
                # result_pwr[0].append(numpy.max(heaterpwr[0]))
                # result_pwr[0].append(numpy.min(heaterpwr[0]))
                # result_pwr[1].append(numpy.mean(heaterpwr[1]))
                # result_pwr[1].append(numpy.max(heaterpwr[1]))
                # result_pwr[1].append(numpy.min(heaterpwr[1]))
                # result_pwr[2].append(numpy.mean(heaterpwr[2]))
                # result_pwr[2].append(numpy.max(heaterpwr[2]))
                # result_pwr[2].append(numpy.min(heaterpwr[2]))
                # result_pwr[3].append(numpy.mean(heaterpwr[3]))
                # result_pwr[3].append(numpy.max(heaterpwr[3]))
                # result_pwr[3].append(numpy.min(heaterpwr[3]))
                # result_stage[0].append(numpy.mean(stageheater[0]))
                # result_stage[0].append(numpy.max(stageheater[0]))
                # result_stage[0].append(numpy.min(stageheater[0]))
                # result_stage[1].append(numpy.mean(stageheater[1]))
                # result_stage[1].append(numpy.max(stageheater[1]))
                # result_stage[1].append(numpy.min(stageheater[1]))
                # result_stage[2].append(numpy.mean(stageheater[2]))
                # result_stage[2].append(numpy.max(stageheater[2]))
                # result_stage[2].append(numpy.min(stageheater[2]))

                # print("21 temp:", end=" ")
                # for m1 in range(len(result_pwr[0])):
                #     print(result_pwr[0][m1], end=" ")
                # print()
                # print("22 temp:", end=" ")
                # for m2 in range(len(result_pwr[1])):
                #     print(result_pwr[1][m2], end=" ")
                # print()
                # print("21 pwr:", end=" ")
                # for m3 in range(len(result_pwr[2])):
                #     print(result_pwr[2][m3], end=" ")
                # print()
                # print("22 pwr:", end=" ")
                # for m4 in range(len(result_pwr[3])):
                #     print(result_pwr[3][m4], end=" ")
                # print()
                # print("Stage heater temp:", end=" ")
                # for m5 in range(len(result_stage[0])):
                #     print(result_stage[0][m5], end=" ")
                # print()
                # print("Stage pwr ReadIn:", end=" ")
                # for m6 in range(len(result_stage[1])):
                #     print(result_stage[1][m6], end=" ")
                # print()
                # print("Stage pwr ReadOut:", end=" ")
                # for m7 in range(len(result_stage[2])):
                #     print(result_stage[2][m7], end=" ")
                # print()
                result_dep = []
                result_nit = []

                # for k in range(len(pres)):
                #     time.append(0.1 * k)
                # plt.plot(time, pres, linewidth=1, label=file)

        # plt.xlabel('Time [s]')
        # plt.ylabel('Pressure [Torr]')
        # plt.grid()
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # plt.tight_layout()
        # plt.show()

        # print("Temp: (Body, flapper) = " + "(" + str(numpy.mean(temp[0])) + ", " + str(numpy.mean(temp[1])) + ")")

    except:
        continue

print("Complete!")
