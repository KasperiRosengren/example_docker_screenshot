"""Testing dockers viability for GUI test automation
"""
import os
import argparse
import time
import subprocess
import pyautogui as pya
import pywinctl
import datetime
import logging

from common.display import Display
from common.common import SizeSquare, Point
from applications.krita import Krita
from controllers import wmctrl
from controllers import xdotool

# https://www.gimpusers.com/gimp/hotkeys
# https://shortcutworld.com/Krita/win/Krita-Painting_3_Shortcuts
logging.basicConfig(
        level=logging.DEBUG,
        format= "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        filename="/app/screenshots/log.log",
        filemode='w'
    )
logger = logging.getLogger(__name__)

def parse_args():
    """Get all run specific information from commandline"""
    desciption = """
        Test docker functionality with pyautogui
        """
    parser = argparse.ArgumentParser(description=desciption, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-d', '--screenshots-dir', 
        type=str,
        default="/app/screenshots",
        help='Directory where screenshots are stored. Default is ./screenshots'
    )
    
    args = parser.parse_args()

    return args.screenshots_dir


def main(save_folder: str):
    """main"""
    # Open display
    # Open Application
    # Take screenshot of screen
    # Do something on the app
    # Take a second screenshot
    wmctrl.get_window_manager()
    display_1 = Display(90, SizeSquare(1920, 1080), 16)
    display_1.start()
    wmctrl.get_window_manager()
    display_2 = Display(91, SizeSquare(1920, 1080), 16)
    display_2.start()
    #wmctrl.get_window_manager()

    krita = Krita(display_1)
    krita.start()
    time.sleep(30) # Wait for app to show up
    display_1.get_windows()
    display_1.take_screenshot(save_folder, "krita_start", "png")
    display_1.get_active_window()
    krita.make_fullscreen()
    display_1.take_screenshot(save_folder, "krita_fullscreen", "png")
    krita.start_new_document(SizeSquare(800,800))
    display_1.take_screenshot(save_folder, "krita_new_document", "png")
    krita.draw_square(Point(800, 500), SizeSquare(200,200))
    display_1.take_screenshot(save_folder, "krita_square", "png")
    temp_box = (
        800 - 150, 500 - 150, 200 + 300, 200 + 300
    )
    display_1.take_screenshot(save_folder, "square", "png", region=temp_box)

    krita.test_func()
    display_1.take_screenshot(save_folder, "krita_drawing", "png")

    

if __name__=="__main__":
    time.sleep(10)
    logger.info("STARTING".center(80, "-"))
    main(parse_args())
    logger.info("ENDING".center(80, "-"))