# coding:utf-8
import qrcode
from PIL import Image
import matplotlib.pyplot as plt

i = qrcode.make("天王盖地虎")
i.save("zhao.png")
print("\33[1;31mcreate QRcode finish\33[0m")
# qr.make_image(fill_color="black", back_color="white")

# "晋级版"
qr = qrcode.QRCode(
    version=2,  # 控制二维码的大小：(25*25)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # ERROR_CORRECT_H:30%的字码可被容错
    box_size=8,  # 控制二维码中每个小格子包含的像素数
    border=4  # 控制边框(二维码与图片边界的距离)包含的格子数(默认为4)
)
qr.add_data("月落乌啼上满天，江枫渔火对愁眠，姑苏城外寒山寺，夜半钟声到客船。")  # 添加数据
qr.make(fit=True)
img = qr.make_image()  # 生成二维码
img = img.convert("RGBA")

# 添加logo，打开logo照片
icon = Image.open("hai.png")
# 获取图片的宽高
img_w, img_h = img.size
# 参数设置logo的大小
factor = 6
size_w = int(img_w / factor)
size_h = int(img_h / factor)
icon_w, icon_h = icon.size
if icon_w > size_w:
    icon_w = size_w
if icon_h > size_h:
    icon_h = size_h
# 重新设置logo的尺寸
icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
# 得到画图的x，y坐标，居中显示
w = int((img_w - icon_w) / 2)
h = int((img_h - icon_h) / 2)
# 黏贴logo照
img.paste(icon, (w, h), mask=None)
# 终端显示图片
plt.imshow(img)
plt.show()

img.save("ok.png")  # 保存二维码
img.show()  # 显示二维码
