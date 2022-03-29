import time
import win32gui
import win32ui
import win32api
import win32con
import pytesseract
import numpy as np
import pandas as pd
from PIL import Image

Y_OFFSET = 15
result = []

class torcs:
    def __init__(self, classname, filename):

        self.handle = win32gui.FindWindow(classname, filename)
        self.loc = win_findloc(self.handle)
        self.race = (327, 96)
        self.cruise = (327, 96)
        self.new_race = (327, 96)
        self.config_race = (327,130)
        self.newtype = (537,82)
        self.newtrack = (537, 102)
        self.accept = (213, 440)
        self.continu = (327, 440)
        self.process = []
        self.totalT = (110,115,65,20)
        self.totalTE = (210,115,65,20)
        self.error = (405,115,65,20)

    def newrace(self, *args):
        with open('D:/test.txt', 'w+') as tf:
            for a in args:
                tf.write(str(a)+'\n')
        self.process = [self.new_race]
        self.click()
        time.sleep(3)
        speedx(16)
        time.sleep(13) # decided by specific tracks
        self.get_grade(list(args))

    def reconfig(self, retype = False, retype_num = 1, reconfig_num = 1):
        self.process = [self.config_race, self.accept]
        if(retype):
            for i in range(retype_num):
                self.process.insert(1, self.newtrack)
        for i in range(reconfig_num):
            self.process.insert(-1, self.newtype)
        self.click()

    def nextrace(self):
        self.process = [self.continu]
        self.click()


    def click(self):
        for choice in self.process:
            mouse_click(self.loc[0], self.loc[1], choice)  #0,1,2,3->left, top, right, bottom
            time.sleep(0.3)

    def get_grade(self, args):
        get_windows(self.handle, self.totalTE, './test.png')
        text = pytesseract.image_to_string(Image.open("./test.png"),lang="eng")
        print(text)
        args.append(text)
        result.append(args)
        
    def exit_race(self):
        print("race failed, trying to exit...\n")
        win32api.keybd_event(0x1B, 0, 0, 0)
        win32api.keybd_event(0x1B, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)
        self.process = [self.abandon]
        self.click



def win_findloc(handle):
    if (handle):
        rect = win32gui.GetWindowRect(handle)
        print(hex(handle),rect)
        return rect
    return None

def mouse_click(x, y, delta):
    win32api.SetCursorPos([x + delta[0], y + delta[1] + Y_OFFSET])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def speedx(s):
    while(s>1):
        print("try")
        win32api.keybd_event(0x10, 0, 0, 0)
        win32api.keybd_event(0xBB, 0, 0, 0)
        win32api.keybd_event(0xBB, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)
        s = s/2

def get_windows(handle, loc, filename):

    hdDC = win32gui.GetWindowDC(handle)
    newhdDC = win32ui.CreateDCFromHandle(hdDC)
    saveDC = newhdDC.CreateCompatibleDC()
    saveBitmap = win32ui.CreateBitmap()

    left, top, width, height = loc
    saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
    saveDC.SelectObject(saveBitmap)
    saveDC.BitBlt((0,0), (width, height), newhdDC, (left, top), win32con.SRCCOPY)
    saveBitmap.SaveBitmapFile(saveDC, filename)


torcs_path = r"D:\input yout filepath\wtorcs.exe"
rj = torcs("GLUT", torcs_path)


#for p1 in np.arange(0.16,0.28,0.04):
#    for p2 in np.arange(1.3,2.4,0.2):
#        print(p1,p2)
#        rj.newrace(p1,p2)
#        rj.nextrace()

#for p1 in np.arange(0.07,0.09,0.002):
#    print(p1)
#    rj.newrace(p1)
#    rj.nextrace()

#df1 = pd.DataFrame(result)
#df1.to_csv('test.csv', index = False, header = False)
   
