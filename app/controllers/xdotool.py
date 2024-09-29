import time

from controllers.common import run_cmd
from common.common import Point

def set_active_window(window_id):
    """Sets given window ID as active window"""
    res = run_cmd(["xdotool", "windowactivate", str(window_id)])
    return res.stdout

def set_focus_window(window_id):
    """Focuses on the given window ID"""
    res = run_cmd(["xdotool", "windowfocus", str(window_id)])
    return res.stdout

def get_window_with_name(window_title: str):
    """Gets all windows matching the name"""
    res = run_cmd(["xdotool", "search", "--name", window_title])
    return res.stdout

def get_active_window():
    """Gets currently active window"""
    res = run_cmd(["xdotool", "getactivewindow"])
    return res.stdout

def get_window_focus():
    """Gets currently focused window"""
    res = run_cmd(["xdotool", "getwindowfocus"])
    return res.stdout

def get_window_name():
    """Gets currently active window"""
    res = run_cmd(["xdotool", "getwindowname"])
    return res.stdout

#
#   MOUSE
#
def get_mouse_position():
    """Gets the mouse position on screen and returns `Point`"""
    # x:459 y:319 screen:0 window:27267499
    res = run_cmd(["xdotool", "getmouselocation"])
    x_str, y_str, *_ = res.stdout.split()
    return Point(x=int(x_str.split(":")[1]), y = int(y_str.split(":")[1]))

def move_mouse(x, y, delay: float = 0.0):
    res = run_cmd(["xdotool", "mousemove", "--sync", str(x), str(y), "sleep", f"{delay:.2f}"])
    return res.stdout

def click_mouse_left():
    res = run_cmd(["xdotool", "click", "1"])
    return res.stdout

def move_and_click_mouse_left(x, y, delay: float = 0.0):
    res = run_cmd(["xdotool", "mousemove", "--sync", str(x), str(y), f"sleep {delay:.2f}" "click", "1"])
    return res.stdout

def drag_mouse_left(x:int ,y: int):
    res = run_cmd(["xdotool", "mousedown", "1", "mousemove", str(x), str(y), "mouseup", "1"])
    return res.stdout

def _drag_mouse_to(x: int, y: int, steps: int = 100, total_time: float = 0.1):
    step_time = total_time / steps
    current_mouse = get_mouse_position()
    move_x = x - current_mouse.x
    move_y = y - current_mouse.y

    step_x_dist = move_x / steps
    step_y_dist = move_y / steps

    #[start + x*step_dist for x in range(steps+1)]
    steps_x = [current_mouse.x + step_x_dist * i for i in range(steps +1)]
    steps_y = [current_mouse.y + step_y_dist * i for i in range(steps +1)]

    for point in [Point(px, py) for px, py in zip(steps_x, steps_y)]:
        #move_and_click_mouse_left(point.x, point.y)
        drag_mouse_left(point.x, point.y)
        time.sleep(step_time)


def press_mouse_left():
    res = run_cmd(["xdotool", "mousedown", "1"])
    return res.stdout

def release_mouse_left():
    res = run_cmd(["xdotool", "mouseup", "1"])
    return res.stdout

def get_commands():
    res = run_cmd(["xdotool", "mouseup", "1"])
    return res.stdout

#
#   KEYBOARD
#

# http://www.linuxcertif.com/man/1/xdotool/
#https://gitlab.com/nokun/gestures/-/wikis/xdotool-list-of-key-codes
def press_key(key: str):
    res = run_cmd(["xdotool", "key", key])
    return res.stdout

def press_multiple_keys(keys: list[str]):
    key = "+".join(keys)
    res = run_cmd(["xdotool", "key", key])
    return res.stdout

def write(text: str):
    res = run_cmd(["xdotool", "type", text])
    return res.stdout
