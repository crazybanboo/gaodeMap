# -*- coding: utf-8 -*-
import requests
import json
import xlrd, xlwt
import mf
import sys

#用于测试高德api是否能正确读取到想要的值

# print(sys.path[0])
# 可更改参数#####################################
excel_name = '地址名称数据_襄阳南路500m.xls'
# 打开excel表格读取数据于data中
data = xlrd.open_workbook(sys.path[0] + '/襄阳南路/半径_襄阳南路500m.xls')
################################################
# 选中第一个sheet
table = data.sheets()[0]
#创建写数据的excel
book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('Sheet1')
sheet.write(0, 0, '序号')
sheet.write(0, 1, '地址名称')
sheet.write(0, 2, '最短距离')
sheet.write(0, 3, '感兴趣点数')
sheet.write(0, 4, '距离')


# 读取经纬度
for i in range(table.nrows):
    if i == 0:
        continue
    xuhao = table.cell(i, 0).value# 获取坐标表格中的序号
    distance = table.cell(i, 3).value# 获取坐标表格中的距离信息
    print('行：', i, '序号：', xuhao)# 打印序号
    jingdu = round(table.cell(i, 1).value, 6)# 获取表格中的经度
    weidu = round(table.cell(i, 2).value, 6)  # 获取表格中的纬度
    url = 'http://restapi.amap.com/v3/geocode/regeo?output=json&location='+str(jingdu)+','+str(weidu)+\
          '&key=389880a06e3f893ea46036f030c94700&radius=100&extensions=all'
    res = requests.get(url)
    params = json.loads(res.text)
    # 100米内无感兴趣点即跳过
    if len(params["regeocode"]["pois"]) == 0:
        sheet.write(i, 0, xuhao)
        sheet.write(i, 1, '无')
        print('无无无无')
        continue
    # 比较各感兴趣点与坐标点的距离，选择最近的那个
    d_poi = {}
    for poi in params["regeocode"]["pois"]:
        # print(poi['name'], poi['distance'])
        d_poi[poi['name']] = float(poi['distance'])# 加入字典
    min_distance = min(d_poi.values())
    name = mf.get_keys(d_poi, min_distance)
    print(name[0], min_distance)
    sheet.write(i, 0, xuhao)
    sheet.write(i, 1, name[0])
    sheet.write(i, 2, min_distance)
    sheet.write(i, 3, len(params["regeocode"]["pois"]))
    sheet.write(i, 4, distance)
    book.save('D:/软件学习_Software/python/高德API_找半径/虹古路/'+excel_name)
    # if i == 10:
    #     break

print('finish')


