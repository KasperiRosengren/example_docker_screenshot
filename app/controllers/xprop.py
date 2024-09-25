from controllers.common import run_cmd


def get_active_window():
    """Get active window"""
    res = run_cmd(["xprop", "-root", "_NET_ACTIVE_WINDOW"])
    return res.stdout

def get_all_root():
    res = run_cmd(["xprop", "-root"])
    return res.stdout