"""

This file contains the functionality to install Windows Subsystem for Linux
Do not alter this file unless necessary.
Configuration to enable, disable or edit the functionality of this program can be accessed via the CLI or Application.

"""

#Local config

_SCRIPT_NAME = "wsl_setup"
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

############################################################################################################################################
#                                                                                                                                          #
#                                             SETUP END - DO NOT EDIT AFTER THIS LINE                                                      #
#                                                                                                                                          #
############################################################################################################################################

def script():

    Interface.output(States.OK, "Starting WSL Setup!")

    if Interface.get_config(private=True).get_value("STEP_CODE") == 0:

        Interface.system_command("dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")
        Interface.system_command("dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart")
        
        
        Interface.output(States.INFO, "Installing WSL2")
        Interface.increment_step()
        message, code = Interface.system_command("powershell.exe wsl --install")
        Interface.output(States.INFO, "Updating WSL2")
        Interface.increment_step()
        message, code = Interface.system_command("powershell.exe wsl --update")

    Interface.output(States.OK, "WSL2 is installed.")

    if Interface.get_config(private=True).get_value("STEP_CODE") == 2:
        
        Interface.output(States.INFO, "Starting UNIX setup.")
        Interface.increment_step()
        message, code = Interface.system_command("wsl exit")

    Interface.output(States.OK, "UNIX is set up.")

    Interface.output(States.OK, "WSL has finished setup.")
