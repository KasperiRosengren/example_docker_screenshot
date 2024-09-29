import os
import time
import subprocess

import pyautogui as pya

from common.common import SizeSquare
from controllers import xdotool
from controllers import xwininfo
#from applications.application_base import ApplicationBase


class Display:
    """
    Currently only one screen supported, maybe adding a way to control more
    """
    def __init__(self, id: int, size: SizeSquare, color_accuracy: int):
        self.id = id
        self.size = size
        self.color_accuracy = color_accuracy
        self.display = None
        self.applications = {}
        #self.env = None

    def __str__(self):
        return f":{self.id} {self.size.width}x{self.size.height}x{self.color_accuracy}"
    
    def start(self):
        # Hardcoded screen value, not supporting more at the moment
        print("Starting display")
        self.display = subprocess.Popen([
            "Xvfb",
            f":{self.id}",
            "-screen",
            "0",
            f"{self.size.width}x{self.size.height}x{self.color_accuracy}"
        ])
        time.sleep(2)
        #self.env = os.environ.copy()
        self.enable()
        self.window_manager = subprocess.Popen(["fluxbox"], env=os.environ)
        time.sleep(5) # Give some time for WM
    
    def enable(self):
        #self.env["DISPLAY"] = f":{self.id}"
        os.environ["DISPLAY"] = f":{self.id}"
        time.sleep(2)
    
    def terminate(self):
        self.enable()
        if len(self.applications) > 0:
            for app in self.applications.values():
                app.terminate()
        
        if self.window_manager:
            self.window_manager.terminate()
        
        if self.display:
            self.display.terminate()

    def open_app(self, application: "ApplicationBase"):
        """Opens the given application, call directly from the application"""
        self.enable()
        print(f"Starting app {application.name}")
        app_process = subprocess.Popen([f"/usr/bin/{application.name}"], env=os.environ)
        print(app_process)
        print(f"{self.applications=}")
        self.applications[application] = app_process
        print(f"{self.applications=}")
    
    def close_application(self, application: "ApplicationBase"):
        self.enable()
        app_process: subprocess.Popen = self.applications[application]
        app_process.terminate()
    
    def take_screenshot(self, save_path, file_name: str = "test", endix: str = "png", region: tuple[int] = None):
        """SCR"""
        print(f"Taking screenshot: {self}")
        print(f"{xdotool.get_active_window()=}\n{xdotool.get_window_with_name("Krita")=}")
        print(self.applications)
        self.enable()
        screenshot = pya.screenshot(region=region)
        screenshot.save(f"{save_path}/{file_name}.{endix}")

    def get_active_window(self):
        self.enable()
        print(xdotool.get_active_window())

    def get_windows(self):
        self.enable()
        print(xwininfo.get_all_windows())

