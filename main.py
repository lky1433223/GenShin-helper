import pyautogui
import time
import sys
import ctypes

# 保护措施，避免失控
pyautogui.FAILSAFE = True
# 为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。
pyautogui.PAUSE = 0.1
# 文件路径
path3 = "assets/chosen.bmp"


def wait(x):
    print("等待 " + str(x) + "s")
    for i in range(0, x):
        print(i + 1)
        time.sleep(1)


def click():
    try:
        coords = pyautogui.locateOnScreen(path3, confidence=0.6)
        if coords is not None:
            xy = pyautogui.center(coords)
            print("已找到对话框")
            wait(5)  # 等5秒把话说完
            pyautogui.moveTo(x=xy.x, y=xy.y, duration=0.2)
            pyautogui.click()
            print("已点击")
            return True
        else:
            print("未找到对话框")
            return False
    except:
        print("程序出错了")


def main():
    op = pyautogui.confirm(text='请将窗口调整为1600*900，打开剧情自动\n确   认后将自动进行剧情对话点击',
                           title='原神剧情小助手', buttons=['OK', 'Cancel'])
    if op == 'OK':
        while True:
            c = click()
            # 点到对话之后3秒
            if c:
                wait(3)
            else:
                wait(2)
    else:
        pyautogui.alert(text='感谢您的使用，再见', title='原神剧情小助手', button='OK')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except BaseException as err:
        print(err)
        raise err


if __name__ == '__main__':
    if not is_admin():
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
            sys.exit(0)
    main()
