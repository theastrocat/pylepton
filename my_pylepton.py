import time
import sys
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3

def part_gen():
    while True:
         for x in range(0,3):
            yield x

def capture(device = "/dev/spidev0.0"):
    switch = 0
    start = time.time()
    name_gen = part_gen()
    while time.time() < start + rec_len:
        chk_time = round((time.time() - start) % 1,1)
        if round(chk_time % .3, 1) == 0 and switch == 0 and round((time.time() - start),1) % 1 != 0:
            with Lepton3(device) as l:
                a,_ = l.capture()
                name = int(round(time.time()))
            cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)
            np.right_shift(a, 8, a)
            image = np.uint8(a)
            cv2.imwrite("/images/{}_{}".format(name, name_gen.next()), image)
            switch = 1
        if switch == 1 and round(chk_time % .3, 1) != 0:
            switch = 0
        time.sleep(0.001)

if __name__ == '__main__':
    capture()
