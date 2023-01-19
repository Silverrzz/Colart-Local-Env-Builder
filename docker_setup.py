"""

This file contains the functionality to install Docker Desktop and all the containers needed.
Do not alter this file unless necessary.
Configuration to enable, disable or edit the functionality of this program can be accessed via the CLI or Application.

"""

#Local config

_SCRIPT_NAME = "docker_setup"
_SAFE_MSG = "(Safe mode is enabled)"

#Package imports

import os
import sys
import shutil
import subprocess

#Local imports

from interface import States, Interface

#Safety checks

SAFE_MODE = Interface.get_config().get_value("SAFE_MODE")

if SAFE_MODE:

    if not Interface.run_checks():
        assert(f"{_SCRIPT_NAME} > Script execution attempt failed: Interface did not pass all checks {_SAFE_MSG}")
        sys.exit(1)

#Script config

SCRIPT_ENABLED = Interface.get_config().get_value("INSTALL_DOCKER")
DOCKER_DRIVE = input("Path to install docker desktop: ")

############################################################################################################################################
#                                                                                                                                          #
#                                             SETUP END - DO NOT EDIT AFTER THIS LINE                                                      #
#                                                                                                                                          #
############################################################################################################################################

def script():

    Interface.output(States.OK, "Starting Docker setup!")
    Interface.output(States.INFO, "Downloading docker desktop.")
    Interface.system_command(f"curl https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe --output {DOCKER_DRIVE}/docker.exe")
    Interface.output(States.INFO, "Docker desktop downloaded, running installer.")
    Interface.system_command(f"{DOCKER_DRIVE}/docker.exe")
