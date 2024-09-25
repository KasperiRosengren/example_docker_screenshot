from controllers.common import run_cmd

def get_window_titles():
    res = run_cmd(["wmctrl", "-l"])
    return res

def focus_on_window_with_title(title):
    res = run_cmd(["wmctrl", "-a", title])
    return res

def get_window_manager():
    res = run_cmd(["wmctrl", "-m"])
    return res