# 用于创建数据库 及表结构 及视图

import sqlite3
import os
try:
    from conf import settings
except Exception:
    print("from conf import settings 失败！")

# 创建支出表
payments_table = '''CREATE TABLE if not exists payments(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100),
        money FLOAT NOT NULL,
        account_id INT ,
        seller_id INT ,
        category_pid INT ,
        category_cid INT ,
        member_id INT ,
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建收入表
incomes_table = '''CREATE TABLE if not exists incomes(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100),
        money FLOAT NOT NULL,
        account_id INT ,
        seller_id INT ,
        category_pid INT ,
        category_cid INT ,
        member_id INT ,
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建借入表
borrows_table = '''CREATE TABLE if not exists borrows(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100),
        money FLOAT NOT NULL,
        account_id INT ,
        seller_id INT ,
        category_pid INT ,
        category_cid INT ,
        member_id INT ,
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建借出表
lends_table = '''CREATE TABLE if not exists lends(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100),
        money FLOAT NOT NULL,
        account_id INT ,
        seller_id INT ,
        category_pid INT ,
        category_cid INT ,
        member_id INT ,
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建还款表
repayments_table = '''CREATE TABLE if not exists repayments(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100),
        money FLOAT NOT NULL,
        account_id INT ,
        seller_id INT ,
        category_pid INT ,
        category_cid INT ,
        member_id INT ,
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建成员/消费者/使用者表
notes_table = '''CREATE TABLE if not exists notes(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        note_date TEXT NOT NULL,
        title VARCHAR(50) NOT NULL, -- 记录操作 比如冲水30吨
        remark VARCHAR(100), -- 记录操作后剩余量 比如冲水后 还有40吨水
        remark2 VARCHAR(200), -- 记录其他备注事项
        create_time TEXT NOT NULL,
        modify_time TEXT,
        is_delete bit default 0
        );'''

# 创建账户表
accounts_table = '''CREATE TABLE if not exists accounts(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100)
        );'''

# 创建商家/交易对象表
sellers_table = '''CREATE TABLE if not exists sellers(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100)
        );'''

# 创建类别表
# 支出类别
pay_categorys_table = '''CREATE TABLE if not exists pay_categorys(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        title VARCHAR(50) NOT NULL,
        pid INT
        );'''
# 收入类别
income_categorys_table = '''CREATE TABLE if not exists income_categorys(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        title VARCHAR(50) NOT NULL,
        pid INT
        );'''

# 创建成员/消费者/使用者表
members_table = '''CREATE TABLE if not exists members(
        id INTEGER PRIMARY KEY   AUTOINCREMENT NOT NULL,
        title VARCHAR(50) NOT NULL,
        remark VARCHAR(100)
        );'''


tables = [payments_table, incomes_table, borrows_table, lends_table, repayments_table, notes_table,
          accounts_table, sellers_table, pay_categorys_table, income_categorys_table, members_table]


# 创建视图
v_payments_info = """create view  if not exists v_payments_info as
      select p.id,p.note_date,p.title,p.remark,p.money,a.title as account,s.title as seller,
      c_p.title as category_p,c_c.title as category_c,m.title as member,p.create_time,p.modify_time 
      from payments as p left join accounts as a on p.account_id = a.id
      left join sellers as s on p.seller_id = s.id
      left join pay_categorys as c_p on p.category_pid = c_p.id
      left join pay_categorys as c_c on p.category_cid = c_c.id
      left join members as m on p.member_id = m.id where is_delete=0;
      """

v_incomes_info = """create view  if not exists v_incomes_info as
      select p.id,p.note_date,p.title,p.remark,p.money,a.title as account,s.title as seller,
      c_p.title as category_p,c_c.title as category_c,m.title as member,p.create_time,p.modify_time 
      from incomes as p left join accounts as a on p.account_id = a.id
      left join sellers as s on p.seller_id = s.id
      left join income_categorys as c_p on p.category_pid = c_p.id
      left join income_categorys as c_c on p.category_cid = c_c.id
      left join members as m on p.member_id = m.id where is_delete=0;
      """

v_borrows_info = """create view if not exists v_borrows_info as
      select p.id,p.note_date,p.title,p.remark,p.money,a.title as account,s.title as seller
      ,p.create_time,p.modify_time 
      from borrows as p left join accounts as a on p.account_id = a.id
      left join sellers as s on p.seller_id = s.id
      where is_delete=0;
      """

v_lends_info = """create view if not exists v_lends_info as
      select p.id,p.note_date,p.title,p.remark,p.money,a.title as account,s.title as seller
      ,p.create_time,p.modify_time 
      from lends as p left join accounts as a on p.account_id = a.id
      left join sellers as s on p.seller_id = s.id
      where is_delete=0;
      """

v_repayments_info = """create view  if not exists v_repayments_info as
      select p.id,p.note_date,p.title,p.remark,p.money,a.title as account,s.title as seller
      ,p.create_time,p.modify_time 
      from repayments as p left join accounts as a on p.account_id = a.id
      left join sellers as s on p.seller_id = s.id
      where is_delete=0;
      """

v_notes_info = """create view if not exists v_notes_info as select * from notes where is_delete=0"""

views = [v_payments_info, v_incomes_info, v_borrows_info, v_lends_info, v_repayments_info, v_notes_info]


def create():
    # 用于创建数据库表结构
    conn = sqlite3.connect(os.path.join(settings.DB_PATH))
    print("Opened database successfully")
    c = conn.cursor()
    # 创建表结构
    for item in tables:
        c.execute(item)
    conn.commit()
    print("创建数据库表结构完成！")
    # 创建视图
    for item in views:
        c.execute(item)
    print("创建视图完成！")

    # 初始化插入表数据
    # 初始化账户表
    accounts_table = '''insert into accounts (title) values (?);'''

    # 初始化商家/交易对象表
    sellers_table = '''insert into sellers (title) values (?);'''

    # 初始化类别表
    pay_categorys_table = '''insert into pay_categorys (title) values (?);'''
    income_categorys_table = '''insert into income_categorys (title) values (?);'''

    # 初始化成员/消费者/使用者表
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


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base_dir, "db")
    conn = sqlite3.connect(os.path.join(db_dir, "finance.db"))
    print("Opened database successfully")
    c = conn.cursor()
    # 创建表结构
    for item in tables:
        c.execute(item)
    conn.commit()
    print("创建数据库表结构完成！")
    # 创建视图
    for item in views:
        c.execute(item)
    print("创建视图完成！")
    conn.commit()
    c.close()
    conn.close()
