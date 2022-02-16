import pyautogui as pag
import keyboard
import time
import sys
import os

start_key: str = 'f'
stop_key: str = 't'
going: bool = False
glb_conf: float = 0.9
pos_list = [(-125, 0), (-125, -15), (-75, -75), (150, 0), (175, 0), (176, 25), (74, 75), (-150, 0), (-101, -11)]


def get_img_list():
    img_list = os.listdir()

    # 从文件列表中去除不是 .png 结尾的文件
    img_list = [each_file for each_file in img_list if each_file.endswith('png')]

    if not img_list:  # 若清理后的列表为空
        if pag.confirm('注意，未读取到任何以.png结尾的图片，此时在任何时间按下f都将激活程序，按确认继续，否则退出程序') != 'OK':
            sys.exit(0)

    return img_list


class Detector:
    def __init__(self):
        self.img_list = get_img_list()
        self.img_pos_dic = {}

    def __call__(self):
        return self.detected()

    def detected(self):
        for each_img in self.img_list:

            if each_img in self.img_pos_dic:  # 若已在字典中记录位置
                img_pos = pag.locateOnScreen(each_img, region=self.img_pos_dic[each_img], confidence=glb_conf)

                if not img_pos:  # 若在字典中位置没匹配到图片
                    print(f'[{get_time()}] 未匹配到图片\"{each_img}\"，从字典中删除')
                    del self.img_pos_dic[each_img]
                    img_pos = pag.locateOnScreen(each_img, confidence=glb_conf)

                else:
                    return True

            else:  # 若未在字典中记录位置
                img_pos = pag.locateOnScreen(each_img, confidence=glb_conf)

            if not img_pos:  # 若未匹配到图片
                print(f'[{get_time()}] 未匹配到图片\"{each_img}\"')

            if img_pos and (each_img not in self.img_pos_dic):  # 若匹配到位置但是在字典中没有记录
                print(f'[{get_time()}] 在\"{tuple(img_pos)}\"位置匹配到图片\"{each_img}\"，已记录在字典中')
                self.img_pos_dic[each_img] = tuple(img_pos)
                return True
        return False


def stop_working():
    global going
    if going:
        print(f'[{get_time()}] paused')
        going = False


def get_time():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    keyboard.add_hotkey(stop_key, stop_working)
    detected = Detector()

    while True:
        # 等待热键触发
        keyboard.wait(start_key)
        print(f'[{get_time()}] 侦测到按下f键')

        # 若侦测到未在指定地点，则不开启循环，返回等待阶段
        if not detected():
            continue

        else:
            print(f'[{get_time()}] started')
            going = True

            while going:
                for each in pos_list:
                    if not going:
                        break
                    elif not detected():
                        print(f'[{get_time()}] auto paused')
                        going = False
                        break

                    pag.mouseDown(button='left')
                    pag.moveRel(each[0], each[1], duration=0.15)
                    time.sleep(0.8)
                    pag.mouseUp(button='left')
