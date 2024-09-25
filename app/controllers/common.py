import subprocess
import logging

def run_cmd(cmd: list):
    """Run every CMD through this"""
    logger = logging.getLogger(__name__)
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False
    )
    logger.debug(res)
    if res.stderr:
        logger.warning(res.stderr)
    if res.stdout:
        logger.info(f"{res.stdout=}")
    return res