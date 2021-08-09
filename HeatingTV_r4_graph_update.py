import numpy
import os
import itertools
from matplotlib import pyplot as plt
from bokeh.models import ColumnDataSource
from bokeh.plotting import output_file, figure, show
from bokeh.palettes import Category10 as palette

output_file("graph.html")
plot = figure()

#
# def color_gen():
#     yield from itertools.cycle(Category10[10])


# color = color_gen()
colors = itertools.cycle(palette)
while True:
    q = 0
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
        time = []

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
                pres.append(float(line_list[5]))
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

            print()
            print("Name: ", file)

            for j in range(len(dep_pos)):
                if len(dep_pos) != 1:
                    print("cycle", j+1)
                    result_dep.append(numpy.mean(dep_pos[j]))
                    result_dep.append(numpy.std(dep_pos[j]))
                    result_dep.append(numpy.max(dep_pres[j]))
                    result_dep.append(numpy.min(dep_pres[j]))

                    result_nit.append(numpy.mean(nit_pos[j]))
                    result_nit.append(numpy.std(nit_pos[j]))
                    result_nit.append(numpy.max(nit_pres[j]))
                    result_nit.append(numpy.min(nit_pres[j]))

                else:
                    result_dep.append(numpy.mean(dep_pos[j]))
                    result_dep.append(numpy.std(dep_pos[j]))
                    result_dep.append(numpy.max(dep_pres[j]))
                    result_dep.append(numpy.min(dep_pres[j]))

                    result_nit.append(numpy.mean(nit_pos[j]))
                    result_nit.append(numpy.std(nit_pos[j]))
                    result_nit.append(numpy.max(nit_pres[j]))
                    result_nit.append(numpy.min(nit_pres[j]))

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

            for k in range(len(pres)):
                time.append(0.1 * k)
            plot.line(time, pres, color=colors, line_width=2, muted_color="#ececec", alpha=0.8, legend_label=file)
            q += 1
    # plt.xlabel('Time [s]')
    # plt.ylabel('Pressure [Torr]')
    # plt.grid()
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.tight_layout()
    plot.legend.location = "center_right"
    plot.legend.click_policy = "mute"

    show(plot)

    # print("Temp: (Body, flapper) = " + "(" + str(numpy.mean(temp[0])) + ", " + str(numpy.mean(temp[1])) + ")")

    # except:
    #     continue

print("Complete!")
