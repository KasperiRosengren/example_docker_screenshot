from controllers.common import run_cmd

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

# http://www.linuxcertif.com/man/1/xdotool/
#https://gitlab.com/nokun/gestures/-/wikis/xdotool-list-of-key-codes
def press_key(key: str):
    res = run_cmd(["xdotool", "key", key])
    return res.stdout

def press_multiple_keys(keys: list[str]):
    key = "+".join(keys)
    res = run_cmd(["xdotool", "key", key])
    return res.stdout
