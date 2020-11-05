"""
time: 2020-10-26
author: zhao
env: python3.6
this is tkinter exercise
"""
import pickle
import tkinter.messagebox
from tkinter import *

# 初始化
root = Tk()
root.title("Welcome to xxx")
root.resizable(False, False)  # 窗口大小可调性
# 窗口居中
# 获取屏幕 宽、高
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
# 计算 x, y 位置
x = (ws - 400) / 2
y = (hs - 500) / 2
root.geometry('%dx%d+%d+%d' % (400, 500, x, y))

# 设置图标
icon = PhotoImage(file="hai.png")
root.iconphoto(True, icon)

# 添加画布，导入图片
canvas = Canvas(root, bg="green", width=400, height=124)
image = PhotoImage(file="hai.png")
canvas.create_image(200, 10, anchor="n", image=image)
canvas.pack()

# 输入框名
Label(root, text="Welcome", font=("Arial", 16)).pack()
Label(root, text='User name:', font=('Arial', 14)).place(x=10, y=170)
Label(root, text='Password:', font=('Arial', 14)).place(x=10, y=210)
# 输入框
user_name = StringVar()
user_pwd = StringVar()
user_name.set('example@163.com')
username_entry = Entry(root, textvariable=user_name, font=('Arial', 12))
userpwd_entry = Entry(root, textvariable=user_pwd, font=('Arial', 12), show="*")
username_entry.place(x=120, y=174)
userpwd_entry.place(x=120, y=214)


# TODO 登录
def user_login():
    # 获取用户名和用户密码
    username = username_entry.get()
    userpwd = userpwd_entry.get()
    print("name: {}, pwd: {}".format(username, userpwd))  # 打印数据

    # 第一次不存在，创建管理员账号
    try:
        with open("user_info.pickle", "rb") as u_f:
            user_info = pickle.load(u_f)
            print(user_info)
    except Exception as e:
        print("\33[1;31m FileNotFoundError \33[0m")
        print("\33[1;31mError:\33[0m", e)
        # 没有用户则创建一个管理员账号
        with open("user_info.pickle", "wb") as u_f:
            user_info = {"admin": "admin"}
            pickle.dump(user_info, u_f)
            tkinter.messagebox.showinfo(title='Welcome', message='init success')
            user_register()

    # 有数据存在，校验用户
    if username in user_info:  # 用户已经存在，校验密码
        if userpwd == user_info[username]:
            tkinter.messagebox.showinfo(title='Welcome', message='Hello ' + username + "！")
        else:
            tkinter.messagebox.showerror(title='Error', message='Error, your password is wrong, try again.')
    # 没有该用户，弹出提示框，并且询问是否要创建用户
    else:
        is_sign_up = tkinter.messagebox.askyesno(title='Welcome！ ', message='You have not register. Register now?')
        if is_sign_up:
            user_register()


# TODO 注册
def user_register():
    # 注册逻辑
    def register_account():
        # 获取参数
        username = new_name_entry.get()
        pwd_new = new_pwd_entry.get()
        again_pwd = again_pwd_entry.get()

        # 输入不能为空
        if not username or not pwd_new or not again_pwd:
            tkinter.messagebox.showwarning(title='warn', message='name or password not empty!')
            # user_register()

        # 校验
        try:
            with open("user_info.pickle", "rb") as u_f:
                user_info = pickle.load(u_f)
                print(user_info)
        except:
            # 创建一个管理员账号
            with open("user_info.pickle", "wb") as u_f:
                user_info = {"admin": "admin"}
                pickle.dump(user_info, u_f)
                tkinter.messagebox.showinfo(title='Welcome', message='init success')

        # 校验用户名
        if username in user_info:
            return

        # TODO 校验

    # 定义长在窗口上的窗口（注册框）
    register_window = Toplevel(root)
    register_window.geometry('%dx%d+%d+%d' % (300, 200, x-15, y-15))
    register_window.title('register')
    # 弹窗一直保持在主窗口之上(置顶)
    register_window.attributes("-topmost", 1)

    # 注册信息
    name_new = StringVar()
    pwd_new = StringVar()
    again_pwd = StringVar()
    name_new.set('example@python.com')

    # 注册框名
    Label(register_window, text='User name: ').place(x=10, y=10)
    Label(register_window, text='password : ').place(x=10, y=50)
    Label(register_window, text='again pwd: ').place(x=10, y=90)
    # 输入框
    new_name_entry = Entry(register_window, textvariable=name_new, font=('Arial', 12))
    new_pwd_entry = Entry(register_window, textvariable=pwd_new, font=('Arial', 12), show="*")
    again_pwd_entry = Entry(register_window, textvariable=again_pwd, font=('Arial', 12), show="*")
    new_name_entry.place(x=90, y=14)
    new_pwd_entry.place(x=90, y=54)
    again_pwd_entry.place(x=90, y=94)

    # 按钮
    btn_comfirm_sign_up = Button(register_window, text='提交', command=register_account)
    btn_comfirm_sign_up.place(x=180, y=120)


# 按钮
login_button = Button(root, text="登录", command=user_login).place(x=120, y=243)
btn_sign_up = Button(root, text='注册', command=user_register).place(x=200, y=243)
# 循环主窗口
root.mainloop()
