# HRI SOFTWARE 

This package contains instructions for installing and using software useful to develop HRI applications.

## INSTALL 

### OPTION 1 - DOCKER INSTALLATION 

* See [docker/README](docker/README.md)


### OPTION 2 - FULL LINUX INSTALLATION 

Note: instructions for this option have not been updated recently.

* See [scripts/README](scripts/README.md)



## TEST

Run each set of commands in a different terminal.
If you are using `tmux` in docker (default configuration), 
use `CTRL-b c` to create new tmux windows.

### NAOqi

* Run NAOqi

        cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64
        ./naoqi

* Run `pepper_tools` scripts

        cd ~/src/pepper_tools/memory
        python read.py

        cd ~/src/pepper_tools/say
        python say.py --sentence "Hello"




## Development

Use `playground` folder to write programs for your robot. Do not directly edit files in `pepper_tools`, as it will prevent future updates.


### Connection to Pepper robot

`pepper_tools` scripts connect to IP address stored in environment variable `PEPPER_IP`.

In the docker container, set robot's IP address

    export PEPPER_IP=<robot_IP>

Note: you have to execute this command in every terminal you want to use to connect to the robot.



### pepper_tools program

* Host OS

        cd ~/playground
        <your_preferred_editor> sayhello.py

            import os, sys

            sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

            import pepper_cmd
            from pepper_cmd import *

            begin()

            pepper_cmd.robot.say('Hello')

            end()


* Docker container (simulation mode)

    Execution will be emulated in the local naoqi system (no actions/sensing will be actually executed)

    Terminal 1:

        cd /opt/Aldebaran/naoqi-sdk-2.5.5.5-linux64
        ./naoqi

    Terminal 2:

        cd ~/playground
        python sayhello.py



* Docker container (robot mode)

    Execution will run on the robot

    Terminal 1:

        export PEPPER_IP=<robot_IP>

        cd ~/playground
        python sayhello.py


