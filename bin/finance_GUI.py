import tkinter as tk

import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from bin.MainPage import *


# 创建GUI窗体
root = tk.Tk()
root.title('finance by wyl')
# root.iconbitmap(r'C:\Users\Pro\Desktop\test.ico')
MainPage(root)
root.mainloop()
