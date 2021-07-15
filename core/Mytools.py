import re


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
