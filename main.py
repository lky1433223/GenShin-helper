import json
import random

import pyautogui
import time
import sys
import ctypes
import logging
import json

# 加载对话设置
with open("settings/text.json", encoding="utf-8") as f:
    text = json.load(f)
    f.close()
text_windows = text["window"]
text_dialogue = text["dialogue"]
# 初始化设置
with open("settings/settings.json", encoding="utf-8") as f:
    settings = json.load(f)
    f.close()
# chosen图片的路径
path_chosen = settings["chosen_path"]

# 保护措施，避免失控
pyautogui.FAILSAFE = True
# 为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。
pyautogui.PAUSE = 0.1


def wait(x):
    print("等待 " + str(x) + "s")
    for i in range(x):
        print(i + 1, end='...\n')
        time.sleep(1)


def click() -> bool:
    """
    寻找对话图标并进行点击
    :return: true:找到并点击 false：未找到
    """
    try:
        coords = pyautogui.locateOnScreen(path_chosen, confidence=0.8)  # 寻找图片 confidence是模糊值
        if coords is not None:
            xy = pyautogui.center(coords)  # 图像坐标
            print(text_dialogue["find"])
            wait(settings["wait_after_find"])  # 等5秒把话说完
            pyautogui.moveTo(x=xy.x, y=xy.y, duration=0.1 + random.random() / 3)  # 随机在0.1-0.4移动鼠标混淆
            pyautogui.click()
            print(text_dialogue["clicked"])
            return True
        else:
            print(text_dialogue["not find"])
            return False
    except Exception as err:
        print(text_dialogue["error"], err)
        raise err


def main():
    op = pyautogui.confirm(text=text_windows["prompt"], title=text_windows["title"], buttons=['OK', 'Cancel'])
    if op == 'OK':
        while True:
            clicked = click()
            wait(settings["wait_after_clicked"]) if clicked else wait(settings["wait_not_find"])  # 点到之后对话/没有点到对话
    else:
        pyautogui.alert(text=text_windows["thank"], title=text_windows["title"], button='OK')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except BaseException as err:
        print(err)
        raise err


if __name__ == '__main__':
    # TODO:优化使用体验,跳过对话等功能
    # TODO:剧情自动
    # logger
    if not is_admin():
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
            sys.exit(0)
    main()
