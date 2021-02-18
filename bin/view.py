import os
import sys
import sqlite3
import time
import traceback
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter.scrolledtext import ScrolledText
from tkinter import END
from tkinter.filedialog import askopenfilename, asksaveasfilename
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import settings
from core.Mytools import changeStrToDate
from core import excel
from core.logger import logger


class BaseFrame(tk.LabelFrame):
    """所有功能模块的父类"""
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        # 创建聊天记录查看页面
        self.root = ttk.LabelFrame(master, text='支出记录')  # 定义内部变量root
        self.pwin = master  # 父容器对象引用，方便后面调用父容器实例方法
        self.root.grid()
        self.select_id = tk.IntVar()  # 要定位的id  ，用于定位数据库中的记账记录
        self.current_id = None  # 用于记录当前选中id
        self.db_v = "v_payments_info"  # 数据库视图名称
        self.db_table = "payments"  # 数据库表名
        self.account = tk.StringVar()  # 账户下拉框数据
        self.seller = tk.StringVar()  # 商家/交易对象下拉框数据
        self.category_p = tk.StringVar()  # 类别下拉框数据,一级分类
        self.category_c = tk.StringVar()  # 类别下拉框数据，二级分类
        self.member = tk.StringVar()  # 成员/使用者下拉框数据
        self.title = tk.StringVar()  # 事项
        self.note_date = tk.StringVar()  # 日期
        self.remark = tk.StringVar()  # 备注
        self.money = tk.DoubleVar()  # 金额
        self.search_key = tk.StringVar()  # 搜索关键字
        self.search_mode = tk.StringVar()  # 搜索模式  字段
        self.search_mode.set("title")
        self.order_mode = tk.StringVar()  # 排序模式  id, note_date, money
        self.order_mode.set("id")
        self.order_option = tk.StringVar()  # 排序参数  asc 升序  desc 降序
        self.order_option.set("asc")
        self.entry_flag = tk.BooleanVar()  # 刷新输入区  True 每次提交完都会将输入区内容清空， 如果要重复输入重复日期 就很不方便
        self.entry_flag.set(True)
        # 链接数据库
        self.conn = sqlite3.connect(settings.DB_PATH)
        self.c = self.conn.cursor()
        # self.createPage()

    def createPage(self):
        self.f_top = ttk.Frame(self.root)
        self.f_title = ttk.Frame(self.root)
        self.f_content = ttk.Frame(self.root)
        self.f_bottom = ttk.Frame(self.root)
        self.f_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.f_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.f_title.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.f_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 标签
        ttk.Label(self.f_title, text="事项").grid(row=0, column=1)
        ttk.Label(self.f_title, text="日期").grid(row=0, column=2)  # 格式：'%Y-%m-%d %H:%M:%S'
        ttk.Label(self.f_title, text="备注").grid(row=0, column=3, columnspan=2)
        ttk.Label(self.f_title, text="金额").grid(row=0, column=5)
        ttk.Label(self.f_title, text="账户/支付方式").grid(row=2, column=1)
        ttk.Label(self.f_title, text="交易对象").grid(row=2, column=2)  # 格式：'%Y-%m-%d %H:%M:%S'

        self.entry_title = ttk.Entry(self.f_title, textvariable=self.title, width=20)
        self.entry_title.grid(row=1, column=1, sticky=tk.EW, padx=2)
        self.entry_date = ttk.Entry(self.f_title, textvariable=self.note_date, width=20)  # 输入事项框
        self.entry_date.grid(row=1, column=2, sticky=tk.EW, padx=2)
        self.entry_remark = ttk.Entry(self.f_title, textvariable=self.remark, width=40)  # 输入备注框
        self.entry_remark.grid(row=1, column=3, columnspan=2, sticky=tk.EW, padx=2)
        self.entry_money = ttk.Entry(self.f_title, textvariable=self.money, width=20)  # 输入金额框
        self.entry_money.grid(row=1, column=5, sticky=tk.EW, padx=2)
        self.buttun_create_note = ttk.Button(self.f_title, text="创建", command=self.addNote)  # 创建记账记录 按钮
        self.buttun_create_note.grid(row=1, column=6, sticky=tk.EW, padx=2)

        # 账户框
        self.chosen_account = ttk.Combobox(self.f_title, textvariable=self.account)
        self.chosen_account.grid(row=3, column=1, sticky=tk.EW, padx=2)

        # 交易对象框
        self.chosen_seller = ttk.Combobox(self.f_title, textvariable=self.seller)
        self.chosen_seller.grid(row=3, column=2, sticky=tk.EW, padx=2)

        # 创建标签签 按钮
        ttk.Button(self.f_title, text="新建标签", command=self.create_new_tag).grid(row=3, column=6, sticky=tk.EW, padx=2)

        self.label_notes_info = ttk.Label(self.f_content)  # 所有记录总数信息
        self.label_notes_info.grid(row=0, column=0, columnspan=2, pady=5)
        # 记录显示区
        # 详情
        self.txt_note = ScrolledText(self.f_content, wrap=tk.WORD, width=100, height=32)
        self.txt_note.grid(row=1, column=0)
        # 总体分析
        self.info_note = ScrolledText(self.f_content, wrap=tk.WORD, width=35, height=32)
        self.info_note.grid(row=1, column=1)
        self.f_radios = ttk.Frame(self.f_bottom)  # 防止单选项区域  即根据什么搜索的选项
        self.f_radios.grid(row=0, columnspan=9)
        ttk.Label(self.f_radios, text="设置:").grid(row=0, column=0)
        ttk.Radiobutton(self.f_radios, text="根据ID排序", value="id", variable=self.order_mode, command=self.searchNotes).grid(row=0, column=1)
        ttk.Radiobutton(self.f_radios, text="根据日期排序", value="note_date", variable=self.order_mode, command=self.searchNotes).grid(row=1, column=1)
        ttk.Radiobutton(self.f_radios, text="根据金额排序", value="money", variable=self.order_mode, command=self.searchNotes).grid(row=2, column=1)
        ttk.Radiobutton(self.f_radios, text="升序", value="asc", variable=self.order_option, command=self.searchNotes).grid(row=0, column=2)
        ttk.Radiobutton(self.f_radios, text="降序", value="desc", variable=self.order_option, command=self.searchNotes).grid(row=1, column=2)
        ttk.Radiobutton(self.f_radios, text="刷新输入区 ", value=True, variable=self.entry_flag).grid(row=0, column=3)
        ttk.Radiobutton(self.f_radios, text="不刷新输入区", value=False, variable=self.entry_flag).grid(row=1, column=3)

        ttk.Label(self.f_radios, text="搜索方式:").grid(row=4, column=0)
        ttk.Radiobutton(self.f_radios, text="根据事项", value="title", variable=self.search_mode).grid(row=4, column=1)
        ttk.Radiobutton(self.f_radios, text="根据日期", value="note_date", variable=self.search_mode).grid(row=4, column=2)
        ttk.Radiobutton(self.f_radios, text="根据备注", value="remark", variable=self.search_mode).grid(row=4, column=3)
        ttk.Radiobutton(self.f_radios, text="根据金额", value="money", variable=self.search_mode).grid(row=4, column=4)
        ttk.Radiobutton(self.f_radios, text="根据账户/支付方式", value="account", variable=self.search_mode).grid(row=4, column=5)
        ttk.Radiobutton(self.f_radios, text="根据交易方", value="seller", variable=self.search_mode).grid(row=4, column=6)

        ttk.Label(self.f_bottom, text="搜索内容:").grid(row=1, column=0)
        ttk.Entry(self.f_bottom, textvariable=self.search_key, width=50).grid(row=1, column=1, columnspan=4)
        ttk.Button(self.f_bottom, text="搜索", command=self.searchNotes).grid(row=1, column=5)
        ttk.Button(self.f_bottom, text="查看所有", command=self.showAll).grid(row=1, column=6)
        ttk.Label(self.f_bottom, text="定位编号:").grid(row=2, column=0)
        ttk.Entry(self.f_bottom, textvariable=self.select_id).grid(row=2, column=1)
        ttk.Button(self.f_bottom, text="定位", command=self.locateNote).grid(row=2, column=2)
        self.buttun_cancel = ttk.Button(self.f_bottom, text="取消修改", command=self.cancelUpdate)
        self.buttun_cancel.grid(row=2, column=4)
        ttk.Button(self.f_bottom, text="删除记录", command=self.delNote).grid(row=2, column=5)
        for child in self.f_radios.winfo_children():
            child.grid_configure(padx=2, pady=4, sticky=tk.EW)
        for child in self.f_bottom.winfo_children():
            child.grid_configure(padx=2, pady=4, sticky=tk.EW)

        # self.set_combox_values()
        self.showAll()

    def get_combox_values_from_db(self, table_name):
        """用于从数据库获取下拉框的值"""
        self.c.execute("select title from %s" % table_name)
        result = []
        # [('日常',), ('交通',), ('住房',)]
        for item in self.c.fetchall():
            result.append(item[0])
        return tuple(result)

    def set_combox_values(self):
        # 用于设置下拉框的values
        accounts = self.get_combox_values_from_db("accounts")
        sellers = self.get_combox_values_from_db("sellers")
        members = self.get_combox_values_from_db("members")
        self.chosen_account['values'] = accounts
        self.chosen_seller['values'] = sellers
        comboxs = [self.chosen_account, self.chosen_seller]
        for item in comboxs:
            item.current(0)  # 设置初始显示值，值为元组['values']的下标
            item.config(state='readonly')  # 设为只读模式

    def create_new_tag(self):
        """用于创建记账分类新标签"""
        NewTagFrame(self)

    def addNote(self):
        """新增/修改记账记录"""
        # list = [self.title, self.note_date, self.remark, self.money, self.account, self.seller]
        # for item in list:
        #     print(item.get(), end=" ")
        # print()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = self.note_date.get()
        note_date = changeStrToDate(note_date)
        if note_date is None:
            note_date = time.strftime('%Y-%m-%d', time.localtime())
            self.note_date.set(note_date)
        title = self.title.get()
        remark = self.remark.get()
        money = self.money.get()
        self.c.execute("select id from accounts where title=?", (self.account.get(),))
        account_id = self.c.fetchall()[0][0]
        self.c.execute("select id from sellers where title=?", (self.seller.get(),))
        seller_id = self.c.fetchall()[0][0]
        if not self.current_id:
            # 新增
            sql = "insert into %s(note_date, title, remark, money, account_id, seller_id, create_time) values(?,?,?,?,?,?,?)" % self.db_table
            self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id, time_now))
        else:
            # 修改
            sql = "update %s set note_date=?,title=?,remark=?,money=?,account_id=?,seller_id=?,modify_time=? where id=?" % self.db_table
            self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id, time_now, self.current_id))
        self.conn.commit()
        self.clearMsg()
        self.showAll()

    def showAll(self):
        """展示所有交易记录"""
        # print(self.db_v, self.db_table)
        # 显示交易分析汇总信息
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        self.c.execute("select count(money),sum(money),avg(money),max(money),min(money) from %s order by %s %s;" % (self.db_v, order_mode, order_key))
        result = self.c.fetchone()  # 总信息
        # print(result)
        self.info_note.delete("0.0", END)
        self.info_note.insert(tk.INSERT, "共进行了 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n\n" % result)
        show_dict = {"account": "按账户/支付方式 统计：", "seller": "按交易方 统计："}
        for item in ["account", "seller"]:
            sql = "select %s,count(money),sum(money),avg(money),max(money),min(money) from %s group by %s;" % (item, self.db_v, item)
            # print(sql)
            self.c.execute(sql)
            results = self.c.fetchall()
            self.info_note.insert(tk.INSERT, "\n%s\n" % show_dict[item])
            for result in results:
                self.info_note.insert(tk.INSERT, "%s 相关共 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n" % result)
        # 显示交易详情
        self.txt_note.delete("0.0", END)  # 清空显示区
        sql = "select id,note_date,title,remark,money,account,seller from %s order by %s %s;" % (self.db_v, order_mode, order_key)
        self.c.execute(sql)
        result = self.c.fetchall()
        for item in result:
            msg = "id:%s\n日期:%s, 事项:%s, 备注:%s, 金额:%s, \n账户/支付方式:%s, 交易方:%s\n\n" % item
            self.txt_note.insert(tk.INSERT, msg)
        self.clearMsg()
        self.label_notes_info.config(text="当前共有 %s 条记账记录！" % len(result))  # 显示记账记录数

    def searchNotes(self):
        """用于搜索便签"""
        # 获取搜索关键字
        search_key = self.search_key.get()  # 搜索词
        search_mode = self.search_mode.get()  # 搜索模式  “content” 事项和备注 “note_date” 时间
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        # 显示交易详情
        self.txt_note.delete("0.0", END)
        # 获取交易分析汇总信息
        sql = """select count(money),sum(money),avg(money),max(money),min(money) from %s
                where %s like ? order by %s %s;""" % (self.db_v, search_mode, order_mode, order_key)
        self.c.execute(sql, ("%%%s%%" % search_key,))
        result = self.c.fetchone()  # 总信息
        self.info_note.delete("0.0", END)
        self.info_note.insert(tk.INSERT, "共进行了 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n\n" % result)
        show_dict = {"account": "按账户/支付方式 统计：", "seller": "按交易方 统计："}
        for item in ["account", "seller"]:
            sql = """select %s,count(money),sum(money),avg(money),max(money),min(money) from %s
              where %s like ? group by %s""" % (item, self.db_v, search_mode, item)
            self.c.execute(sql, ("%%%s%%" % search_key,))
            results = self.c.fetchall()
            self.info_note.insert(tk.INSERT, "\n%s\n" % show_dict[item])
            for result in results:
                msg = "%s 相关共 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n" % result
                self.info_note.insert(tk.INSERT, msg)
        # 获取交易详情
        sql = """select id,note_date,title,remark,money,account,seller
                from %s where %s like ? order by %s %s;""" % (self.db_v, search_mode, order_mode, order_key)
        self.c.execute(sql, ("%%%s%%" % search_key,))
        # 显示交易详情信息
        result = self.c.fetchall()
        self.clearMsg()
        if not result:  # 没有搜索到结果
            self.label_notes_info.config(text="未搜索到符合条件的记账记录！")
        else:
            self.label_notes_info.config(text="共搜索到符合条件的 %s 条记账记录！" % len(result))  # 显示找到多少条
            for item in result:
                msg = "id:%s\n日期:%s, 事项:%s, 备注:%s, 金额:%s, \n账户/支付方式:%s, 交易方:%s\n\n" % item
                self.txt_note.insert(tk.INSERT, msg)

    def locateNote(self):
        """用于通过id定位便签并将其填充到对应控件内"""
        # 定位要修改的便签
        select_id = self.select_id.get()
        # print("select_id:", select_id)
        sql = "select id,note_date, title, remark, money, account, seller, category_p, category_c, member from %s where id=?" % self.db_v
        self.c.execute(sql, (select_id,))
        note_item = self.c.fetchone()
        # print("note_item:", note_item)
        if note_item:
            self.current_id = select_id  # 记录当前选中的id
            self.title.set(note_item[2])
            self.note_date.set(note_item[1])
            self.remark.set(note_item[3])
            self.money.set(note_item[4])
            self.account.set(note_item[5])
            self.seller.set(note_item[6])
            self.buttun_create_note.config(text="修改")
            self.txt_note.delete("0.0", END)
            self.info_note.delete("0.0", END)
            self.label_notes_info.config(text="正在修改id为%s的记账记录！" % select_id)
        else:
            self.clearMsg()
            self.txt_note.delete("0.0", END)
            self.info_note.delete("0.0", END)
            self.buttun_create_note.config(text="创建")
            self.label_notes_info.config(text="数据库中未找到id为:%s的记账记录！" % select_id)

    def cancelUpdate(self):
        """用于取消修改便签内容操作"""
        # 还原标签状态为新增便签
        self.clearMsg()
        self.txt_note.delete("0.0", END)
        self.buttun_create_note.config(text="创建")

    def delNote(self):
        """用于删除记账记录"""
        # 只进行逻辑删除
        sql = "update %s set is_delete=1 where id=?" % self.db_table
        self.c.execute(sql, (self.current_id,))
        self.conn.commit()
        print("删除id:%s 的记账记录！" % self.current_id)
        self.clearMsg()
        # 刷新结果
        self.showAll()

    def clearMsg(self):
        """用于将显示区的控件信息恢复最初状态"""
        self.current_id = None
        self.buttun_create_note.config(text="创建")
        self.label_notes_info.config(text="")
        if self.entry_flag.get() is True:
            self.title.set("")
            self.note_date.set("")
            self.remark.set("")
            self.money.set(0.0)
        # logger.debug("current_id:%s" % self.current_id)
        # logger.debug("entry_flag:%s" % self.entry_flag.get())


class BaseFrameFull(BaseFrame):
    """支出和收入功能模块的父类"""

    def createPage(self):
        super().createPage()
        ttk.Label(self.f_title, text="交易对象").grid(row=2, column=2)  # 格式：'%Y-%m-%d %H:%M:%S'
        ttk.Label(self.f_title, text="分类").grid(row=2, column=3, columnspan=2)
        ttk.Label(self.f_title, text="成员/使用者").grid(row=2, column=5)

        self.buttun_create_note = ttk.Button(self.f_title, text="创建", command=self.addNote)  # 创建记账记录 按钮
        self.buttun_create_note.grid(row=1, column=6, sticky=tk.EW, padx=2)

        # 类别框
        self.chosen_category1 = ttk.Combobox(self.f_title, textvariable=self.category_p)
        self.chosen_category1.grid(row=3, column=3, sticky=tk.EW, padx=2)
        self.chosen_category1.bind("<<ComboboxSelected>>", self.resetChosen_category2)  # 类别框2绑定与类别框1联动

        # 类别框2
        self.chosen_category2 = ttk.Combobox(self.f_title, textvariable=self.category_c)
        self.chosen_category2.grid(row=3, column=4, sticky=tk.EW, padx=2)

        # 成员/使用者框
        self.chosen_member = ttk.Combobox(self.f_title, textvariable=self.member)
        self.chosen_member.grid(row=3, column=5, sticky=tk.EW, padx=2)

        ttk.Radiobutton(self.f_radios, text="根据一级分类", value="category_p", variable=self.search_mode).grid(row=4, column=7)
        ttk.Radiobutton(self.f_radios, text="根据二级分类", value="category_c", variable=self.search_mode).grid(row=4, column=8)
        ttk.Radiobutton(self.f_radios, text="根据使用者", value="member", variable=self.search_mode).grid(row=4, column=9)

        self.set_combox_values()
        self.showAll()

    def get_combox_values_from_db(self, table_name):
        """用于从数据库获取下拉框的值"""
        self.c.execute("select title from %s" % table_name)
        result = []
        # [('日常',), ('交通',), ('住房',)]
        for item in self.c.fetchall():
            result.append(item[0])
        return tuple(result)

    def set_combox_values(self):
        # 用于设置下拉框的values
        accounts = self.get_combox_values_from_db("accounts")
        sellers = self.get_combox_values_from_db("sellers")
        members = self.get_combox_values_from_db("members")
        if self.db_table == "payments":
            category_table = "pay_categorys"
        else:
            category_table = "income_categorys"
        self.c.execute("select title from %s where pid is null" % category_table)
        categorys_p = []
        result = self.c.fetchall()
        if result:
            for item in result:
                categorys_p.append(item[0])
        categorys_p = tuple(categorys_p)
        # print("categorys_p:", categorys_p)
        if categorys_p:
            self.c.execute("select id from %s where title=?" % category_table, (categorys_p[0],))
            pid = self.c.fetchall()[0][0]
            # print("pid:", pid)
            self.c.execute("select title from %s where pid=?" % category_table, (pid,))
            categorys_c = []
            for item in self.c.fetchall():
                categorys_c.append(item[0])
            categorys_c = tuple(categorys_c)
            if not categorys_c:
                categorys_c = ("",)
        else:
            categorys_c = ("",)
        # print(categorys_c)

        self.chosen_account['values'] = accounts
        self.chosen_seller['values'] = sellers
        self.chosen_category1['values'] = categorys_p
        self.chosen_category2['values'] = categorys_c
        self.chosen_member['values'] = members
        comboxs = [self.chosen_account, self.chosen_seller, self.chosen_category1, self.chosen_category2, self.chosen_member]
        for item in comboxs:
            item.current(0)  # 设置初始显示值，值为元组['values']的下标
            item.config(state='readonly')  # 设为只读模式

    def resetChosen_category2(self, event):
        """用于实现类别框2与类别框1联动，根据类别框1所选值更新类别框2的值
        event 默认触发就会传递，无实际意义
        """
        self.chosen_category2.config(state="normal")  # 设为可写
        category_p = self.category_p.get()
        if self.db_table == "payments":
            category_table = "pay_categorys"
        else:
            category_table = "income_categorys"
        if category_p:
            self.c.execute("select id from %s where title=?" % category_table, (category_p,))
            pid = self.c.fetchone()[0]
            print("pid: type:%s ,value:%s" % (type(pid), pid))
            self.c.execute("select title from %s where pid is ?" % category_table, (pid,))
            categorys_c = []
            for item in self.c.fetchall():
                categorys_c.append(item[0])
            categorys_c = tuple(categorys_c)
            if not categorys_c:
                categorys_c = ("",)
        else:
            categorys_c = ("",)
        # print(categorys_c)
        self.chosen_category2["values"] = categorys_c
        self.chosen_category2.current(0)
        self.chosen_category2.config(state="readonly")  # 设为可写

    def addNote(self):
        """新增/修改记账记录"""
        # list = [self.title, self.note_date, self.remark, self.money, self.account, self.seller, self.category_p, self.category_c, self.member]
        # for item in list:
        #     print(item.get(), end=" ")
        # print()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = self.note_date.get()
        note_date = changeStrToDate(note_date)
        if note_date is None:
            note_date = time.strftime('%Y-%m-%d', time.localtime())
            self.note_date.set(note_date)
        title = self.title.get()
        remark = self.remark.get()
        money = self.money.get()
        self.c.execute("select id from accounts where title=?", (self.account.get(),))
        account_id = self.c.fetchall()[0][0]
        self.c.execute("select id from sellers where title=?", (self.seller.get(),))
        temp = self.c.fetchall()
        if temp:
            seller_id = temp[0][0]
        else:
            seller_id = None
        if self.db_table == "payments":
            category_table = "pay_categorys"
        else:
            category_table = "income_categorys"

        self.c.execute("select id from %s where title=?" % category_table, (self.category_p.get(),))
        category_pid = self.c.fetchall()[0][0]
        self.c.execute("select id from %s where title=? and pid=?" % category_table, (self.category_c.get(), category_pid))
        categorys_cid = self.c.fetchall()
        if categorys_cid:
            # 有内容
            category_cid = categorys_cid[0][0]
        else:
            # 数据库中无
            category_cid = None
            # category_cid = 0
        self.c.execute("select id from members where title=?", (self.member.get(),))
        member_id = self.c.fetchall()[0][0]
        if not self.current_id:
            # 新增
            sql = "insert into %s(note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id, create_time) values(?,?,?,?,?,?,?,?,?,?)" % self.db_table
            self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id, time_now))
        else:
            # 修改
            sql = "update %s set note_date=?,title=?,remark=?,money=?,account_id=?,seller_id=?,category_pid=?,category_cid=?,member_id=?,modify_time=? where id=?" % self.db_table
            self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id, time_now, self.current_id))
        self.conn.commit()
        self.clearMsg()
        self.showAll()

    def showAll(self):
        """展示所有交易记录"""
        # print(self.db_v, self.db_table)
        # 显示交易分析汇总信息
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        self.c.execute("select count(money),sum(money),avg(money),max(money),min(money) from %s order by %s %s;" % (self.db_v, order_mode, order_key))
        result = self.c.fetchone()  # 总信息
        # print(result)
        self.info_note.delete("0.0", END)
        self.info_note.insert(tk.INSERT, "共进行了 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n\n" % result)
        show_dict = {"account": "按账户/支付方式 统计：", "seller": "按交易方 统计：", "category_p": "按一级分类 统计：", "category_c": "按二级分类 统计：", "member": "按使用者 统计："}
        for item in ["account", "seller", "category_p", "category_c", "member"]:
            sql = "select %s,count(money),sum(money),avg(money),max(money),min(money) from %s group by %s;" % (item, self.db_v, item)
            # print(sql)
            self.c.execute(sql)
            results = self.c.fetchall()
            self.info_note.insert(tk.INSERT, "\n%s\n" % show_dict[item])
            for result in results:
                self.info_note.insert(tk.INSERT, "%s 相关共 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n" % result)
        # 显示交易详情
        self.txt_note.delete("0.0", END)  # 清空显示区
        sql = "select id,note_date,title,remark,money,account,seller,category_p,category_c,member from %s order by %s %s;" % (self.db_v, order_mode, order_key)
        self.c.execute(sql)
        result = self.c.fetchall()
        for item in result:
            msg = "id:%s\n日期:%s, 事项:%s, 备注:%s, 金额:%s, \n账户/支付方式:%s, 交易方:%s, 一级分类:%s, 二级分类:%s, 使用者:%s\n\n" % item
            self.txt_note.insert(tk.INSERT, msg)
        self.clearMsg()
        self.label_notes_info.config(text="当前共有 %s 条记账记录！" % len(result))  # 显示记账记录数

    def searchNotes(self):
        """用于搜索便签"""
        # 获取搜索关键字
        search_key = self.search_key.get()  # 搜索词
        search_mode = self.search_mode.get()  # 搜索模式  “content” 事项和备注 “note_date” 时间
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        # 显示交易详情
        self.txt_note.delete("0.0", END)
        # 获取交易分析汇总信息
        sql = """select count(money),sum(money),avg(money),max(money),min(money) from %s where %s like ? """ % (self.db_v, search_mode)
        self.c.execute(sql, ("%%%s%%" % search_key,))
        result = self.c.fetchone()  # 总信息
        self.info_note.delete("0.0", END)
        self.info_note.insert(tk.INSERT, "共进行了 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n\n" % result)
        show_dict = {"account": "按账户/支付方式 统计：", "seller": "按交易方 统计：", "category_p": "按一级分类 统计：",
                     "category_c": "按二级分类 统计：", "member": "按使用者 统计："}
        for item in ["account", "seller", "category_p", "category_c", "member"]:
            sql = """select %s,count(money),sum(money),avg(money),max(money),min(money) from %s
              where %s like ? group by %s""" % (item, self.db_v, search_mode, item)
            self.c.execute(sql, ("%%%s%%" % search_key,))
            results = self.c.fetchall()
            self.info_note.insert(tk.INSERT, "\n%s\n" % show_dict[item])
            for result in results:
                msg = "%s 相关共 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n" % result
                self.info_note.insert(tk.INSERT, msg)
        # 获取交易详情
        sql = """select id,note_date,title,remark,money,account,seller,category_p,category_c,member 
                from %s where %s like ? order by %s %s;""" % (self.db_v, search_mode, order_mode, order_key)
        logger.debug("搜索sql:%s " % sql)
        self.c.execute(sql, ("%%%s%%" % search_key,))
        # 显示交易详情信息
        result = self.c.fetchall()
        self.clearMsg()
        if not result:  # 没有搜索到结果
            self.label_notes_info.config(text="未搜索到符合条件的记账记录！")
        else:
            self.label_notes_info.config(text="共搜索到符合条件的 %s 条记账记录！" % len(result))  # 显示找到多少条
            for item in result:
                msg = "id:%s\n日期:%s, 事项:%s, 备注:%s, 金额:%s, \n账户/支付方式:%s, 交易方:%s, 一级分类:%s, 二级分类:%s, 使用者:%s\n\n" % item
                self.txt_note.insert(tk.INSERT, msg)

    def locateNote(self):
        """用于通过id定位便签并将其填充到对应控件内"""
        # 定位要修改的便签
        select_id = self.select_id.get()
        # print("select_id:", select_id)
        # sql = "select id,note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id from %s where id=?" % self.db_table
        sql = "select id,note_date, title, remark, money, account, seller, category_p, category_c, member from %s where id=?" % self.db_v
        self.c.execute(sql, (select_id,))
        note_item = self.c.fetchone()
        logger.debug(note_item)
        # print("note_item:", note_item)
        if note_item:
            self.current_id = select_id  # 记录当前选中的id
            self.title.set(note_item[2])
            self.note_date.set(note_item[1])
            self.remark.set(note_item[3])
            self.money.set(note_item[4])
            self.account.set(note_item[5])
            self.seller.set(note_item[6])
            self.category_p.set(note_item[7])
            self.category_c.set(note_item[8])
            self.member.set(note_item[9])
            self.buttun_create_note.config(text="修改")
            self.txt_note.delete("0.0", END)
            self.info_note.delete("0.0", END)
            self.label_notes_info.config(text="正在修改id为%s的记账记录！" % select_id)
        else:
            self.clearMsg()
            self.txt_note.delete("0.0", END)
            self.info_note.delete("0.0", END)
            self.buttun_create_note.config(text="创建")
            self.label_notes_info.config(text="数据库中未找到id为:%s的记账记录！" % select_id)


class IndexFrame(tk.LabelFrame):
    """首页/信息汇总页"""
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        # 创建聊天记录查看页面
        self.root = ttk.LabelFrame(master, text='信息汇总')  # 定义内部变量root
        self.pwin = master  # 父容器对象引用，方便后面调用父容器实例方法
        self.root.grid()
        # 链接数据库
        self.conn = sqlite3.connect(settings.DB_PATH)
        self.c = self.conn.cursor()
        self.createPage()
        self.show_infos()

    def createPage(self):
        # 标签
        ttk.Label(self.root, text="支出", width=40).grid(row=0, column=0, padx=2, pady=4)
        ttk.Label(self.root, text="收入", width=40).grid(row=0, column=1, padx=2, pady=4)
        ttk.Label(self.root, text="借入", width=40).grid(row=0, column=2, padx=2, pady=4)
        ttk.Label(self.root, text="借出", width=40).grid(row=2, column=0, padx=2, pady=4)
        ttk.Label(self.root, text="还款", width=40).grid(row=2, column=1, padx=2, pady=4)
        ttk.Label(self.root, text="记录", width=40).grid(row=2, column=2, padx=2, pady=4)
        ttk.Button(self.root, text="刷新", command=self.show_infos).grid(row=12)
        # 内容
        self.l_payment = ttk.Label(self.root)
        self.l_income = ttk.Label(self.root)
        self.l_borrow = ttk.Label(self.root)
        self.l_lend = ttk.Label(self.root)
        self.l_repayment = ttk.Label(self.root)
        self.l_note = ttk.Label(self.root)
        self.labels = [self.l_payment, self.l_income, self.l_borrow, self.l_lend, self.l_repayment, self.l_note]
        row = 1
        col = 0
        for item in self.labels:
            item.grid(row=row, column=col)
            col += 1
            if col == 3:
                row += 2
                col = 0

    def show_infos(self, event=None):
        # 显示交易分析汇总信息
        # print("show_infos 函数运行，event:", event)
        db_views = ["v_payments_info", "v_incomes_info", "v_borrows_info", "v_lends_info", "v_repayments_info"]
        count = 0
        # 显示交易汇总信息
        for db_v in db_views:
            self.c.execute("select count(money),sum(money),avg(money),max(money),min(money) from %s" % db_v)
            result = self.c.fetchone()  # 总信息
            self.labels[count].config(text="共进行了 %s 笔交易\n交易总金额:%s \n平均交易金额:%s \n最大交易金额:%s \n最小交易金额:%s \n" % result)
            count += 1
        # 显示记录汇总信息
        self.c.execute("select id,note_date,title,remark,remark2 from v_notes_info;")
        result = self.c.fetchall()
        self.l_note.config(text="当前共有 %s 条记事记录！" % len(result))  # 显示记录数


class PaymentFrame(BaseFrameFull):
    """支出记录"""
    def __init__(self, master=None):
        super(PaymentFrame, self).__init__(master)
        self.createPage()


class IncomeFrame(BaseFrameFull):
    """收入记录"""
    def __init__(self, master=None):
        super(IncomeFrame, self).__init__(master)
        self.root.config(text="收入记录")
        self.db_v = "v_incomes_info"  # 数据库视图名称
        self.db_table = "incomes"  # 数据库表名
        self.createPage()


class BorrowFrame(BaseFrame):
    """借入记录"""
    def __init__(self, master=None):
        super(BorrowFrame, self).__init__(master)
        self.root.config(text="借入记录")
        self.db_v = "v_borrows_info"  # 数据库视图名称
        self.db_table = "borrows"  # 数据库表名
        self.createPage()
        self.set_combox_values()


class LendFrame(BaseFrame):
    """借出记录"""
    def __init__(self, master=None):
        super().__init__(master)
        self.root.config(text="借出记录")
        self.db_v = "v_lends_info"  # 数据库视图名称
        self.db_table = "lends"  # 数据库表名
        self.createPage()
        self.set_combox_values()


class RepaymentFrame(BaseFrame):
    """还款记录"""
    def __init__(self, master=None):
        super().__init__(master)
        self.root.config(text="还款记录")
        self.db_v = "v_repayments_info"  # 数据库视图名称
        self.db_table = "repayments"  # 数据库表名
        self.createPage()
        self.set_combox_values()


class NewTagFrame(tk.LabelFrame):
    """用于创建新的类别标签"""
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        # 创建聊天记录查看页面
        self.pwin = master  # 父容器对象引用，方便后面调用父容器实例方法
        self.temp = ttk.LabelFrame(self.pwin.pwin, text='新增标签')  # 创建新Frame用于新增标签
        self.pwin.root.grid_forget()  # 关闭上一页显示
        self.temp.grid()  # 显示修改标签页
        # 链接数据库
        self.conn = sqlite3.connect(settings.DB_PATH)
        self.c = self.conn.cursor()
        self.addChosenTag()

    def addChosenTag(self):
        """用于新增下拉框的标签"""
        ttk.Label(self.temp, text="选择要新增的标签类型：").grid(row=0, column=0)
        mode = tk.StringVar()  # 要新增的标签类型
        mode.set("pay_categorys")
        title = tk.StringVar()  # 要新增的标签title
        remark = tk.StringVar()  # 要新增的标签描述，如果新增类别（category）标签 则进行转换为pid
        ttk.Radiobutton(self.temp, text="账户/支付方式", value="accounts", variable=mode).grid(row=0, column=1)
        ttk.Radiobutton(self.temp, text="交易对象", value="sellers", variable=mode).grid(row=0, column=2)
        ttk.Radiobutton(self.temp, text="支出分类", value="pay_categorys", variable=mode, width=20).grid(row=0, column=3)
        ttk.Radiobutton(self.temp, text="收入分类", value="income_categorys", variable=mode, width=20).grid(row=0, column=4)
        ttk.Radiobutton(self.temp, text="成员/使用者", value="members", variable=mode, width=20).grid(row=0, column=5)
        ttk.Label(self.temp, text="请输入要新增的信息:").grid(row=1, column=0)
        self.label_title = ttk.Label(self.temp, text="内容/新增分类")
        self.label_title.grid(row=1, column=1)
        self.label_remark = ttk.Label(self.temp, text="备注/所属上级分类")
        self.label_remark.grid(row=1, column=2)
        ttk.Entry(self.temp, textvariable=title).grid(row=2, column=1)
        ttk.Entry(self.temp, textvariable=remark).grid(row=2, column=2)
        ttk.Button(self.temp, text="新增", command=lambda: self.doAddChosenTag(mode, title, remark)).grid(row=3, column=1)
        ttk.Button(self.temp, text="返回上一页", command=self.returnPrePage).grid(row=3, column=4)
        # 批量调整控件布局
        for child in self.temp.winfo_children():
            child.grid_configure(sticky=tk.EW, padx=2, pady=5)

    def returnPrePage(self):
        """返回上一页"""
        self.temp.grid_forget()
        self.pwin.root.grid()
        self.pwin.set_combox_values()  # 刷新下拉框数据

    def doAddChosenTag(self, mode, title, remark):
        """将获取到的信息插入数据库"""
        mode = mode.get()
        title = title.get()
        remark = remark.get()
        # 判断是否已存在数据库
        self.c.execute("select count(*) from %s where title=?" % mode, (title,))
        if self.c.fetchone()[0]:
            print("%s已存在%s数据库中" % (title, mode))
            mBox.showwarning("失败", message="数据已存在数据库！")
            return
        # 新增标签，写入数据库表数据
        if mode in ["pay_categorys", "income_categorys"]:
            self.c.execute("select id from %s where title=?" % mode, (remark,))
            pid = self.c.fetchall()
            if pid:
                pid = pid[0][0]
            else:
                pid = None
            # print("pid, type:%s, value:%s" % (type(pid), pid))
            self.c.execute("insert into %s (title, pid) values (?,?)" % mode, (title, pid))
            self.conn.commit()
        else:
            sql_dict = {"accounts": "insert into accounts (title, remark) values (?,?)",
                        "sellers": "insert into sellers (title, remark) values (?,?)",
                        "members": "insert into members (title, remark) values (?,?)"}
            self.c.execute(sql_dict[mode], (title, remark))
            self.conn.commit()
        mBox.showinfo("成功", message="新建标签成功！")


class NoteFrame(tk.LabelFrame):
    """记录模块"""
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        # 创建聊天记录查看页面
        self.root = ttk.LabelFrame(master, text='记录')  # 定义内部变量root
        self.pwin = master  # 父容器对象引用，方便后面调用父容器实例方法
        self.root.grid()
        self.select_id = tk.IntVar()  # 要定位的id  ，用于定位数据库中的记账记录
        self.current_id = None  # 用于记录当前选中id
        self.db_v = "v_notes_info"  # 数据库视图名称
        self.db_table = "notes"  # 数据库表名
        self.title = tk.StringVar()  # 事项
        self.note_date = tk.StringVar()  # 日期
        self.remark = tk.StringVar()  # 操作后余量
        self.remark2 = tk.StringVar()  # 额外备注
        self.search_key = tk.StringVar()  # 搜索关键字
        self.search_mode = tk.StringVar()  # 搜索模式  字段
        self.search_mode.set("title")
        self.order_mode = tk.StringVar()  # 排序模式  id, note_date, money
        self.order_mode.set("id")
        self.order_option = tk.StringVar()  # 排序参数  asc 升序  desc 降序
        self.order_option.set("asc")
        self.entry_flag = tk.BooleanVar()  # 刷新输入区  True 每次提交完都会将输入区内容清空， 如果要重复输入重复日期 就很不方便
        self.entry_flag.set(True)
        # 链接数据库
        self.conn = sqlite3.connect(settings.DB_PATH)
        self.c = self.conn.cursor()
        self.createPage()

    def createPage(self):
        f_top = ttk.Frame(self.root)
        f_title = ttk.Frame(self.root)
        f_content = ttk.Frame(self.root)
        f_bottom = ttk.Frame(self.root)
        f_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        f_title.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        f_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 标签
        ttk.Label(f_title, text="事项").grid(row=0, column=1)
        ttk.Label(f_title, text="时间").grid(row=0, column=2)  # 格式：'%Y-%m-%d %H:%M:%S'
        ttk.Label(f_title, text="内容").grid(row=0, column=3, columnspan=2)
        ttk.Label(f_title, text="额外备注").grid(row=0, column=5)

        self.entry_title = ttk.Entry(f_title, textvariable=self.title, width=20)
        self.entry_title.grid(row=1, column=1, sticky=tk.EW, padx=2)
        self.entry_date = ttk.Entry(f_title, textvariable=self.note_date, width=20)  # 输入事项框
        self.entry_date.grid(row=1, column=2, sticky=tk.EW, padx=2)
        self.entry_remark = ttk.Entry(f_title, textvariable=self.remark, width=40)  # 输入备注框
        self.entry_remark.grid(row=1, column=3, columnspan=2, sticky=tk.EW, padx=2)
        self.entry_remark2 = ttk.Entry(f_title, textvariable=self.remark2, width=40)  # 输入额外备注框
        self.entry_remark2.grid(row=1, column=5, sticky=tk.EW, padx=2)
        self.buttun_create_note = ttk.Button(f_title, text="创建", command=self.addNote)  # 创建记账记录 按钮
        self.buttun_create_note.grid(row=1, column=6, sticky=tk.EW, padx=2)

        self.label_notes_info = ttk.Label(f_content)  # 所有记录总数信息
        self.label_notes_info.grid(row=0, column=0, columnspan=2, pady=5)
        # 记录显示区
        self.txt_note = ScrolledText(f_content, wrap=tk.WORD, width=130, height=38)
        self.txt_note.grid(row=1, column=0)

        f_radios = ttk.Frame(f_bottom)  # 防止单选项区域  即根据什么搜索的选项
        f_radios.grid(row=0, columnspan=9)
        ttk.Label(f_radios, text="设置:").grid(row=0, column=0)
        ttk.Radiobutton(f_radios, text="根据ID排序", value="id", variable=self.order_mode, command=self.searchNotes).grid(row=0, column=1)
        ttk.Radiobutton(f_radios, text="根据日期排序", value="note_date", variable=self.order_mode, command=self.searchNotes).grid(row=1, column=1)
        ttk.Radiobutton(f_radios, text="升序", value="asc", variable=self.order_option, command=self.searchNotes).grid(row=0, column=2)
        ttk.Radiobutton(f_radios, text="降序", value="desc", variable=self.order_option, command=self.searchNotes).grid(row=1, column=2)
        ttk.Radiobutton(f_radios, text="刷新输入区", value=True, variable=self.entry_flag).grid(row=0, column=3)
        ttk.Radiobutton(f_radios, text="不刷新输入区", value=False, variable=self.entry_flag).grid(row=1, column=3)
        ttk.Label(f_radios, text="搜索方式:").grid(row=4, column=0)
        ttk.Radiobutton(f_radios, text="根据事项", value="title", variable=self.search_mode).grid(row=4, column=1)
        ttk.Radiobutton(f_radios, text="根据日期", value="note_date", variable=self.search_mode).grid(row=4, column=2)
        ttk.Radiobutton(f_radios, text="根据备注", value="remark", variable=self.search_mode).grid(row=4, column=1)
        ttk.Radiobutton(f_radios, text="根据额外备注", value="remark2", variable=self.search_mode).grid(row=4, column=3)

        ttk.Label(f_bottom, text="搜索内容:").grid(row=1, column=0)
        ttk.Entry(f_bottom, textvariable=self.search_key, width=50).grid(row=1, column=1, columnspan=4)
        ttk.Button(f_bottom, text="搜索", command=self.searchNotes).grid(row=1, column=5)
        ttk.Button(f_bottom, text="查看所有", command=self.showAll).grid(row=1, column=6)
        ttk.Label(f_bottom, text="定位编号:").grid(row=2, column=0)
        ttk.Entry(f_bottom, textvariable=self.select_id).grid(row=2, column=1)
        ttk.Button(f_bottom, text="定位", command=self.locateNote).grid(row=2, column=2)
        self.buttun_cancel = ttk.Button(f_bottom, text="取消修改", command=self.cancelUpdate)
        self.buttun_cancel.grid(row=2, column=4)
        ttk.Button(f_bottom, text="删除记录", command=self.delNote).grid(row=2, column=5)
        for child in f_radios.winfo_children():
            child.grid_configure(padx=2, pady=4, sticky=tk.EW)
        for child in f_bottom.winfo_children():
            child.grid_configure(padx=2, pady=4, sticky=tk.EW)
        self.showAll()

    def addNote(self):
        """新增/修改记账记录"""
        # list = [self.title, self.note_date, self.remark, self.remark2]
        # for item in list:
        #     print(item.get(), end=" ")
        # print()
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = self.note_date.get()
        note_date = changeStrToDate(note_date)
        if note_date is None:
            note_date = time.strftime('%Y-%m-%d', time.localtime())
            self.note_date.set(note_date)
        title = self.title.get()
        remark = self.remark.get()
        remark2 = self.remark2.get()
        if not self.current_id:
            # 新增
            sql = "insert into %s(note_date, title, remark, remark2, create_time) values(?,?,?,?,?)" % self.db_table
            self.c.execute(sql, (note_date, title, remark, remark2, time_now))
        else:
            # 修改
            sql = "update %s set note_date=?,title=?,remark=?,remark2=?,modify_time=? where id=?" % self.db_table
            self.c.execute(sql, (note_date, title, remark, remark2, time_now, self.current_id))
        self.conn.commit()
        self.clearMsg()
        self.showAll()

    def showAll(self):
        """展示所有交易记录"""
        # 显示详情
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        self.txt_note.delete("0.0", END)  # 清空显示区
        sql = "select id,note_date,title,remark,remark2 from %s order by %s %s;" % (self.db_v, order_mode, order_key)
        self.c.execute(sql)
        result = self.c.fetchall()
        for item in result:
            msg = "id:%s\n日期:%s, 事项:%s, \n备注:%s, 额外备注:%s\n\n" % item
            self.txt_note.insert(tk.INSERT, msg)
        self.clearMsg()
        self.label_notes_info.config(text="当前共有 %s 条记事记录！" % len(result))  # 显示记录数

    def searchNotes(self):
        """用于搜索便签"""
        # 获取搜索关键字
        search_key = self.search_key.get()  # 搜索词
        search_mode = self.search_mode.get()  # 搜索模式  “content” 事项和备注 “note_date” 时间
        order_mode = self.order_mode.get()  # 根据什么排序
        order_key = self.order_option.get()  # 排序
        # 显示交易详情
        self.txt_note.delete("0.0", END)
        sql = """select id,note_date,title,remark,remark2 from %s where %s like ?  order by %s %s;""" % (self.db_v, search_mode, order_mode, order_key)
        self.c.execute(sql, ("%%%s%%" % search_key,))
        result = self.c.fetchall()
        self.clearMsg()
        if not result:  # 没有搜索到结果
            self.label_notes_info.config(text="未搜索到符合条件的记录！")
        else:
            self.label_notes_info.config(text="共搜索到符合条件的 %s 条记录！" % len(result))  # 显示找到多少条
            for item in result:
                msg = "id:%s\n日期:%s, 事项:%s, \n备注:%s, 额外备注:%s\n\n" % item
                self.txt_note.insert(tk.INSERT, msg)

    def locateNote(self):
        """用于通过id定位便签并将其填充到对应控件内"""
        # 定位要修改的便签
        select_id = self.select_id.get()
        # print("select_id:", select_id)
        sql = "select id, note_date, title, remark, remark2 from %s where id=?" % self.db_table
        self.c.execute(sql, (select_id,))
        note_item = self.c.fetchone()
        # print("note_item:", note_item)
        if note_item:
            self.current_id = select_id  # 记录当前选中的id
            self.title.set(note_item[2])
            self.note_date.set(note_item[1])
            self.remark.set(note_item[3])
            self.remark2.set(note_item[4])
            self.buttun_create_note.config(text="修改")
            self.txt_note.delete("0.0", END)
            self.label_notes_info.config(text="正在修改id为%s的记录！" % select_id)
        else:
            self.clearMsg()
            self.txt_note.delete("0.0", END)
            self.buttun_create_note.config(text="创建")
            self.label_notes_info.config(text="数据库中未找到id为:%s的记录！" % select_id)

    def cancelUpdate(self):
        """用于取消修改便签内容操作"""
        # 还原标签状态为新增便签
        self.clearMsg()
        self.txt_note.delete("0.0", END)
        self.buttun_create_note.config(text="创建")

    def delNote(self):
        """用于删除记账记录"""
        # 只进行逻辑删除
        sql = "update %s set is_delete=1 where id=?" % self.db_table
        self.c.execute(sql, (self.current_id,))
        self.conn.commit()
        print("删除id:%s 的记录！" % self.current_id)
        self.clearMsg()
        # 刷新结果
        self.showAll()

    def clearMsg(self):
        """用于将显示区的控件信息恢复最初状态"""
        self.current_id = None
        self.buttun_create_note.config(text="创建")
        self.label_notes_info.config(text="")
        if self.entry_flag.get() is True:
            self.title.set("")
            self.note_date.set("")
            self.remark.set("")
            self.remark2.set("")


class BackupFrame(tk.LabelFrame):
    """用于从excel文件导入"""
    def __init__(self, master=None):
        tk.LabelFrame.__init__(self, master)
        # 创建聊天记录查看页面
        self.root = ttk.LabelFrame(master, text='备份与恢复')  # 定义内部变量root
        self.pwin = master  # 父容器对象引用，方便后面调用父容器实例方法
        self.root.grid()
        self.top = ttk.Frame(self.root)
        self.top.grid()
        self.option = ttk.Frame(self.root)
        self.option.grid()
        # 链接数据库
        self.conn = sqlite3.connect(settings.DB_PATH)
        self.c = self.conn.cursor()
        # excel 文件路径
        self.excel_path1 = tk.StringVar()  # 导入文件路径
        self.excel_path2 = tk.StringVar()  # 导出文件路径
        ttk.Label(self.top, text="excel文件路径:").grid(row=0, column=0)
        ttk.Entry(self.top, textvariable=self.excel_path1, width=80).grid(row=0, column=1)
        ttk.Button(self.top, text="浏览", command=self.select_filepath_1).grid(row=0, column=2)
        ttk.Button(self.top, text="导入到数据库", command=self.insert_db).grid(row=0, column=3)

        ttk.Label(self.top, text="导出路径:").grid(row=1, column=0)
        ttk.Entry(self.top, textvariable=self.excel_path2, width=80).grid(row=1, column=1)
        ttk.Button(self.top, text="浏览", command=self.select_filepath_2).grid(row=1, column=2)
        ttk.Button(self.top, text="导出到excel", command=self.export_excel).grid(row=1, column=3)

    def select_filepath_1(self):
        """用于通过浏览按钮获取导入文件路径"""
        file_path = askopenfilename()
        self.excel_path1.set(file_path)

    def select_filepath_2(self):
        """用于通过浏览按钮获取导出文件路径"""
        file_path = asksaveasfilename()
        self.excel_path2.set(file_path)

    def insert_db(self):
        """用于将数据从excel表中插入到数据库"""
        file_path = self.excel_path1.get()
        logger.info("导入的excel文件路径:%s" % file_path)
        # sheet_names = ["支出", "收入", "借入", "借出", "还款", "记录"]
        try:
            # 读取 excel文件内容
            logger.info("正在读取excel文件内容")
            r = excel.ReadExcel(file_path)
            result = r.read_data()
            logger.debug("result: %s" % result)
            func_dict = {"支出": self.insert_db_payment,
                         "收入": self.insert_db_income,
                         "借入": self.insert_db_borrow,
                         "借出": self.insert_db_lend,
                         "还款": self.insert_db_repayment,
                         "记录": self.insert_db_note
                         }
            for sheet in result:
                self.data_list = result[sheet]
                for data in self.data_list:
                    func_dict[sheet](data)
        except Exception as e:
            print(traceback.print_exc())
            logger.error("导入excel数据出错%s" % e)
            mBox.showerror("失败", message="从%s 恢复到数据库失败！" % file_path)
        else:
            logger.info("导入excel数据成功!")
            mBox.showinfo("成功", message="从%s 恢复到数据库完成！" % file_path)

    def get_id_db(self, sql, paras):
        """用于从数据库中查找id
        sql :sql语句
        paras : 元组参数
        """
        self.c.execute(sql, paras)
        results = self.c.fetchall()
        if results:
            return results[0][0]
        else:
            return

    def get_data(self, key, data):
        """data : excel中每一行的数据字典"""
        # 从excel读取的数据中提取所需数据 用于避免 比如excel"收入"表中没有"交易方"这一列导致直接data["交易方"] 报KeyError: '交易方'
        if key in data:
            return data[key]
        else:
            return

    def insert_db_payment(self, data):
        # 用于将excel文件中支出的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = data["事项"]
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = data["备注"]
        money = data["支出金额"]
        account = data["支出途径"]
        seller = data["交易方"]
        category_p = data["一级分类"]
        category_c = data["二级分类"]
        member = data["对象"]
        account_id = self.get_id_db("select id from accounts where title=?", (account,))
        seller_id = self.get_id_db("select id from sellers where title=?", (seller,))
        category_pid = self.get_id_db("select id from pay_categorys where title=?", (category_p,))
        category_cid = self.get_id_db("select id from pay_categorys where title=? and pid=?", (category_c, category_pid))
        member_id = self.get_id_db("select id from members where title=?", (member,))
        sql = "insert into payments(note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id,create_time,modify_time) values(?,?,?,?,?,?,?,?,?,?,?)"
        self.c.execute(sql, (
            note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id,create_time,modify_time))
        self.conn.commit()

    def insert_db_income(self, data):
        # 用于将excel文件中收入的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = data["事项"]
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = self.get_data("备注", data)
        money = self.get_data("收入金额", data)
        account = self.get_data("收入途径", data)
        seller = self.get_data("交易方", data)
        category_p = self.get_data("一级分类", data)
        category_c = self.get_data("二级分类", data)
        member = self.get_data("备注", data)
        account_id = self.get_id_db("select id from accounts where title is ?", (account,))
        seller_id = self.get_id_db("select id from sellers where title is ?", (seller,))
        category_pid = self.get_id_db("select id from income_categorys where title is ?", (category_p,))
        categorys_cid = self.get_id_db("select id from income_categorys where title is ? and pid is ?",
                                       (category_c, category_pid))
        if categorys_cid:
            # 有内容
            category_cid = categorys_cid[0][0]
        else:
            # 数据库中无
            category_cid = None
        # category_cid = 0
        member_id = self.get_id_db("select id from members where title=?", (member,))
        sql = "insert into incomes(note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id,create_time,modify_time) values(?,?,?,?,?,?,?,?,?,?,?)"
        self.c.execute(sql, (
            note_date, title, remark, money, account_id, seller_id, category_pid, category_cid, member_id,create_time,modify_time))
        self.conn.commit()

    def insert_db_borrow(self, data):
        # 用于将excel文件中支出的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = data["事项"]
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = data["备注"]
        money = data["金额"]
        account = data["账户"]
        seller = data["交易方"]
        account_id = self.get_id_db("select id from accounts where title=?", (account,))
        seller_id = self.get_id_db("select id from sellers where title=?", (seller,))
        sql = "insert into borrows(note_date, title, remark, money, account_id, seller_id,create_time,modify_time) values(?,?,?,?,?,?,?,?)"
        self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id,create_time,modify_time))
        self.conn.commit()

    def insert_db_lend(self, data):
        # 用于将excel文件中支出的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = data["事项"]
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = data["备注"]
        money = data["金额"]
        account = data["账户"]
        seller = data["交易方"]
        account_id = self.get_id_db("select id from accounts where title=?", (account,))
        seller_id = self.get_id_db("select id from sellers where title=?", (seller,))
        sql = "insert into lends(note_date, title, remark, money, account_id, seller_id,create_time,modify_time) values(?,?,?,?,?,?,?,?)"
        self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id,create_time,modify_time))
        self.conn.commit()

    def insert_db_repayment(self, data):
        # 用于将excel文件中支出的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = data["事项"]
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = data["备注"]
        money = data["金额"]
        account = data["账户"]
        seller = data["交易方"]
        account_id = self.get_id_db("select id from accounts where title=?", (account,))
        seller_id = self.get_id_db("select id from sellers where title=?", (seller,))
        sql = "insert into repayments(note_date, title, remark, money, account_id, seller_id,create_time,modify_time) values(?,?,?,?,?,?,?,?)"
        self.c.execute(sql, (note_date, title, remark, money, account_id, seller_id,create_time,modify_time))
        self.conn.commit()

    def insert_db_note(self, data):
        # 用于将excel文件中支出的信息记录到数据库中
        create_time = self.get_data("创建时间", data)
        modify_time = self.get_data("修改时间", data)
        if not create_time:
            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        note_date = changeStrToDate(data["日期"])
        title = self.get_data("事项", data)
        if title is None:
            # 防止空单元格导致写入数据库报错
            return
        remark = self.get_data("充值后剩余", data)
        if remark:
            remark = "充值后" + remark
        remark2 = self.get_data("额外备注", data)
        sql = "insert into notes(note_date, title, remark, remark2,create_time,modify_time) values(?,?,?,?,?,?)"
        self.c.execute(sql, (note_date, title, remark, remark2, create_time, modify_time))
        self.conn.commit()

    def export_excel(self):
        """从数据库获取所有交易记录并写出到excel文件"""
        # 显示交易详情
        file_path = self.excel_path2.get()
        logger.info("导出的excel文件路径:%s" % file_path)
        result = {}
        sql = "select note_date,title,money,account,remark,seller,category_p,category_c,member,create_time,modify_time from v_payments_info order by note_date;"
        self.c.execute(sql)
        result["支出"] = self.c.fetchall()
        sql = "select note_date,title,money,account,remark,seller,category_p,category_c,member,create_time,modify_time from v_incomes_info order by note_date;"
        self.c.execute(sql)
        result["收入"] = self.c.fetchall()
        sql = "select note_date,title,money,account,remark,seller,create_time,modify_time from v_borrows_info order by note_date;"
        self.c.execute(sql)
        result["借入"] = self.c.fetchall()
        sql = "select note_date,title,money,account,remark,seller,create_time,modify_time from v_lends_info order by note_date;"
        self.c.execute(sql)
        result["借出"] = self.c.fetchall()
        sql = "select note_date,title,money,account,remark,seller,create_time,modify_time from v_repayments_info order by note_date;"
        self.c.execute(sql)
        result["还款"] = self.c.fetchall()
        sql = "select note_date,title,remark,remark2,create_time,modify_time from v_notes_info order by note_date;"
        self.c.execute(sql)
        result["记录"] = self.c.fetchall()
        # print(result)
        logger.info("导出数据到excel文件:%s" % file_path)
        w = excel.WriteExcel(file_path, result)
        w.write_data()
        logger.info("导出数据到excel成功！")
        mBox.showinfo("成功", message="导出到%s 完成！" % file_path)


