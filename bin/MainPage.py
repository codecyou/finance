from bin.view import *   # 菜单栏对应的各个子页面
from tkinter import ttk


class MainPage(object):
    def __init__(self, master=None):
        self.win = master  # 定义内部变量root
        # self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)  # 绑定窗口关闭事件，防止计时器正在工作导致数据丢失

        # 设置窗口大小
        winWidth = 1000
        winHeight = 800
        # 获取屏幕分辨率
        screenWidth = self.win.winfo_screenwidth()
        screenHeight = self.win.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置窗口初始位置在屏幕居中
        self.win.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        self.page = None  # 用于标记功能界面
        self.createPage()

    def createPage(self):
        # 设置主框架标签页
        # Tab Control introduced here --------------------------------------
        tabControl = ttk.Notebook(self.win)  # Create Tab Control

        tab1 = ttk.Frame(tabControl)  # Create a tab
        tabControl.add(tab1, text='  主页  ')  # Add the tab

        tab2 = ttk.Frame(tabControl)  # Add a second tab
        tabControl.add(tab2, text='  支出  ')  # Make second tab visible

        tab3 = ttk.Frame(tabControl)  # Add a third tab
        tabControl.add(tab3, text='  收入  ')  # Make second tab visible

        tab4 = ttk.Frame(tabControl)
        tabControl.add(tab4, text='  借入  ')

        tab5 = ttk.Frame(tabControl)
        tabControl.add(tab5, text='  借出  ')

        tab6 = ttk.Frame(tabControl)
        tabControl.add(tab6, text='  还款  ')

        tab7 = ttk.Frame(tabControl)
        tabControl.add(tab7, text='  记录  ')

        tab8 = ttk.Frame(tabControl)
        tabControl.add(tab8, text='  备份与恢复  ')


        tabControl.pack(expand=1, fill="both")  # Pack to make visible
        # ~ Tab Control introduced here -----------------------------------------

        # monty1 = IndexFrame(tab1)
        self.monty1 = IndexFrame(tab1)
        self.monty1.grid(column=0, row=0, padx=8, pady=4)

        self.monty2 = PaymentFrame(tab2)
        self.monty2.grid(column=0, row=0, padx=8, pady=4)

        self.monty3 = IncomeFrame(tab3)
        self.monty3.grid(column=0, row=0, padx=8, pady=4)

        self.monty4 = BorrowFrame(tab4)
        self.monty4.grid(column=0, row=0, padx=8, pady=4)

        self.monty5 = LendFrame(tab5)
        self.monty5.grid(column=0, row=0, padx=8, pady=4)

        self.monty6 = RepaymentFrame(tab6)
        self.monty6.grid(column=0, row=0, padx=8, pady=4)

        self.monty7 = NoteFrame(tab7)
        self.monty7.grid(column=0, row=0, padx=8, pady=4)

        monty8 = BackupFrame(tab8)
        monty8.grid(column=0, row=0, padx=8, pady=4)

        # 绑定标签栏 鼠标左键事件 用于每次点击 主页标签都能得到最新的汇总信息
        tabControl.bind("<Button-1>", self.reshow_infos)  # 调用方法获取最新汇总信息

    def reshow_infos(self, event=None):
        # 刷新显示各个页面最新信息
        self.monty1.show_infos()
        self.monty2.showAll()
        self.monty3.showAll()
        self.monty4.showAll()
        self.monty5.showAll()
        self.monty6.showAll()
        self.monty7.showAll()

