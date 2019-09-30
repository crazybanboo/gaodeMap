# -*- coding: utf-8 -*-
import requests
import json
import xlrd, xlwt
import mf
import os, sys

#画地图程序
# 800 1200 1500 1800 2500 3000 3500 4200 5000
# 15  15   14   14   14   13   13   13   12
# 121.457833,31.210342 襄阳南路
# 121.442489,31.190129 南丹东路
# 121.377899,31.204861 虹古路
# 121.518910,31.228420 八佰伴
# 121.415711,31.218476 中山公园
# 121.454790,31.230410 北京西路
# 121.480835,31.207344 丽园路
# 121.512293,31.255874 保定路
############可更改的数据####################
shop_name = '宁波南部商务区'
file_dir = '/20190219lastest/'+shop_name+'/'# 输入存放excel的文件夹
Now_path = os.path.abspath(os.path.dirname(sys.argv[0])) + file_dir
# data = xlrd.open_workbook(Now_path + '半径_保定路5000m.xls')
# map_name = Now_path + '保定路_地图图片5000m.png'
###########################################
params_list = [(500,15),(1000,15),(2000,14),(3000,13),(4000,13),(5000,12)]
# params_list = [(800,15),(1200,15),(1500,14),(1800,14),(2500,14),(3000,13),(3500,13),(4200,13),(5000,12)]
for l in params_list:
    meter = l[0]
    zoom = l[1]
    data = xlrd.open_workbook(Now_path + '半径_'+shop_name+str(meter)+'m.xls')
    map_name = Now_path + shop_name+'_地图图片'+str(meter)+'m.png'
# 选中第一个sheet
    table = data.sheets()[0]
    locations = []
    for row in range(table.nrows):
        if row == 0:
            continue
        locations.append(str(round(table.cell(row, 1).value, 6)))# 经度
        locations.append(',')# 格式：116.31604, 39.96491;
        locations.append(str(round(table.cell(row, 2).value, 6)))# 纬度
        locations.append(';')

    locations.pop() 
    # print(locations)
    s = ''
    s_locations = s.join(locations)
    # print(s_locations)
    # 1024*1024是图片宽高的最大值 zoom值越大放的越大 1000-》15
    url = 'http://restapi.amap.com/v3/staticmap?zoom='+str(zoom)+'&size=1024*1024&scale=2&paths=3,0x0000ff,1,,:' \
        +s_locations+ \
        '&key=389880a06e3f893ea46036f030c94700'

    res = requests.get(url)

    # r = requests.get(url,stream=True)
    with open(map_name, 'wb') as fd:
        for chunk in res.iter_content():
            fd.write(chunk)

print('finish!!')
# print(json.loads(res.text))