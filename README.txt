finance 1.0
说明编写于2021-2-11
程序目录结构：

│  README.txt    # 说明文档
│
├─bin    # 执行目录
│      finance_GUI.py   # 程序执行文件
│      MainPage.py   # 程序视图
│      view.py  # 程序视图
│
├─conf  # 配置目录
│      settings.py  # 程序配置文件
│
├─core  # 程序功能模块目录
│      create_db.py  # 创建数据库结构模块
│      excel.py  # 读写excel模块
│      init_db.py  # 初始化数据库表数据模块
│      logger.py  # 日志模块
│      Mytools.py  # 通用方法模块
│
├─db  # 数据库文件目录
│      finance.db  # 数据库文件
│
└─log  # 日志目录
        info.log  # 程序日志

使用说明:
1.程序所需第三方包openpyxl
安装 pip install openpyxl

2.运行方式 python finance_GUI.py

注意事项:
    1.程序输入日期的时候支持 20210211,2021-02-11,2021-2-11,2021.2.11 等输入方式,程序会自动检验日期是否正确并且输出"xxxx-xx-xx"日期格式
    2.由于tkinter entry控件在中文输入法状态下无法输入小数点,故输入金额时请务必注意切换输入法为英文状态




程序模块说明：
view.py
BaseFrame 为所有记账功能的父类
BaseFrameFull 为"支出"和"收入"功能的父类
IndexFrame 为主页类
PaymentFrame 为支出类
IncomeFrame 为收入类
BorrowFrame 为借入类
LendFrame 为借出类
RepaymentFrame 为还款类
NoteFrame 为记录类
NewTagFrame 为新建标签类
BackupFrame 为备份恢复类