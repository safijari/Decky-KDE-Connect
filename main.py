import os

from click import get_app_dir
import decky_plugin
from pathlib import Path
import json
import os
import subprocess
import sys
import shutil
import time
import asyncio
import traceback

logger = decky_plugin.logger

std_out_file = open(Path(decky_plugin.DECKY_PLUGIN_LOG_DIR) / "std-out.log", "w")
std_err_file = open(Path(decky_plugin.DECKY_PLUGIN_LOG_DIR) / "std-err.log", "w")

class Plugin:
    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)

    async def kdeconnect_runner(self):
        await asyncio.sleep(5)
        decky_plugin.logger.info("KDE Connecter started")
        last_display = None
        proc = None
        while True:
            try:
                decky_plugin.logger.info("in loop")
                display = ":0"
                ret = subprocess.run(["xprop","-d",":0","-root"], capture_output=True)
                app_id = None
                for line in ret.stdout.decode("utf-8").split("\n"):
                    if "GAMESCOPE_FOCUSED_APP(CARDINAL)" in line:
                        app_id = line.split(" = ")[1]

                decky_plugin.logger.info(f"app id {app_id}")
                if app_id is None:
                    await asyncio.sleep(0.5)
                    continue

                if app_id != "769":
                    display = ":1"

                if display != last_display:
                    last_display = display
                    # env = os.environ.copy()
                    ret = subprocess.run(["pkill","kdeconnectd"])
                    proc = subprocess.Popen(["/home/deck/run_kde_connect.sh", display, "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    logger.info(proc)
                    logger.info(f"Starting KDE connect on DISPLAY {last_display}")
            except Exception:
                logger.info(traceback.format_exc())
            await asyncio.sleep(0.5)

    async def _main(self):
        try:
            loop = asyncio.get_event_loop()
            Plugin._runner_task = loop.create_task(Plugin.kdeconnect_runner(self))
            decky_plugin.logger.info("Initialized")
        except Exception:
            decky_plugin.logger.exception("main")
