# Import Modules
import time

import pygame as pg
import sys, os
from pygame.locals import *
import tkinter.messagebox


# init tkinter messagebox method
root = tkinter.Tk()
root.withdraw()  # mainloop window hide

# Check
if not pg.font:
    print("Warning, font disabled!!!")
    tkinter.messagebox.showwarning(title="Warning", message="Warning, font disabled!!!")
if not pg.mixer:
    print("Warning, mixer disabled!!!")
    tkinter.messagebox.showwarning(title="Warning", message="Warning, mixer disabled!!!")


# TODO Loading resources
def load_image(name, colorkey=None):  # Load image
    fullname = os.path.join("data", name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):  # Load sound
    class NoneSound:
        def play(self): pass

    if not pg.mixer:
        return NoneSound
    fullname = os.path.join("data", name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error as message:
        print("Cannot load sound:", fullname)
        raise SystemExit(message)
    return sound


# Game object
class Fist(pg.sprite.Sprite):  # 拳头
    """在屏幕上握紧拳头，跟随鼠标移动"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # 初始化基类
        self.image, self.rect = load_image("fist.bmp", -1)
        self.punching = 0

    def update(self, *args, **kwargs):  # 根据鼠标移动拳头
        pos = pg.mouse.get_pos()  # 获取鼠标位置
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):  # 是否击中敌人，打出拳头
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)  # bool

    def unpunch(self):  # 收回拳头
        self.punching = 0


class Chimp(pg.sprite.Sprite):
    """在屏幕上移动一个猴子，当被拳头打中时发生改变"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # 首先确保初始化基类
        self.image, self.rect = load_image("chimp.bmp", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()  # 显示屏幕大小
        self.rect.topleft = 10, 34
        self.move = 2
        self.dizzy = 0

    def update(self):  # 根据猴子的状态，刷新每一帧页面
        if self.dizzy:
            self._spin()  # 旋转
        else:
            self._walk()  # 行走
            # print("ok")
        # print(self.dizzy)

    def _walk(self):  # 行走方法，猴子在屏幕上行走，最后旋转
        newpos = self.rect.move((self.move, 0))
        # print(self.area)
        # print(newpos)
        if not self.area.contains(newpos):
            # print("=====================================")
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)  # 垂直和水平翻转函数对图像进行镜像
            self.rect = newpos

    def _spin(self):  # 旋转猴子
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        # 重复旋转相同的图像，质量会越来越差.我们确保新图像的中心与旧图像的中心相匹配，所以它会旋转
        self.rect = self.image.get_rect(center=center)

    def punched(self):  # 确认改变
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image  # 生成副本


def start_game():
    # init everything
    pg.init()  # 初始化pygame
    screen = pg.display.set_mode((568, 90))  # 设置屏幕大小
    pg.display.set_caption('Monkey Fever')  # 设置窗口名
    pg.mouse.set_visible(0)  # 鼠标可见

    background = pg.Surface(screen.get_size())  # 创建一个跟窗口一样大的新表面
    background = background.convert()  # 替代
    background.fill((250, 250, 250))  # 设置背景色,填充

    if pg.font:
        font = pg.font.Font(None, 36)
        # render函数创建一个适合文本大小的新表面,渲染创建反锯齿文本(为了一个漂亮的光滑的外观)，并使用深灰色。
        text = font.render("strike monkey", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2)
        # 最后，我们blit (blit就像复制或粘贴)的文本到背景图像
        background.blit(text, textpos)

    # 在pygame中，对显示表面的更改不会立即可见。flip()函数,简单地处理整个窗口区域，并处理单缓冲和双缓冲表面。
    screen.blit(background, (0, 0))
    pg.display.flip()

    # start
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp()
    fist = Fist()
    clock = pg.time.Clock()  # 时钟对象将用于帮助控制我们的游戏的帧率,确保它不会运行得太快
    allsprites = pg.sprite.RenderPlain((fist, chimp))

    flag = False
    while True:
        clock.tick(80)
        for event in pg.event.get():
            if event.type == QUIT:  # 退出
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:  # 鼠标事件（按下）
                if fist.punch(chimp):
                    punch_sound.play().set_volume(0.1)  # punch
                    # print(punch_sound.get_volume())
                    chimp.punched()
                else:
                    if not flag:
                        whiff_sound.play().set_volume(0.2)  # miss
                        flag = True
                        start_time = time.time()
                    elif time.time() - start_time >= whiff_sound.get_length() - 0.1:
                        flag = False
                        whiff_sound.play().set_volume(0.2)
                    # print(whiff_sound.get_volume(),"===")
                    # print(whiff_sound.get_length(),"===")
                    # print(whiff_sound.get_raw(),"===")
            elif event.type == MOUSEBUTTONUP:  # 放开鼠标
                fist.unpunch()
        allsprites.update()  # 更新页面

        # 绘制页面，使页面可见
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()


if __name__ == '__main__':
    start_game()
