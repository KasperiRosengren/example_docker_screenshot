import time

import pyautogui as pya

from common.display import Display
from common.common import SizeSquare, Point
from applications.application_base import ApplicationBase, NewDocumentFailed
from controllers import xdotool

class Krita(ApplicationBase):
    HOTKEYS = {
        "all_time":{
            "fullscreen": ["Shift", "Ctrl", "f"],
            "new_document": ["Ctrl", "n"]
        },
        "new_document":{
            "accept": ["Alt_L", "c"],
            "select_width": ["Alt_L", "i"],
            "select_height": ["Alt_L", "h"]
        }
    }
    SCREENSHOTS = {
        "main": "/app/helper_screenshots/krita_color_selector.png"
    }
    def __init__(self, display: "Display"):
        super().__init__(display)
        self.name = "krita"
    
    def start_new_document(self, doc_size: SizeSquare):
        # TODO - CHECKS if there was an old one that needs saving/deleting
        try:
            xdotool.press_multiple_keys(Krita.HOTKEYS["all_time"]["new_document"])
            time.sleep(1) # TODO - replace with check
            xdotool.press_multiple_keys(Krita.HOTKEYS["new_document"]["select_width"])
            xdotool.write(str(doc_size.width))
            xdotool.press_multiple_keys(Krita.HOTKEYS["new_document"]["select_height"])
            xdotool.write(str(doc_size.height))
            xdotool.press_multiple_keys(Krita.HOTKEYS["new_document"]["accept"])
        except Exception as e:
            raise NewDocumentFailed(e)

    def make_fullscreen(self):
        # Check that window is active, so the hotkey go to it
        xdotool.press_multiple_keys(Krita.HOTKEYS["all_time"]["fullscreen"])
        time.sleep(1)

    def set_drawing_type(self, drawing_type: str):
        """Sets the wanted drawing type, either with hotkeys, or with click"""
        pass

    def draw_line_freehand_p2p(self, start: Point, end: Point):
        self.display.enable()
        xdotool.move_mouse(*start)
        xdotool._drag_mouse_to(*end)
    
    def draw_line_freehand_from_place(self, end: Point):
        self.display.enable()
        xdotool._drag_mouse_to(*end)
    
    def draw_square(self, top_left: Point, size: SizeSquare):
        self.display.enable()
        # Top left -> top right
        self.draw_line_freehand_p2p(
            top_left, 
            Point(x=top_left.x + size.width, y=top_left.y)
        )
        # Top right -> bottom right
        self.draw_line_freehand_from_place(
            Point(x=top_left.x + size.width,
                  y=top_left.y + size.height
            )
        )
        # Bottom right -> bottom left
        self.draw_line_freehand_from_place(
            Point(x=top_left.x,
                  y=top_left.y + size.height
            )
        )
        # Bottom left -> top left
        self.draw_line_freehand_from_place(top_left)

        

    def test_func(self):
        self.display.enable()
        width, height = self.display.size
        center_x = width // 2
        center_y = height // 2

        print(f"{pya.position()}")
        print(f"{center_x}, {center_y}")
        print("LOOKING FOR IT".center(50, "-"))
        try:
            box = pya.locateOnScreen(Krita.SCREENSHOTS["main"], minSearchTime=10, confidence=0.85)
            print(f"{box=}")
            tmp = tuple((
                int(box.left),
                int(box.top),
                int(box.left + box.width),
                int(box.top + box.height)
            ))
            print(f"{tmp=}")
            scr = pya.screenshot(region=tmp)
            scr.save("/app/screenshots/testcolorpicker.png")
        except pya.ImageNotFoundException as INFE:
            print(f"Image {Krita.SCREENSHOTS['main']} not found: {INFE}")
        print("DID I FIND IT".center(50, "-"))

        xdotool.move_mouse(center_x, center_y)
        print(xdotool.get_mouse_position())
        xdotool._drag_mouse_to(center_x + 100, center_y + 100, total_time=10)
        print(xdotool.get_mouse_position())
        xdotool.click_mouse_left()
        xdotool.move_mouse(center_x + 100, center_y)
        print(xdotool.get_mouse_position())
        xdotool._drag_mouse_to(center_x + 200, center_y + 100)
        print(xdotool.get_mouse_position())


        # TODO - Test pyautogui more, seems to be not working atm?
        # pya.moveTo(center_x, center_y)
        # print(f"{pya.position()}")
        # pya.dragTo(center_x +100, center_y + 100, button="left", duration=0.2)
        # print(f"{pya.position()}")
        # pya.moveTo(center_x +100, center_y)
        # print(f"{pya.position()}")
        # pya.dragTo(center_x +200, center_y + 100, button="left", duration=0.2)
        # print(f"{pya.position()}")
        


    
    