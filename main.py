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

class Plugin:
    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)

    async def kdeconnect_runner(self):
        decky_plugin.logger.info("KDE Connecter started")
        last_display = None
        while True:
            try:
                decky_plugin.logger.info("in loop")
                display = ":0"
                ret = subprocess.run(["xprop","-d",":0","-root"], capture_output=True)
                app_id = None
                for line in ret.stdout.decode("utf-8").split("\n"):
                    if "GAMESCOPE_FOCUSED_APP(CARDINAL)" in line:
                        app_id = line.split(" = ")[1]

                if app_id is None:
                    await asyncio.sleep(0.5)
                    continue

                if app_id != "769":
                    display = ":1"

                if display != last_display:
                    last_display = display
                    logger.info(f"Starting KDE connect on DISPLAY {last_display}")
                    env = os.environ.copy()
                    env["DISPLAY"] = last_display
                    ret = subprocess.run(["pkill","kdeconnectd"])
                    subprocess.Popen(["/usr/lib/kdeconnectd", "--replace", "&"], env=env, close_fds=True)
            except Exception:
                decky_plugin.logger.info("watchdog")
            await asyncio.sleep(0.5)

    async def _main(self):
        try:
            loop = asyncio.get_event_loop()
            Plugin._runner_task = loop.create_task(Plugin.kdeconnect_runner(self))
            decky_plugin.logger.info("Initialized")
        except Exception:
            decky_plugin.logger.exception("main")
