"""
author: zhao
time: 2020-10-30
env： python3.6
this is a cookies
"""
from tkinter import *
import tkinter.messagebox
root = Tk()
root.title("1111111111")

root.attributes('-toolwindow', 0,  # 工具栏样式
                '-alpha', 0.1,  # 透明度
                '-fullscreen', 1,  # 全屏
                '-topmost', 1)  # 置顶
root.overrideredirect(True)  # 去掉标题栏
Button(root, text=" ", command=root.quit, width=4).place(x=14, y=14)
tkinter.messagebox.showinfo(title="惊喜", message='开心吧！')
root.mainloop()
