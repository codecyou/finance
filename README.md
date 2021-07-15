# finance
个人记账程序/记账/支出/收入/还款/记录


version 1.0.4.1 修复bug  
    update：  
        1. 修复版本1.0.2和1.0.3中出现的“还款”，“借入”，“借出”等功能中无法定位id的bug，bug 原因：view.BaseFrame.locateNote方法中的selecet语句出现数据库中没有的字段（一级分类、二级分类等）  
        2. 修复详细查询中必须输入金额，而且严格匹配金额的bug  
            修复：  
                1）将view.QueryFrame中的money属性设为StringVar，这样不输入或者输入非纯数字就不会报错  
                2）在view.QueryFrame.searchNotes方法中对money进行类型转换，若不输入或者输入非纯数字，则置为None  
                3）在view.QueryFrame.searchNotes方法中拼接查询条件子语句sub_sql时，如果遇见money为None，则跳过，这样就会匹配所有金额  
        3. 修复详细查询中日期输入必须严格格式的bug，比如其他功能模块可以输入2021.7.15或者2021-7-15或者20210715甚至2021.7-15都会自动转成2021-07-15 而该模块必须输入严格格式  
            修复：添加一步：note_date = changeStrToDate(note_date)  # 自动转换为标准格式  
        4. 优化view.BackupFrame导出excel功能，导出文件时默认指定文件类型和文件名，优化使用体验  
        
 version 1.0.3 调整“新增标签模块”  
    update:  
        1. 调整“新增标签模块”，将新增标签模块从每个页面的按钮独立出来成为和支出收入等功能同级的一个单独标签页，并且在MainPage.reshow_infos方法中刷新各个模块页面最新下拉框值
            优化NewTagFrame，添加redisplayLabel方法，可以根据不同的单选项更新标签显示内容/备注/分类/上级分类  
        2. 新增view模块BackupFrame.get_ids_from_db 用于一次性从数据库获取所有id，title 减少后面恢复时一次次数据库查询  
        3. 新增view模块BackupFrame.get_id_from_result 直接从3中查询的result中直接查询id，并且如果支付方式，分类等在数据库中不存在的话会新建，避免原来程序直接置null导致数据丢失  
        
version 1.0.2 优化代码，修复bug  
    update:  
        1. 增加“查询”代码，实现多种条件的复杂查询  
        2. 优化excel导入代码  
        3. 优化其他部分代码  

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


