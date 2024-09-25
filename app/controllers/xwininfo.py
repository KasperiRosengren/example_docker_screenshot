from controllers.common import run_cmd

def get_all_windows():
    """Get all windows"""
    res = run_cmd(["xwininfo", "-tree", "-root"])
    return res.stdout
