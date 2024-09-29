from abc import ABC, abstractmethod
from typing import Union, Optional, NamedTuple



#from common.display import Display

class ApplicationStopFailed(Exception):
    pass

class ApplicationStartFailed(Exception):
    pass

class NewDocumentFailed(Exception):
    pass

class ApplicationBase(ABC):
    HOTKEYS: dict = {}
    SCREENSHOTS = {}
    @abstractmethod
    def __init__(self, display: "Display"):
        self.display: "Display" = display
        self.running: bool = False
        self.name: str = None

    
    def start(self):
        """Start the apllication in the `self.display` Display"""
        try:
            self.display.open_app(self)
            self.running = True
        except Exception as e:
            ApplicationStartFailed(e)
    
    def close(self):
        try:
            self.display.close_application(self)
            self.running = False
        except Exception as e:
            ApplicationStopFailed(e)

    
    def make_window_active(self):
        # Makes the application window active in the `self.display`
        pass

    
    def is_window_active(self):
        # Checks whether applications window is active in the `self.display`
        pass

    @abstractmethod
    def make_fullscreen(self):
        pass


