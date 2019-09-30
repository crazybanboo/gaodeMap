# -*- coding: utf-8 -*-
import xlwt
import requests
import json
import mf
import os, sys
# from goto import with_goto
Now_path = os.path.abspath(os.path.dirname(sys.argv[0]))
# 121.457833,31.210342 襄阳南路
# 121.442489,31.190129 南丹东路
# 121.377899,31.204861 虹古路
# 121.518910,31.228420 八佰伴
# 121.415711,31.218476 中山公园
# 121.454790,31.230410 北京西路
# 121.480835,31.207344 丽园路
# ##### 在高德开放平台上获取到的新经纬度#####
# 121.377938,31.204807 虹古路
# 121.457833,31.210342 襄阳南路
# 121.518943,31.228569 八佰伴
# 可更改参数#####################################
# origin_jingdu = 121.457833
# origin_weidu = 31.210342
# r_yuan = 0.0083602
# fanwei_r = 800# 搜索区域路程半径
lastest_dir = "20190219lastest"
# excel_name = '半径_襄阳南路800m.xls'
# n = 0# 起始度数

jingweidu_tuple_list = [
                        # (121.457833,31.210342,"襄阳南路"),# 襄阳南路
                        # (121.442489,31.190129,"南丹东路"),# 南丹东路
                        # (121.377899,31.204861,"虹古路"),# 虹古路
                        # (121.518910,31.228420,"八佰伴"),# 八佰伴
                        # (121.415711,31.218476,"中山公园"),# 中山公园
                        # (121.454790,31.230410,"北京西路"),# 北京西路
                        # (121.480835,31.207344,"丽园路")# 丽园路
                        # (121.405277,31.195232,"富贵东道")# 富贵东道
                        # (121.416100,31.170090,"田林路")
                        # (121.440180,31.245970,"澳门路"),
                        # (121.381410,31.173330,"亲水花街"),
                        # (121.379784,31.106590,"莘庄"),
                        # (121.260529,31.345648,"宝龙城市广场"),
                        # (121.503700,31.277210,"五角场"),
                        # (121.482390,31.234950,"南京东路"),
                        # (121.488390,31.266740,"欧阳路"),
                        # (121.260900,31.346090,"宝龙城市广场"),
                        # (121.482390,31.234950,"人民广场"),
                        # (121.431840,31.136710,"凌云沃尔玛"),
                        # (121.427280,31.280960,"静安大融城"),
                        (121.456639,31.183624,"绿地缤纷城"),
                        (121.313762,31.192502,"华泾龙湖天街"),
                        (121.549887,29.807907,"宁波南部商务区")
                        ]
circleR_distance_list = [
                        (0.0053602, 500),
                         (0.0103602, 1000),
                         (0.0203602, 2000),
                         (0.0303602, 3000),
                         (0.0403602, 4000),
                         (0.0503602, 5000),
                         ]
# circleR_distance_list = [
#                         (0.0083602, 800),
#                          (0.0123602, 1200),
#                          (0.0153602, 1500),
#                          (0.0183602, 1800),
#                          (0.0253602, 2500),
#                          (0.0303602, 3000),
#                          (0.0353602, 3500),
#                          (0.0423602, 4200),
#                          (0.0503602, 5000)
#                          ]
################################################


# print(params['route']['paths'][0]['distance'])
# print(params['route']['paths'][0]['duration'])

class FindPoint(object):
    def __init__(self):
        

        self.shop_cnt = 0
        self.distance_cnt = 0
        self.errorHappen = False

    # @with_goto
    # def getPointToExecel(self, origin_jingdu, origin_weidu, shop_name, circleR_distance_list1):
    def getPointToExecel(self, origin_jingdu, origin_weidu, shop_name, circleR_distance_tuple):
        while True:
            try:
                book = xlwt.Workbook(encoding='utf-8')
                sheet = book.add_sheet('Sheet1')
                sheet.write(0, 0, '序号')
                sheet.write(0, 1, '目标经度')
                sheet.write(0, 2, '目标纬度')
                sheet.write(0, 3, '距离')             
                num_sheet = 0
                change_value = 0.001
                d_dict = {}# 防止来回都归不到所需的范围               
                times = 0
                distance = 0
                # label .nextShop# -----------------------------------------------------------------------------       
                # origin_jingdu, origin_weidu, shop_name = jingweidu_tuple_list[self.shop_cnt]
                # r_yuan, fanwei_r = circleR_distance_list1[self.distance_cnt] # 每个店铺的第一次赋值在这
                r_yuan, fanwei_r = circleR_distance_tuple # 每个店铺的第一次赋值在这
                
                file_dir = '/'+ lastest_dir + '/'+ shop_name +'/'# excel_name = '半径_襄阳南路800m.xls'
                # if self.cnt == len(jingweidu_tuple_list) + 1:
                #     return
                
                # 如果失败从这重新开始
                # label .restart# -----------------------------------------------------------------------------
                
                excel_name = '半径_'+ shop_name + str(fanwei_r) + 'm.xls'# excel_name = '半径_襄阳南路800m.xls'
                destination_jingdu, destination_weidu = mf.yuan(origin_jingdu, origin_weidu, 0, r_yuan)
                destination_jingdu = round(destination_jingdu, 6)
                destination_weidu = round(destination_weidu, 6)
                print(destination_jingdu, destination_weidu)

                n = 0
                
                while True:
                    
                    # times = times + 1
                    # print(times)
                    # print('distance:',distance)
                    url_amap = 'http://restapi.amap.com/v3/direction/walking?origin=' + str(origin_jingdu) + ',' + str(origin_weidu) + \
                            '&destination=' + str(destination_jingdu) + ',' + str(destination_weidu) + \
                            '&key=389880a06e3f893ea46036f030c94700'
                    res = requests.get(url_amap)  # 向网页请求字符串数据
                    params = json.loads(res.text)  # 暂存为json格式
                    # print('status:', params["info"])
                    if params["info"] != 'ok':
                        print('获取params失败')
                        continue
                    distance = int(params['route']['paths'][0]['distance'])# 获取距离数据
                    if distance <= fanwei_r - 100:# 距离太近
                        if distance not in d_dict:
                            d_dict[distance] = 0
                        else:
                            d_dict[distance] = d_dict[distance] + 1
                        # print(d_dict.values())
                        # print('distance:', distance)
                        # print('change_value:', change_value)
                        if max(d_dict.values())==3:
                            key = mf.get_keys(d_dict, 3)  # 获取值为3的key
                            d_dict[key[0]] = d_dict[key[0]] - 1
                            change_value = change_value/2
                        if change_value < 6.25e-05:# 防止死循环
                            d_dict = {}
                            change_value = 0.001
                            n = n + 1
                            destination_jingdu, destination_weidu = mf.yuan(origin_jingdu, origin_weidu, n, r_yuan)
                            destination_jingdu = round(destination_jingdu, 6)
                            destination_weidu = round(destination_weidu, 6)
                            continue
                        # xiangxian = mf.fen_xiang_xian(origin_jingdu, origin_weidu, destination_jingdu, destination_weidu)
                        destination_jingdu = destination_jingdu + mf.get_delta_xy(n, change_value)[0]
                        destination_weidu = destination_weidu + mf.get_delta_xy(n, change_value)[1]

                    elif fanwei_r-100 <distance< fanwei_r:
                        d_dict = {}# 重置，重新开始计数往复次数
                        change_value = 0.001
                        n = n + 1
                        num_sheet = num_sheet + 1
                        print(shop_name, 'n:', n)
                        sheet.write(num_sheet, 0, n)
                        sheet.write(num_sheet, 1, destination_jingdu)
                        sheet.write(num_sheet, 2, destination_weidu)
                        sheet.write(num_sheet, 3, distance)

                        # print('times:',times)
                        # 逆时针旋转一度找点
                        destination_jingdu, destination_weidu = mf.yuan(origin_jingdu, origin_weidu, n, r_yuan)
                        destination_jingdu = round(destination_jingdu, 6)
                        destination_weidu = round(destination_weidu, 6)
                        # print('经度：', destination_jingdu)
                        # print('纬度：', destination_weidu)
                        # book.save('D:/软件学习_Software/python/高德API_找半径/' + excel_name)
                        book.save(Now_path + file_dir + excel_name)
                        if n >= 359:
                            break
                    elif distance >= fanwei_r:
                        if distance not in d_dict:
                            d_dict[distance] = 0
                        else:
                            d_dict[distance] = d_dict[distance] + 1
                        # print(d_dict.values())
                        # print('distance:', distance)
                        # print('change_value:', change_value)
                        if max(d_dict.values())==3:
                            key = mf.get_keys(d_dict, 3)# 获取值为3的key
                            d_dict[key[0]] = d_dict[key[0]] - 1
                            change_value = change_value/2
                        if change_value < 6.25e-05:# 防止死循环
                            d_dict = {}
                            change_value = 0.001
                            n = n + 1
                            destination_jingdu, destination_weidu = mf.yuan(origin_jingdu, origin_weidu, n, r_yuan)
                            destination_jingdu = round(destination_jingdu, 6)
                            destination_weidu = round(destination_weidu, 6)
                            continue
                        # xiangxian = mf.fen_xiang_xian(origin_jingdu, origin_weidu, destination_jingdu, destination_weidu)
                        destination_jingdu = destination_jingdu + mf.get_delta_xy(n, -change_value)[0]
                        destination_weidu = destination_weidu + mf.get_delta_xy(n, -change_value)[1]
            except Exception as e:
                # goto .restart
                print(e)
                self.errorHappen = True

            finally:
                if self.errorHappen is True: # 如果发生了错误则当前循环重新来一遍
                    self.errorHappen = False
                else:
                    return
                    # if self.shop_cnt == len(jingweidu_tuple_list):
                    #     self.shop_cnt = 0
                    #     print('finish!')
                    #     return
                    
                    # self.distance_cnt = self.distance_cnt + 1
                    # if self.distance_cnt == len(circleR_distance_list):
                    #     self.distance_cnt = 0
                    #     print(shop_name, 'finish!')
                    #     return
                    #     # self.shop_cnt = self.shop_cnt + 1
                    #     # goto .nextShop
                    # print(self.distance_cnt)
                    # r_yuan, fanwei_r = circleR_distance_list[self.distance_cnt]


if __name__ == '__main__':
    from multiprocessing import Pool

    shop_num = len(jingweidu_tuple_list)
    length = len(circleR_distance_list)
    shop_list = []
    # p = Pool(shop_num*length)
    p = Pool(4)
    for i in range(shop_num):
        for n in range(length):
            shop_list.append(FindPoint())

        jingdu =    jingweidu_tuple_list[i][0]
        weidu =     jingweidu_tuple_list[i][1]
        shop_name = jingweidu_tuple_list[i][2]
        # 为进程创建任务 为任务传参
        
        for j in range(length):
            print('j=',j)
            p.apply_async(shop_list[i*length+j].getPointToExecel, args=(jingdu, weidu, shop_name, circleR_distance_list[j],))
    
    p.close()
    p.join()
    
    # find = FindPoint()
    # find.getPointToExecel()
