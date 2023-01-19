from interface import States, Interface

Interface.output(States.OK, "Starting CLEB")

#First script to run is wsl-setup

import wsl_setup #Import the script
Interface.reset_step() #Reset step code
wsl_setup.script() #Run script

#Next script is docker_setup.py

import docker_setup #Import the script
Interface.reset_step() #Reset step code
docker_setup.script() #Run script