import pyautogui
import os
import time
import random
import ctypes, sys
# 保护措施，避免失控
pyautogui.FAILSAFE = True
# 为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。
pyautogui.PAUSE = 0.1
# 文件路径
path3 = "chosen.png"
path4 = "pause.png"

coldInitFlag = False

#各阶段停留时间，单位秒
waitTime_Talk = 4.0
waitTime_optionClick = 3.0
waitTime_noDialogClick = 2.0
waitTime_dialogClick = 1.0

#点击时间混淆
timeFilter = 0.01

# 自动点击的速度等级, 1最慢, 5最快
SpdLevel = 2
SpdLevelTable = [1,2,4,6,10]

def wait(x):
    print("等待 "+str(x)+"s")
    tep = int(x*10)
    for i in range(0, tep):
        #print(i + 1)
        time.sleep(0.1)

def getFilteredTime(x, deltaTime = 5, xFilter = 1.0):
    return x+timeFilter*random.randint(-deltaTime, deltaTime) * xFilter

def click():
    try:
        coords = pyautogui.locateOnScreen(path3, confidence=0.8)
        if(coords != None):
            xy = pyautogui.center(coords)
            print("已找到对话选项")
            wait(getFilteredTime(waitTime_Talk))  # 等waitTime秒把话说完
            pyautogui.moveTo(x=getFilteredTime(xy.x, 20, 100), y=getFilteredTime(xy.y, 2, 100), duration=getFilteredTime(0.2, 2))
            pyautogui.click()
            print("已点击选项")
            return 1
        else:
            print("未找到对话框")
            coords = pyautogui.locateOnScreen(path4, confidence=0.8)
            if(coords != None):
                xy = pyautogui.center(coords)
                print("已找到对话框")
                pyautogui.moveTo(x=getFilteredTime(xy.x+750, 50, 100), y=getFilteredTime(xy.y+400, 10, 100), duration=getFilteredTime(0.2, 2))
                pyautogui.click()
                print("已点击对话框，加速对话")
                return 2
            return 0
    except:
        print("程序出错了")

def creatCfgFile():
    global coldInitFlag
    global SpdLevel
    if(os.path.exists("Genshin.cfg")):
        coldInitFlag = False
        file = open(".\\Genshin.cfg", "r")
        strLines = file.readlines()
        for strLine in strLines:
            if(strLine.split("Speed=")[0].strip()=="" and int(strLine.strip().split("Speed=")[1]) in range(1,5)):
                SpdLevel = int(strLine.split("Speed=")[1].strip())
                break
        file.close()
    else:
        coldInitFlag = True
        file = open(".\\Genshin.cfg", "w+")
        file.write(f"#可配置5种点击速度档，1最慢，5最快,在Speed=后加数字即可配置\n")
        file.write("Speed=2")
        file.close()
    return coldInitFlag

def iniCfg():
    global waitTime_Talk
    global waitTime_optionClick
    global waitTime_noDialogClick
    global waitTime_dialogClick
    waitTime_Talk /= SpdLevelTable[SpdLevel-1]
    waitTime_optionClick /= SpdLevelTable[SpdLevel-1]
    waitTime_noDialogClick /= SpdLevelTable[SpdLevel-1]
    waitTime_dialogClick /= SpdLevelTable[SpdLevel-1]
    
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#以管理员身份运行
if is_admin():
    pass
else:
    if sys.version_info[0] == 3:
    	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    	sys.exit(0)
    	
def main():
    creatCfgFile()
    op = "OK"
    iniCfg()
    if(coldInitFlag):
        op = pyautogui.confirm(text=f'请将游戏分辨率调整为1600*900或以上，并打开剧情自动\n确认后将自动进行剧情对话点击\n本程序目录{os.getcwd()}下Genshin.cfg文件可配置点击速度\n默认速度等级:2',
                           title='原神剧情小助手', buttons=['OK', 'Cancel'])
   
    if(op == 'OK'):
        while(True):
            c = click()
            # 点到对话选项(1)或者对话框(2)之后x秒
            if(1 == c):
                wait(getFilteredTime(waitTime_optionClick))
            elif(2 == c):
                wait(getFilteredTime(waitTime_dialogClick))
            else:
                wait(getFilteredTime(waitTime_noDialogClick))
    else:
        pyautogui.alert(text='感谢您的使用，再见', title='原神剧情小助手', button='OK')

if __name__ == '__main__':
    main()
