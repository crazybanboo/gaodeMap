# -*- coding: utf-8 -*-
import math

# import xlrd
# import requests
# import json
# import os, sys
# Now_path = os.path.abspath(os.path.dirname(sys.argv[0]))
PI = 3.1415926


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def yuan(x0, y0, angle, r):
    x1 = x0 + r * math.cos(angle * PI / 180)
    y1 = y0 + r * math.sin(angle * PI / 180)
    return x1, y1


def fen_xiang_xian(x0, y0, x1, y1):
    x_value = x1 - x0  # 目的地-起点
    y_value = y1 - y0
    if x_value >= 0 and y_value >= 0:
        return 1
    if x_value < 0 and y_value >= 0:
        return 2
    if x_value < 0 and y_value < 0:
        return 3
    if x_value >= 0 and y_value < 0:
        return 4


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


# 角度输入度数即可
def get_delta_xy(angle, change_value):
    PI = 3.1415926
    delta_y = math.sin(du_rad(angle)) * change_value
    delta_x = math.cos(du_rad(angle)) * change_value

    delta_x = round(delta_x, 6)
    delta_y = round(delta_y, 6)
    return delta_x, delta_y


# 度数转弧度
def du_rad(du):
    return du * 2 * PI / 360


def try_qushuzi():
    lujing = 'C:/Users/dodo/Desktop/123.txt'
    r = open(lujing)
    w = open('112.txt', 'w')
    for line in r.readlines():
        # print(line)
        s = line[3:]
        print(s)
        w.write(s)
    w.close()
    r.close()


if __name__ == '__main__':
    print(get_delta_xy(124, -0.001))

    # try_qushuzi()
    # destination_jingdu, destination_weidu = yuan(121.457833, 31.210342, 124, 0.0203602)
    # print(destination_jingdu, destination_weidu)
    # url = 'http://restapi.amap.com/v3/geocode/regeo?output=json&location=121.449838,31.190515' \
    #       '&key=389880a06e3f893ea46036f030c94700&radius=100&extensions=all'
    # res = requests.get(url)
    # params = json.loads(res.text)
    # print(len(params["regeocode"]["pois"]))
    # print(params["regeocode"]["pois"][1]["distance"])

    # data = xlrd.open_workbook('半径_正式.xls')
    # table = data.sheets()[0]
    # print(table.col_values(0))
    # print(table.nrows)
    # print(table.cell(2,0).value)
    # for n in range(table.nrows):
    #     print(table.cell(n, 0).value)

    # print(get_delta_xy(180, -1)[0])# 增减直接用正负数chang_value
    # print(math.sin(45)*math.sqrt(2))
    # print(math.sqrt(2))
    # print(math.sin(du_rad(270)))# 0.017452406139607784
    # print(fen_xiang_xian(121.442591,31.190613,121.452508,31.187615))

    # print(yuan(2, 2, 360, 1))

# print(distance(121.442591, 31.190613, 121.452508, 31.187615))
# print(distance(121.442591, 31.190613, 121.461818, 31.197249))
# print(distance(121.442591, 31.190613, 121.414941, 31.202861))
