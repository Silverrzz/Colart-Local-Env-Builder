"""

This file contains the functionality to install Windows Subsystem for Linux
Do not alter this file unless necessary.
Configuration to enable, disable or edit the functionality of this program can be accessed via the CLI or Application.

"""

#Local config

_SCRIPT_NAME = "wsl-setup"
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

SCRIPT_ENABLED = Interface.get_config().get_value("INSTALL_WSL")
USR_USERNAME = Interface.get_config().get_value("USERNAME")
USR_PASSWORD = Interface.get_config().get_value("PASSWORD")

############################################################################################################################################
#                                                                                                                                          #
#                                             SETUP END - DO NOT EDIT AFTER THIS LINE                                                      #
#                                                                                                                                          #
############################################################################################################################################

Interface.output(States.OK, "Starting WSL Setup!")
Interface.output(States.INFO, "Installing WSL2")

message, code = Interface.system_command("wsl --install")

if code is None:
    Interface.request_restart(1)