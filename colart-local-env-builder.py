import os

os.system("pip install docker")
os.system("pip install colorama")



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
        print(result.stdout.read().decode("utf-8")), result.returncode

    def increment_step():
        Interface.get_config(private=True).set_value("STEP_CODE", Interface.get_config(private=True).get_value("STEP_CODE") + 1)

    def reset_step():
        Interface.get_config(private=True).set_value("STEP_CODE", 0)

    def request_restart():
        Interface.output(States.IMPORTANT, "A system restart is required to continue!")
        Interface.output(States.INFO, f"The process is currently on step {Interface.get_config(private=True).get_value('STEP_CODE')}. If you have come across this restart before there may be a problem.")
        sys.exit()
        
import docker

try:

    execution_directory = os.getcwd()

    Interface.output(States.OK, "Starting...")

    if "spectre.sql.gz" not in os.listdir(execution_directory):
        Interface.output(States.INFO, "Downloading database")
        Interface.system_command(f"curl https://download852.mediafire.com/8x9i9nkxna3g/n0ok8pz6o7dch5l/spectre.sql.gz -o {execution_directory}/spectre.sql.gz")
    else:
        Interface.output(States.INFO, "Database already downloaded")

    Interface.output(States.INFO, "Cloning repository")
    Interface.system_command("wsl git clone git@bitbucket.org:colart/spectre-websites.git")
    Interface.output(States.INFO, "Installing dependencies")
    Interface.system_command("wsl sudo apt update")
    Interface.system_command("wsl sudo apt install gzip")
    Interface.system_command("wsl sudo apt install nodejs npm")
    Interface.system_command("wsl cd spectre-websites/;npm install")
    Interface.system_command("wsl sudo apt install gulp")
    Interface.output(States.INFO, "Building local website files")
    Interface.system_command("wsl cd spectre-websites/;gulp install")

    if "install-db-no-rename" not in os.listdir(execution_directory):
        Interface.output(States.INFO, "Downloading install-db.sh")
        Interface.system_command(f"curl https://download943.mediafire.com/cnfl1179l4og/buwhxxoj2ld96e1/install-db-no-rename -o {execution_directory}/install-db-no-rename")
    else:
        Interface.output(States.INFO, "install sh already downloaded")

    install_location = f"/mnt/{execution_directory.replace(':','/')}/install-db-no-rename"
    Interface.output(States.INFO, f"install-db.sh location: {install_location}")

    Interface.output(States.INFO, "Installing docker scripts")
    Interface.system_command("wsl mv spectre-websites/infrastructure/docker-local/docker/mariadb/install-db.sh spectre-websites/infrastructure/docker-local/docker/mariadb/temp-install-db")
    Interface.system_command(f"wsl mv {install_location} spectre-websites/infrastructure/docker-local/docker/mariadb/install-db.sh")
    Interface.output(States.INFO, "Creating docker containers")
    Interface.system_command("wsl cd spectre-websites/infrastructure/docker-local;docker compose up")
    Interface.output(States.INFO, "Removing temporary install script")
    Interface.system_command("wsl mv spectre-websites/infrastructure/docker-local/docker/mariadb/temp-install-db spectre-websites/infrastructure/docker-local/docker/mariadb/install-db.sh")

    db_directory = f"/mnt/{execution_directory.replace(':','/')}/spectre.sql.gz"
    Interface.output(States.INFO, f"Database location: {db_directory}")

    Interface.output(States.INFO, "Preparing database")
    Interface.system_command(f"wsl mv {db_directory} /tmp/spectre.sql.gz")
    Interface.system_command("wsl gzip -d /tmp/spectre.sql.gz")

    mariadb_container_id = docker.from_env().containers.get("spectre-mariadb").id

    Interface.system_command(f"docker cp /tmp/spectre.sql {mariadb_container_id}:/tmp/spectre.sql")

    Interface.output(States.INFO, "Installing database")
    Interface.system_command(f"docker exec -it {mariadb_container_id} /usr/bin/mysql --password=rootpassword spectre < /tmp/spectre.sql")

    Interface.output(States.OK, "Colart Local Environment Builder finished!")

    input("Press enter to continue...")

except Exception as e:
    Interface.output(States.FATAL, f"An error occurred: {e}")
    input("Press enter to continue...")