# 用于向数据库中插入数据

import sqlite3
import os


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(base_dir, "db")
conn = sqlite3.connect(os.path.join(db_dir, "finance.db"))
print("Opened database successfully")
c = conn.cursor()

# 创建账户表
accounts_table = '''insert into accounts (title) values (?);'''

# 创建商家/交易对象表
sellers_table = '''insert into sellers (title) values (?);'''

# 创建类别表
pay_categorys_table = '''insert into pay_categorys (title) values (?);'''
income_categorys_table = '''insert into income_categorys (title) values (?);'''

# 创建成员/消费者/使用者表
members_table = '''insert into members (title) values (?);'''


accounts = ["微信支付", "支付宝", "小号微信支付", "京东支付", "云闪付", "现金"]
sellers = ["京东", "便利商超", "淘宝", "苏宁", "京东到家", "美团", "饿了么", "其他"]
pay_categorys = ["日常", "交通", "住房", "医疗", "通讯", "人情往来", "科技", "特殊", "娱乐", "经营"]
income_categorys = ["工资", "退款", "费用报销"]
members = ["小家", "大家", "店"]

for item in accounts:
    c.execute(accounts_table, (item,))
for item in sellers:
    c.execute(sellers_table, (item,))
for item in pay_categorys:
    c.execute(pay_categorys_table, (item,))
for item in income_categorys:
    c.execute(income_categorys_table, (item,))
for item in members:
    c.execute(members_table, (item,))

pay_categorys_cs = [("购物", 1), ("餐饮", 1), ("理发", 1)]
for item in pay_categorys_cs:
    c.execute("insert into pay_categorys (title, pid) values (?,?)", item)

print("数据插入完成！")

conn.commit()
c.close()
conn.close()
