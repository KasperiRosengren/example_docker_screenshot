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

import controllers.xdotool as xdotool
import controllers.xprop as xprop
import controllers.xwininfo as xwininfo
import controllers.wmctrl as wmctrl

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



def set_window_active(window_title: str):
    """Needs to be run in case"""
    res = windows[0].activate() if len((windows := pywinctl.getWindowsWithTitle(window_title))) > 0 else None
    if res is None:
        active = xdotool.get_active_window()
        app_windows = xdotool.get_window_with_name(window_title)
        if app_windows and active != (wanted := app_windows.split("\n")[0]):
            xdotool.set_active_window(wanted)
        #xdotool.set_active_window(app_windows.split("\n")[0])
        #xdotool.set_focus_window(app_windows.split("\n")[0])
        #xdotool.get_active_window()
    elif res is False:
        logger.debug(f"Activate window - {window_title}")
    else:
        logger.debug(f"Already active window - {window_title}")



def open_app(app_name: str, display):
    """open"""
    logger.info(f"Opening app - {app_name.capitalize()}")
    # Start Xvfb for the new virtual display
    app_display = subprocess.Popen(["Xvfb", display, "-screen", "0", "1920x1080x16"])
    time.sleep(2)

    # Set the DISPLAY environment variable
    env = os.environ.copy()
    env["DISPLAY"] = display

    window_manager = subprocess.Popen(["fluxbox"], env=env)

    # Start the app
    #subprocess.Popen(["xvfb-run", "-e", "/dev/stdout", "-a", f"/usr/bin/{app_name}"], env=env, stdout=out) # <-- Does not work at all
    app = subprocess.Popen([f"/usr/bin/{app_name}"], env=env)
    time.sleep(2)
    pya.hotkey("ctrl", "n")
    return display, app_display, app, window_manager

def run_preset_commands(display, app_name: str):
    """Test functionality"""
    logger.info(f"Runninng test commands on - {app_name}")
    krita_name = "Krita"
    gimp_name = "GNU Image Manipulation Program"
    os.environ["DISPLAY"] = display
    set_window_active(app_name)
    if app_name == krita_name:
        #Fullscreen
        xdotool.press_multiple_keys(["Shift", "Ctrl", "f"])
        time.sleep(2) # TODO - add a wait for x to show up
        xdotool.press_multiple_keys(["Ctrl", "n"])
        time.sleep(2) # TODO - add a wait for x to show up
        xdotool.press_multiple_keys(["Alt_L", "c"])
    elif app_name == gimp_name:
        # Fullscreen
        xdotool.press_key("F11")
        # Create new window, but not working for now
        #xdotool.press_multiple_keys(["Ctrl", "n"])
        #time.sleep(2)
        #for _ in range(9):
        #    xdotool.press_key("Tab")
        #    time.sleep(0.2)
        #xdotool.press_key("KP_Enter")
    
    time.sleep(2)



def take_screenshot(display, save_path, file_name: str = "test", endix: str = "png"):
    """SCR"""
    logger.info(f"taking screenshot - {file_name}")
    os.environ["DISPLAY"] = display
    time.sleep(5)  # Wait for the app to fully load if needed
    screenshot = pya.screenshot()
    screenshot.save(f"{save_path}/{file_name}.{endix}")

def main(screenshots):
    """main"""
    wmctrl.get_window_manager()
    krita_name = "Krita"
    gimp_name = "GNU Image Manipulation Program"
    krita_display, krita_app_display, krita_app, krita_wm = open_app("krita", ":90")
    gimp_display, gimp_app_display, gimp_app, gimp_wm = open_app("gimp", ":91")
    take_screenshot(krita_display, screenshots, "krita_start")
    run_preset_commands(krita_display, krita_name)
    take_screenshot(krita_display, screenshots, "krita_end")
    
    take_screenshot(gimp_display, screenshots, "gimp_start")
    run_preset_commands(gimp_display, gimp_name)
    take_screenshot(gimp_display, screenshots, "gimp_end")

    krita_app.terminate()
    krita_app_display.terminate()
    krita_wm.terminate()

    gimp_app.terminate()
    gimp_app_display.terminate()
    gimp_wm.terminate()

if __name__=="__main__":
    time.sleep(10)
    logger.info("STARTING".center(80, "-"))
    main(parse_args())
    logger.info("ENDING".center(80, "-"))