import time
import win32gui
import win32ui
import win32api
import win32con
import pytesseract
import numpy as np
import pandas as pd
from PIL import Image

from . import loader

Y_OFFSET = 15

class torcs:
    def __init__(self, filepath, classname = 'GLUT'):

        self.filepath = filepath + r'\wtorcs.exe'
        self.handle = win32gui.FindWindow(classname, self.filepath)
        loader.loaddir(filepath)
        self.loc = _win_findloc(self.handle)
        self.max_time = 15
        self.race = (327, 96)
        self.cruise = (327, 96)
        self.new_race = (327, 96)
        self.config_race = (327,130)
        self.newtype = ((82,82), (537,82))
        self.newtrack = ((82,102), (537,102))
        self.accept = (213, 440)
        self.continu = (327, 440)
        self.process = []
        self.totalT = (110,115,65,20)
        self.totalTE = (210,115,65,20)
        self.error = (405,115,65,20)
        self.result = []

    def newrace(self, *args):
        with open('D:/test.txt', 'w+') as tf:
            for a in args:
                tf.write(str(a)+'\n')
        self.process = [self.new_race]
        self.click()
        time.sleep(3)
        _speedx(16)
        time.sleep(self.max_time) # decided by specific tracks
        self.get_grade(list(args))

    def select_track(self, ntrack):
        ptrack = loader.now_track(self.filepath)
        p = loader.get_track_num(ptrack)
        n = loader.get_track_num(ntrack)
        if (n[0] == p[0]):
            self.reconfig(0, n[1] - p[1])
        else:
            self.reconfig(n[0]-p[0], n[1])

    def reconfig(self, road_num = 0, track_num = 1):
        self.process = [self.config_race, self.accept]

        if (road_num < 0):
            for i in range(abs(road_num)):
                self.process.insert(1, self.newtype[0])
        else:
            for i in range(road_num):
                self.process.insert(1, self.newtype[1])

        if (track_num < 0):
            for i in range(abs(track_num)):
                self.process.insert(-1, self.newtrack[0])
        else:
            for i in range(track_num):
                self.process.insert(-1, self.newtrack[1])

        print(self.process)

        self.click()

    def nextrace(self):
        self.process = [self.continu]
        self.click()


    def click(self):
        for choice in self.process:
            _mouse_click(self.loc[0], self.loc[1], choice)  #0,1,2,3->left, top, right, bottom
            time.sleep(0.3)

    def get_grade(self, args):
        _get_windows(self.handle, self.totalTE, './test.png')
        text = pytesseract.image_to_string(Image.open("./test.png"),lang="eng")
        print(text)
        args.append(text)
        self.result.append(args)
        
    def exit_race(self):
        print("race failed, trying to exit...\n")
        win32api.keybd_event(0x1B, 0, 0, 0)
        win32api.keybd_event(0x1B, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)
        self.process = [self.abandon]
        self.click

    def saveresult(tcls, filepath = 'test.csv'):
        df1 = pd.DataFrame(result)
        df1.to_csv('test.csv', index = False, header = False)



def _win_findloc(handle):
    if (handle):
        rect = win32gui.GetWindowRect(handle)
        print(hex(handle),rect)
        return rect
    return None

def _mouse_click(x, y, delta):
    win32api.SetCursorPos([x + delta[0], y + delta[1] + Y_OFFSET])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def _speedx(s):
    while(s>1):
        print("try")
        win32api.keybd_event(0x10, 0, 0, 0)
        win32api.keybd_event(0xBB, 0, 0, 0)
        win32api.keybd_event(0xBB, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)
        s = s/2

def _get_windows(handle, loc, filename):

    hdDC = win32gui.GetWindowDC(handle)
    newhdDC = win32ui.CreateDCFromHandle(hdDC)
    saveDC = newhdDC.CreateCompatibleDC()
    saveBitmap = win32ui.CreateBitmap()

    left, top, width, height = loc
    saveBitmap.CreateCompatibleBitmap(newhdDC, width, height)
    saveDC.SelectObject(saveBitmap)
    saveDC.BitBlt((0,0), (width, height), newhdDC, (left, top), win32con.SRCCOPY)
    saveBitmap.SaveBitmapFile(saveDC, filename)

