from PIL import Image, ImageTk
import time
import datetime
import random
import os
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import settings


def resize(w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
    """调整图像大小"""
    # 对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
    w, h = pil_image.size  # 获取图像的原始大小
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


def choice_img():
    """用于随机选取展示图像"""
    image_list = []  # 遍历图片路径
    for root, dirs, files in os.walk(settings.IMAGES_PATH):
        for file in files:
            image_list.append(os.path.join(root, file))
    return random.choice(image_list)  # 随机选取一张图像


def calDate(date1, date2):
    """获取两个时间差多少天"""
    # date1 = time.strptime(date1, "%Y-%m-%d")
    # date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
    # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    # date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    # date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return (date2 - date1).days


def changeStrToDate(time_str):
    """用于将字符串转为日期 三种时间格式20210201,2021.2.1,2021-2-1"""
    # print("time_str:", time_str)
    if not time_str:
        return
    time_a = re.search(r"(\d+)[-\.](\d+)[-\.](\d+)", time_str.strip())
    if time_a:
        # 匹配时间格式2021.2.1,2021-2-1
        time_y = time_a.group(1)
        time_m = time_a.group(2)
        time_d = time_a.group(3)
    # 匹配时间格式20210201
    elif (time_str.isdigit()) and (len(time_str) == 8):
        time_y = time_str[0:4]
        time_m = time_str[4:6]
        time_d = time_str[6:]
    else:
        return
    # 筛选格式
    if (not len(time_y) == 4) or (not (int(time_m) in range(1, 13))) or (not (int(time_d) in range(1, 32))):
        return
    # 判断月份
    if (time_m in ['4', '6', '9', '11']) and (time_d == "31"):
        return
    if time_m == '2':
        if time_d in ['30', '31']:
            return
        if (time_d == '29') and ((int(time_y) % 4) != 0):
            return
    # 将"2021-2-1" 转为 "2021-02-01"
    # if len(time_m) < 2:
    #     time_m = '0' + time_m
    time_m = time_m.zfill(2)
    time_d = time_d.zfill(2)
    new_time_str = "-".join((time_y, time_m, time_d))
    return new_time_str


def changeStrToTime(time_str):
    """用于将字符串转为时间 三种时间格式20210201,2021.2.1,2021-2-1"""
    # print("time_str:", time_str)
    time_a = re.search(r"(\d+)[-\.](\d+)[-\.](\d+)", time_str.strip())
    if time_a:
        # 匹配时间格式2021.2.1,2021-2-1
        time_y = time_a.group(1)
        time_m = time_a.group(2)
        time_d = time_a.group(3)
    # 匹配时间格式20210201
    elif (time_str.isdigit()) and (len(time_str) == 8):
        time_y = time_str[0:4]
        time_m = time_str[4:6]
        time_d = time_str[6:]
    else:
        return
    # 筛选格式
    if (not len(time_y) == 4) or (not (int(time_m) in range(1, 13))) or (not (int(time_d) in range(1, 32))):
        return
    # 判断月份
    if (time_m in ['4', '6', '9', '11']) and (time_d == "31"):
        return
    if time_m == '2':
        if time_d in ['30', '31']:
            return
        if (time_d == '29') and ((int(time_y) % 4) != 0):
            return
    # 将"2021-2-1" 转为 "2021-02-01"
    # if len(time_m) < 2:
    #     time_m = '0' + time_m
    time_m = time_m.zfill(2)
    time_d = time_d.zfill(2)
    new_time_str = "-".join((time_y, time_m, time_d))
    return new_time_str


def remake_time_human(temp_time):
    """用于将时间从秒数转化为可读性强的 x天x小时x分钟x秒
    :param temp_time: 时间（秒数）
    """
    time_msg = "%.2f秒" % temp_time
    if temp_time > 60:  # 计算分钟
        cal_time_min = int(temp_time // 60)
        cal_time_sec = temp_time - cal_time_min * 60  # 计算秒数
        time_msg = "%s分钟%.2f秒" % (cal_time_min, cal_time_sec)
        if cal_time_min > 60:  # 计算小时
            cal_time_hour = int(cal_time_min // 60)
            cal_time_min = cal_time_min - cal_time_hour * 60  # 重新计算小时
            time_msg = "%s小时%s分钟%.2f秒" % (cal_time_hour, cal_time_min, cal_time_sec)
            if cal_time_hour > 24:  # 计算天数
                cal_time_day = int(cal_time_hour // 24)
                cal_time_hour = cal_time_hour - cal_time_day * 24  # 重新计算小时
                time_msg = "%s天%s小时%s分钟%.2f秒" % (cal_time_day, cal_time_hour, cal_time_min, cal_time_sec)
                if cal_time_day > 365:  # 计算天数
                    cal_time_year = int(cal_time_day // 365)
                    cal_time_day = cal_time_day - cal_time_year * 365  # 重新计算天数
                    time_msg = "%s年%s天%s小时%s分钟%.2f秒" % (cal_time_year, cal_time_day, cal_time_hour, cal_time_min, cal_time_sec)
    return time_msg


def remake_time_human2(temp_time):
    """用于将时间从秒数转化为可读性强的 x天x小时x分钟x秒,本方法最多显示到小时数
    :param temp_time: 时间（秒数）
    """
    time_msg = "%.2f秒" % temp_time
    if temp_time > 60:  # 计算分钟
        cal_time_min = int(temp_time // 60)
        cal_time_sec = temp_time - cal_time_min * 60  # 计算秒数
        time_msg = "%s分钟%.2f秒" % (cal_time_min, cal_time_sec)
        if cal_time_min > 60:  # 计算小时
            cal_time_hour = int(cal_time_min // 60)
            cal_time_min = cal_time_min - cal_time_hour * 60  # 重新计算小时
            time_msg = "%s小时%s分钟%.2f秒" % (cal_time_hour, cal_time_min, cal_time_sec)
    return time_msg


def remake_time_sec(temp_time):
    """用于将时间从 x天x小时x分钟x秒 转化为秒数
    :param temp_time: 时间（秒数）
    """
    time_msg = 0  # 结果
    temp_time = temp_time.replace(' ', '')  # 去除空格
    time_sec = re.search(r'([0-9\.]+)秒', temp_time)
    time_min = re.search(r'([0-9]+)分钟', temp_time)
    time_hour = re.search(r'([0-9]+)小时', temp_time)
    time_day = re.search(r'([0-9]+)天', temp_time)  # 匹配天

    if time_day:
        print(time_day)
        time_msg = time_msg + float(time_day.group(1)) * 24 * 60 * 60
    if time_hour:
        time_msg = time_msg + float(time_hour.group(1)) * 60 * 60
    if time_min:
        time_msg = time_msg + float(time_min.group(1)) * 60
    if time_sec:
        time_msg = time_msg + float(time_sec.group(1))
    return time_msg
