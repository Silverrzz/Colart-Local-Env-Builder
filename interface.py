"""

This file contains the interface code for all functionality in cleb
Do not alter this file unless necessary.
Running this file will have no effect.

"""

#Local config

#Package imports

import json
import sys
from colorama import Fore, Style
import time
import subprocess

#Internal Functionality

class Config:
    def __init__(self, private):
        self.private = private
        self._raw = self._load_config()
        self.json = self._raw["public" if not private else "private"]

    def get_value(self, v_name):
        return self.json[v_name]

    def set_value(self, v_name, v_content):
        try:
            self.json[v_name] = v_content
            self._raw["public" if not self.private else "private"][v_name] = v_content
            if (self._save_config()):
                return True
            else:
                return False
        except Exception:
            return False

    def _load_config(self):
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        return config

    def _save_config(self):
        try:
            with open("config.json", "w+") as f:
                f.write(json.dumps(self._raw, indent=4))
            return True
        except Exception:
            return False

class States:
    class FATAL:
        code = 0
        col = Fore.RED
        val = "FATAL"

        def __str__(self):
            return States.FATAL.val

    class ERROR:
        code = 1
        col = Fore.RED
        val = "ERROR"

        def __str__(self):
            return States.ERROR.val

    class WARN:
        code = 2
        col = Fore.YELLOW
        val = "WARN"

        def __str__(self):
            return States.WARN.val

    class INFO:
        code = 3
        col = Fore.BLUE
        val = "INFO"

        def __str__(self):
            return States.INFO.val

    class OK:
        code = 4
        col = Fore.GREEN
        val = "OK"

        def __str__(self):
            return States.OK.val

    class IMPORTANT:
        code = 5
        col = Fore.MAGENTA
        val = "IMPORTANT"

        def __str__(self):
            return States.IMPORTANT.val

def process_state(state):
    if state == States.FATAL:
        sys.exit(1)

#External Functionality


class Interface:
    def get_config(private=False):
        return Config(private)

    def output(state, output):
        print(f"{Fore.LIGHTWHITE_EX}[{time.strftime('%H:%M:%S', time.gmtime())}] {state.col}[{state.val}] {Style.RESET_ALL}{output}")
        process_state(state)

    def run_checks():
        return True

    def system_command(cmd):
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        return bytes(result.stdout.read()).decode("utf-8"), result.returncode

    def increment_step():
        Interface.get_config(private=True).set_value("STEP_CODE", Interface.get_config(private=True).get_value("STEP_CODE") + 1)

    def reset_step():
        Interface.get_config(private=True).set_value("STEP_CODE", 0)

    def request_restart():
        Interface.output(States.IMPORTANT, "A system restart is required to continue!")
        Interface.output(States.INFO, f"The process is currently on step {Interface.get_config(private=True).get_value('STEP_CODE')}. If you have come across this restart before there may be a problem.")
        sys.exit()