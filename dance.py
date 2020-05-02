#!/bin/python3

import getopt
import sys
from typing import List, Tuple
import cv2
import time
import curses

def main(argv: List[str]):
    # parse args
    try:
        opts, args = getopt.getopt(argv,"ho:",["help"])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h', "--help"]:
            printHelp()
            return
    if len(args) != 1:
        printHelp()
        return
    # open the video
    try:
        cap = cv2.VideoCapture(args[0])
    except Exception:
        print(Exception)
        return
    
    # open curse
    stdscr = curses.initscr()
    curses.noecho()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        # convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # openCV and curses has different xy axis,
        # get the src_width at y
        gh, gw = len(frame), len(frame[0])
        # shrink the image to adapt to the screen
        minf = min(1, curses.LINES/gh, curses.COLS/gw)
        gray = cv2.resize(gray, (min(curses.COLS, int(minf*gw)), min(curses.LINES, int(minf*gh))))
        assert(len(gray) <= curses.LINES)
        assert(len(gray[0]) <= curses.COLS)
        # convert to ascii
        # all pixel in gray is in [0, 2**8];
        # we have 2**3 ascii character in alphabet;
        # toAscii just get the highest 3 bit
        toAscii = lambda x: " .\"*oO#@"[int(x>>5)]
        # map toAscii for every pixel
        gray = [list(map(toAscii, row)) for row in gray]
        # print them in strscr
        for i, r in enumerate(gray):
            stdscr.addstr(i, 0, "".join(r))
            stdscr.refresh()
        time.sleep(0.08)

    cap.release()
    return

def printHelp():
    print ('usage: dance.py <input file>')
    print ('input file name must not contain any non-ascii character')


if __name__ == "__main__":
    main(sys.argv[1:])
