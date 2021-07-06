# finance
个人记账程序/记账/支出/收入/还款/记录
finance 1.0
程序目录结构：

│ README.txt # 说明文档
│
├─bin # 执行目录
│ finance_GUI.py # 程序执行文件
│ MainPage.py # 程序视图
│ view.py # 程序视图
│
├─conf # 配置目录
│ settings.py # 程序配置文件
│
├─core # 程序功能模块目录
│ create_db.py # 创建数据库结构模块
│ excel.py # 读写excel模块
│ init_db.py # 初始化数据库表数据模块
│ logger.py # 日志模块
│ Mytools.py # 通用方法模块
│
├─db # 数据库文件目录
│ finance.db # 数据库文件
│
└─log # 日志目录
info.log # 程序日志

使用说明:
1.程序所需第三方包openpyxl
安装 pip install openpyxl

2.运行方式 python finance_GUI.py

注意事项:
1.程序输入日期的时候支持 20210211,2021-02-11,2021-2-11,2021.2.11 等输入方式,程序会自动检验日期是否正确并且输出”xxxx-xx-xx”日期格式
2.由于tkinter entry控件在中文输入法状态下无法输入小数点,故输入金额时请务必注意切换输入法为英文状态


程序界面使用说明：
详见项目下：程序使用说明文件夹
![界面说明](https://github.com/codecyou/finance/blob/main/%E7%A8%8B%E5%BA%8F%E8%AF%B4%E6%98%8E/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E1%202021-02-11_000314.jpg)

![搜索](https://github.com/codecyou/finance/blob/main/%E7%A8%8B%E5%BA%8F%E8%AF%B4%E6%98%8E/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E2%E4%B9%8B%E6%90%9C%E7%B4%A2%202021-02-11_001222.jpg)

![修改](https://github.com/codecyou/finance/blob/main/%E7%A8%8B%E5%BA%8F%E8%AF%B4%E6%98%8E/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E3%E4%B9%8B%E4%BF%AE%E6%94%B9%E5%88%A0%E9%99%A4%E8%AE%B0%E5%BD%95%202021-02-11_002143.jpg)

![新增标签](https://github.com/codecyou/finance/blob/main/%E7%A8%8B%E5%BA%8F%E8%AF%B4%E6%98%8E/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E4%E4%B9%8B%E6%96%B0%E5%A2%9E%E6%A0%87%E7%AD%BE%202021-02-11_002812.jpg)

![备份与恢复](https://github.com/codecyou/finance/blob/main/%E7%A8%8B%E5%BA%8F%E8%AF%B4%E6%98%8E/%E7%95%8C%E9%9D%A2%E8%AF%B4%E6%98%8E5%E4%B9%8B%E5%A4%87%E4%BB%BD%E4%B8%8E%E6%81%A2%E5%A4%8D%202021-02-11_003542.jpg)


