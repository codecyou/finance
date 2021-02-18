# 用于配置

import os
import json
from core import create_db


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")  # 保存数据相关的目录
LOG_DIR = os.path.join(BASE_DIR, "log")  # 保存日志的目录
# configFile = os.path.join(BASE_DIR, 'conf', 'config.json')  # 配置文件路径

LOG_PATH = os.path.join(LOG_DIR, "info.log")  # 日志文件
DB_PATH = os.path.join(DB_DIR, "finance.db")  # 数据库文件


def my_init():
    """用于初始化程序运行环境"""
    # 创建目录
    for item in [DB_DIR, LOG_DIR]:
        if not os.path.exists(item):
            os.makedirs(item)
    # 创建数据库并初始化
    if not os.path.exists(DB_PATH):
        create_db.create()


# 初始化程序环境
my_init()
