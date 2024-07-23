'''
Description: 生成2024物流起重机创意赛的随机砝码位置
Author: qingmeijiupiao
Date: 2024-05-26 20:23:08
'''
import cv2
import numpy as np
import random
import time
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk
# 添加图片到底图
def add_image(background, foreground, x_offset=2000, y_offset=1000):

    x_offset=x_offset-foreground.shape[1]//2
    y_offset=y_offset-foreground.shape[0]//2
    # 提取前景图像的RGB通道和alpha通道
    foreground_rgb = foreground[:,:,0:3]
    alpha = foreground[:,:,3] / 255.0  # 将alpha通道归一化到0-1范围

    # 获取前景图像在底图中的位置
    rows, cols, _ = foreground_rgb.shape
    roi = background[y_offset:y_offset+rows, x_offset:x_offset+cols]

    # 对前景图像和背景图像进行alpha混合
    result = np.empty_like(roi, dtype=np.uint8)
    for y in range(rows):
        for x in range(cols):
            alpha_blend = alpha[y, x]
            if alpha_blend == 1.0:
                result[y, x] = foreground_rgb[y, x]
            else:
                result[y, x] = alpha_blend * foreground_rgb[y, x] + (1 - alpha_blend) * roi[y, x]
    # 更新底图中的前景部分
    background[y_offset:y_offset+rows, x_offset:x_offset+cols] = result
    return background

# 12个砝码坐标
points={
    1:(375.000,649.519),
    3:(1125.000,649.519),
    2:(562.500,324.760),
    4:(937.500,324.760),
    5:(0,0),
    6:(375,0),
    7:(1125,0),
    8:(1500,0),
    9:(562.500,-324.760),
    11:(937.500,-324.760),
    10:(375.000,-649.519),
    12:(1125.000,-649.519)
    }

def rand_creat_weight():
    wp = []
    for i in range(1,7):
      wp.append(list(points[2*i-random.randint(0,1)]))
    return wp

class WeightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weight Generator")
        try:
            with open('./show_resolution.json', 'r') as json_file:
                resolution_list = json.load(json_file)./
            self.show_resolution = tuple(resolution_list)
        except FileNotFoundError:
            print("show_resolution.json文件未找到")
            self.show_resolution = (1280, 720)
        # 创建一个画布用于显示图像
        self.canvas = tk.Canvas(root, width=self.show_resolution[0], height=self.show_resolution[1])

        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        self.tk_img = cv2.imread('./background.png')
        self.tk_img = cv2.resize(self.tk_img, self.show_resolution)
        self.tk_img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self.tk_img, cv2.COLOR_BGR2RGB)))
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
        self.canvas.image = self.tk_img  # 保存对图像的引用，避免被垃圾回收
        self.canvas.update()
        # 创建按钮，点击时生成新的图像
        self.generate_button = tk.Button(root, relief="flat",bg="#a2d2ff",text="生成", command=self.generate_image)
        self.generate_button.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        # 用于存储生成的图像
        self.background_image = None

    def generate_image(self):
        # 清空画布
        self.canvas.delete("all")

        # 尝试读取背景和前景图像
        try:
            self.background = cv2.imread('./background.png')
            foreground = cv2.imread('./weight.png', -1)
            if self.background is None or foreground is None:
                messagebox.showerror("Error", "Image files not found.")
                return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
                # 读取分辨率
        
        # 设置随机数种子
        random.seed(time.time())

        # 生成随机砝码
        weight_point = rand_creat_weight()

        # 将砝码添加到底图
        for i in range(0, 6):
            weight_point[i][0] = int(weight_point[i][0]) + 2000
            weight_point[i][1] = int(-1 * weight_point[i][1]) + 1000
            self.background = add_image(self.background, foreground, x_offset=weight_point[i][0], y_offset=weight_point[i][1])
        self.background = cv2.resize(self.background, self.show_resolution)
        # 将OpenCV图像转换为PIL图像，然后保存为临时文件

        temp_image = Image.fromarray(cv2.cvtColor(self.background, cv2.COLOR_BGR2RGB))
        temp_image.save("temp_image.png")  # 保存为临时文件

        # 加载临时图像文件到tkinter
        try:
            self.tk_img = ImageTk.PhotoImage(Image.open("temp_image.png"))
            self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
            self.canvas.image = self.tk_img  # 保存对图像的引用，避免被垃圾回收
        except Exception as e:
            messagebox.showerror("Error", "Failed to load image: " + str(e))

        # 更新画布
        self.canvas.update()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = WeightApp(root)
    app.run()

"""
                                              .=%@#=.
                                            -*@@@@@@@#=.
                                         .+%@@@@@@@@@@@@#=
                                       -#@@@@@@@* =@@@@@@@@*:
                                     =%@@@@@@@@=   -@@@@@@@@@#-
                                  .+@@@@@@@@@@-     .@@@@@@@@@@%=
                                .+@@@@@@@@@@@@-     +@@@@@@@@@@@@@+.
                               +@@@@@@@@@@@@@@@    .@@@@@@@@@@@@@@@@+.
                             =@@@@@@@@@@@@@@@%-     =%@@%@@@@@@@@@@@@@=
                           -%@@@@@@@@@@@@+..     .       -@@@@@@@@@@@@@%-
                         .#@@@@@@@@@@@@@#       -@+       +@@@@@@@@@@@@@@#:
                        +@@@@@@@@@@@@@@@@+     +@@@+     =@@@@@@@@@@@@@@@@@+
                      :%@@@@@@@@@@@@@@@@@+    *@@@@*     =@@@@@@@@@@@@@@@@@@%-
                     +@@@@@@@@@@@@@@#+*+-   .#@@@@+       :+*+*@@@@@@@@@@@@@@@*
                   :%@@@@@@@@@@@@@@+       :%@@@@-    .-       -@@@@@@@@@@@@@@@%:
                  =@@@@@@@@@@@@@@@@-      -@@@@%:    .%@+      =@@@@@@@@@@@@@@@@@=
                 *@@@@@@@@@@@@@@@@@@.    =@@@@#.    -@@@@+    =@@@@@@@@@@@@@@@@@@@#
               .%@@@@@@@@@@@@@@@@@@+    +@@@@*     =@@@@%:    .#@@@@@@@@@@@@@@@@@@@%.
              :@@@@@@@@@@@@@@@%:::.    #@@@@+     +@@@@#        .::.*@@@@@@@@@@@@@@@@-
             -@@@@@@@@@@@@@@@%       .%@@@@=     *@@@@*     +-       *@@@@@@@@@@@@@@@@=
            =@@@@@@@@@@@@@@@@@#.    -@@@@@-    :%@@@@=    .#@@+     +@@@@@@@@@@@@@@@@@@=
           =@@@@@@@@@@@@@@@@@@@:    =====.     -+===:     :====     @@@@@@@@@@@@@@@@@@@@+
          +@@@@@@@@@@@@@@@#%%#-                                     :*%%#%@@@@@@@@@@@@@@@+
         =@@@@@@@@@@@@@@%.       ...........................              *@@@@@@@@@@@@@@@=
        =@@@@@@@@@@@@@@@+      .#@@@@@@@@@@@@@@@@@@@@@@@@@@#     .*:      =@@@@@@@@@@@@@@@@-
       -@@@@@@@@@@@@@@@@@=    .%@@@@@@@@@@@@@@@@@@@@@@@@@@#     :@@@-    =@@@@@@@@@@@@@@@@@@:
      :@@@@@@@@@@@@@@@@@%.   -@@@@%+=====================:     -@@@@%    :%@@@@@@@@@@@@@@@@@@.
      %@@@@@@@@@@@@@=-=:    =@@@@#.                           +@@@@#.      -=--%@@@@@@@@@@@@@%
     #@@@@@@@@@@@@@:       +@@@@*      ............. .       *@@@@*             %@@@@@@@@@@@@@+
    =@@@@@@@@@@@@@@#.     #@@@@+     +@@@@@@@@@@@@@@@#.    .#@@@@+     +#.     +@@@@@@@@@@@@@@@:
   .@@@@@@@@@@@@@@@@-   .%@@@@=     *@@@@@@@@@@@@@@@#     :%@@@@-     *@@%:    @@@@@@@@@@@@@@@@%
   %@@@@@@@@@@@%%%#=   :@@@@@:    .#@@@@+-----------     -@@@@@:     #@@@@=    :#%%%@@@@@@@@@@@@*
  =@@@@@@@@@@@=       -@@@@%.    :%@@@@-                =@@@@%.    .%@@@@=          :%@@@@@@@@@@@:
  @@@@@@@@@@@%.      =@@@@#     -@@@@%:    .:::-:      +@@@@#     :@@@@@:    .       +@@@@@@@@@@@#
 +@@@@@@@@@@@@@.    *@@@@*     =@@@@#.    -@@@@@:     #@@@@+     =@@@@%.    -@#     +@@@@@@@@@@@@@-
.@@@@@@@@@@@@@#    *@%@%=     +@@@@*     =@@@@#.    .#@@@%=     +@@@@#     =@@@%.   =@@@@@@@@@@@@@%
+@@@@@@@@*-==-                .          .           . ..       .....      .....     .=+=+@@@@@@@@@-
%@@@@@@@+                                                                                 -@@@@@@@@#
@@@@@@@-       =#%#=     -#%%#-     -#%%*.     +%%%*.    .*%%#=     :#%%#-     =%%%*.      .#@@@@@@@
@@@@@@=.::::::*@@@@@*:::-@@@@@@-:::=@@@@@%::::*@@@@@#::::%@@@@@+:---@@@@@@=---+@@@@@%------:=@@@@@@@
=@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+
 *@@@@@@@@@@@@@@@@@@@@@@@@@@@%%##**++===----:::::------===++***##%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*
  -#@@@@@@@@@@@@@@@@%#*+=-:.                                        ..::-=+*##%@@@@@@@@@@@@@@@@@#-
    :=*%@@@@@%#*=-:                                                             .:-=+*#%%%%##+-.

          _____                   _______                   _____                    _____                _____
         /\    \                 /::\    \                 /\    \                  /\    \              /\    \
        /::\    \               /::::\    \               /::\____\                /::\    \            /::\    \
       /::::\    \             /::::::\    \             /:::/    /               /::::\    \           \:::\    \
      /::::::\    \           /::::::::\    \           /:::/    /               /::::::\    \           \:::\    \
     /:::/\:::\    \         /:::/~~\:::\    \         /:::/    /               /:::/\:::\    \           \:::\    \
    /:::/  \:::\    \       /:::/    \:::\    \       /:::/    /               /:::/__\:::\    \           \:::\    \
   /:::/    \:::\    \     /:::/    / \:::\    \     /:::/    /               /::::\   \:::\    \          /::::\    \
  /:::/    / \:::\    \   /:::/____/   \:::\____\   /:::/    /      _____    /::::::\   \:::\    \        /::::::\    \
 /:::/    /   \:::\    \ |:::|    |     |:::|    | /:::/____/      /\    \  /:::/\:::\   \:::\____\      /:::/\:::\    \
/:::/____/     \:::\____\|:::|____|     |:::|____||:::|    /      /::\____\/:::/  \:::\   \:::|    |    /:::/  \:::\____\
\:::\    \      \::/    / \:::\   _\___/:::/    / |:::|____\     /:::/    /\::/    \:::\  /:::|____|   /:::/    \::/    /
 \:::\    \      \/____/   \:::\ |::| /:::/    /   \:::\    \   /:::/    /  \/_____/\:::\/:::/    /   /:::/    / \/____/
  \:::\    \                \:::\|::|/:::/    /     \:::\    \ /:::/    /            \::::::/    /   /:::/    /
   \:::\    \                \::::::::::/    /       \:::\    /:::/    /              \::::/    /   /:::/    /
    \:::\    \                \::::::::/    /         \:::\__/:::/    /                \::/____/    \::/    /
     \:::\    \                \::::::/    /           \::::::::/    /                  ~~           \/____/
      \:::\    \                \::::/____/             \::::::/    /
       \:::\____\                |::|    |               \::::/    /
        \::/    /                |::|____|                \::/____/
         \/____/                  ~~                       ~~

"""