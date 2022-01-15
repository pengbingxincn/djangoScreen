from django.shortcuts import render, HttpResponse

# Create your views here.
from app01.models import *
from django.db.models import Count
import json
import datetime
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
'''
test 发送请求，测试获取到的数据
get_province_data() 统计每个省份的专利数量，取最高前八位得 返回列表
get_time_data()统计每个年份的申请日和公开日的数量
get_all_data()统计专利总数有效专利总数
get_classific_data()获取行业分类的数据 和近半年授权分布（未完成）
down_json()更新数据
loads_json()获取到map表中的数据 -------所有数据最终都是从此函数中获取
update_map(name_m,value_m)更新数据子操作
'''


def index(request):
    data = loads_json()
    province_top_data = data["province_top_data"][::-1]
    province_top_name = data["province_top_name"]
    all_datas = data["all_datas"]
    legal_datas = data["legal_datas"]
    pr_date_year_list = data["pr_date_year_list"]
    pr_date_year_data = data["pr_date_year_data"]
    ar_date_year_data = data["ar_date_year_data"]
    class_datas = data["class_datas"][::-1]
    class_names = data["class_names"]

    return render(request, "index.html", {"province_top": province_top_name,
                                          "province_top_data": province_top_data,
                                          "all_data": all_datas,
                                          "year_list": pr_date_year_list,
                                          "year_data": pr_date_year_data,
                                          "time_data": legal_datas,
                                          "ar_date_year_data": ar_date_year_data,
                                          "class_data": class_datas,
                                          "class_name": class_names,
                                          })


def test(request):
    # 测试
    # loads_json()
    # down_json()
    # get_classific_data()
    down_json()
    return HttpResponse("ok")


def get_province_data():
    '''
    获取每个省份的专利总数，获取前八位
    '''
    # 得到总的数据
    result = PatentApplicantDetail.objects.values("province").annotate(total=Count("province")).all()
    # 设置两个列表，c存放省份，d存放总数
    # c = []
    # d = []
    # for i in result:
    #     # 排除获取到的数据中省份为None
    #     if i["province"] != None:
    #         c.append(i["province"])
    #         d.append(i["total"])
    # # 将省份和总数分别存储列表中
    # res_province = [c, d]
    # print(d)
    ret_det = {}
    for i in result:
        if i["province"] != None:
            ret_det[i["province"]] = i["total"]

    det = {}
    for key in ret_det:
        res = PatentConstGroupSet.objects.filter(group=8).filter(stored_value=key).values_list('display_name')
        if len(res) != 0:
            det[res[0][0]] = ret_det[key]
    new_data = sorted(det.items(), key=lambda item: item[1])
    a = []
    b = []
    # 以上排序为递增截取后后8个数据
    for i in new_data[-8:]:
        a.append(i[0])
        b.append(i[1])
    res_list = [a, b]
    # print(res_list)
    # 返回列表 a 省份 b count数据
    return res_list


def get_time_data():
    '''
    统计每个年份的申请日和公开日的数量
    pr_date_count_res 申请日
    ar_date_count_res 公开日
    pr_date_year_list = [] 所有的年份
    ar_date_year_data = [] 申请日每个年份的专利总数
    pr_date_year_data = [] 公开日每个年份的专利总数
    返回 年份 申请日总数 公开日总数
    '''
    pr_date_count_res = PatentPatent.objects.extra(select={'year': 'extract( year from pr_date )'}).values(
        'year').annotate(dcount=Count('pr_date'))
    ar_date_count_res = PatentPatent.objects.extra(select={'year': 'extract( year from ar_date )'}).values(
        'year').annotate(dcount=Count('ar_date'))
    pr_date_year_list = []
    ar_date_year_data = []
    pr_date_year_data = []
    for i in pr_date_count_res:
        pr_date_year_list.append(i["year"])
        pr_date_year_data.append(i["dcount"])
    for i in ar_date_count_res:
        ar_date_year_data.append(i["dcount"])
    return pr_date_year_list, pr_date_year_data, ar_date_year_data


def get_all_data():
    # 统计专利总数
    all_data = PatentPatent.objects.values().count()
    # 统计有效专利总数
    legal_data = PatentPatent.objects.filter(legal_status=1).count()
    return all_data, legal_data


def get_classific_data():
    '''
    获取行业分类的数据
    :return: 每个分类top8
    '''
    # classic_data = PatentCategory.objects.values("first_class").annotate(total=Count("first_class")).all()

    # 获取到去重后的类比int型号 1~31 99
    classic_data = PatentCategory.objects.values("first_class").distinct()
    # 将类别存到class_int列表中
    class_int = []
    for i in classic_data:
        class_int.append(i["first_class"])
    # 获取到每个class对应的id，字典key first_class value 该类别对应的所有id ，该id也对应到PatentPatent表中的id
    id_det = {}
    for i in class_int:
        id_data = PatentCategory.objects.filter(first_class=i).values("id")
        temp_data = []
        for j in id_data:
            temp_data.append(j["id"])
        id_det[i] = temp_data

    # 循环每个id_det中的key，并循环对应的id_list,根据id_list中的id统计该id在PatentPatent中有多少数据，需要计算列表中所有id并求和得到该key所对应类别的总数
    res_det = {}
    res_half_det = {}
    for key in id_det:
        id_count_sum = 0
        half_count_sum = 0
        for v in id_det[key]:
            id_count = PatentPatent.objects.filter(loc=v).count()
            dt_s = datetime.now().date()  # 2018-7-15
            dt_e = (dt_s - timedelta(360))  # 2018-7-08

            half_count = PatentPatent.objects.filter(loc=v).filter(pr_date__range=[dt_s, dt_e]).count()
            id_count_sum = id_count_sum + id_count
            half_count_sum = half_count_sum + half_count
        res_det[key] = id_count_sum
        res_half_det[key] = half_count_sum
    print(res_half_det)
    # 将res_det中key数字显式化
    dis_name = {"1": "食品", "2": "服饰", "3": "旅行", "4": "刷具"
        , "5": "纺织板材", "6": "家具", "7": "家居", "8": "工具", "9": "包装容器",
                "10": "测量仪器", "11": "装饰品", "12": "运输工具", "13": "电力设备", "14": "处理设备",
                "15": "机器", "16": "摄影设备", "17": "乐器", "18": "办公机械", "19": "办公设备",
                "20": "广告设备", "21": "玩具体育", "22": "武器\杀虫",
                "23": "流体设备", "24": "实验设备",
                "25": "建筑元素", "26": "照明器具", "27": "烟草", "28": "药品器具", "29": "救援装置",
                "30": "动物用品", "31": "机器和器具", "32": "图形装饰", "99": "其他"}

    # 对于得到的统计数据进行排序并替换key为其所代表的类别，取前六位
    finall_res = {}
    for key in res_det:
        new_key = dis_name[key]
        finall_res[new_key] = res_det[key]
    new_data = sorted(finall_res.items(), key=lambda item: item[1])
    class_name = []
    class_data = []
    # 以上排序为递增截取后后六个数据
    for i in new_data[-6:]:
        class_name.append(i[0])
        class_data.append(i[1])




    return class_data, class_name


'''
    在 PatentCategory
    通过first_class 1-7查id
    得知了id统计PatentPatent中loc==id的
'''


# Map  更新插入数据
# 如果有新的数据需要存到map数据表中，在该函数下调用update_map(k,v)
def down_json():

    #获取数据并将数据转为json格式存储到数据库中,如果数据库中该字段就更新不存在就插入
    province_top = get_province_data()
    province_top_name = json.dumps(province_top[0])
    province_top_data = json.dumps(province_top[1])
    update_map("province_top_name", province_top_name)
    update_map("province_top_data", province_top_data)
    all_data, legal_data = get_all_data()
    all_datas = json.dumps(all_data)
    legal_datas = json.dumps(legal_data)
    update_map("all_datas", all_datas)
    update_map("legal_datas", legal_datas)
    year_list, year_data, ar_year_data = get_time_data()
    pr_date_year_list = json.dumps(year_list)
    pr_date_year_data = json.dumps(year_data)
    ar_date_year_data = json.dumps(ar_year_data)
    update_map("pr_date_year_list", pr_date_year_list)
    update_map("pr_date_year_data", pr_date_year_data)
    update_map("ar_date_year_data", ar_date_year_data)
    class_data, class_name = get_classific_data()
    class_datas = json.dumps(class_data)
    class_names = json.dumps(class_name)
    update_map("class_datas", class_datas)
    update_map("class_names", class_names)


def loads_json():
    # 读取map中的数据并loads，变为原来的数据类型
    res = Map.objects.values()
    res_det = {}
    for i in res:
        res_det[json.loads(i["name"])] = json.loads(i["value"])
    return res_det

def update_map(name_m,value_m):

    #首先将数据变为json字符串，判断该字段name是否存在，存在修改，不存在插入
    json_name_m = json.dumps(name_m)
    name = Map.objects.filter(name=json_name_m).all().values()
    if name.exists():
        Map.objects.filter(name = json_name_m).update(value=value_m)
    else:
        obj = Map(name=json.dumps(name_m), value=value_m)
        obj.save()


