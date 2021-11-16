# FULL LINUX INSTALLATION

You first need ROS Kinetic on Ubuntu 16.04
(follow instructions in www.ros.org)


## Option 1

Install software packages following `Dockerfile` in the `docker` folder of this reository.

## Option 2

Note: this option is not maintained. Use at your own risk!!!

* Quick installation of a catkin workspace within the hri_software folder

        ./install_16.04.bash


    Note: installation requires sudo password to install system libraries.

    Note: If you want to install the softwre in an already existing catkin workspace, you need to properly modify the `install_XX.bash` script or do the equivalent manual operations.

   
* Build external libraries 
  (sudo password will be asked to install PNP)

        ./make_external_libs.bash  

    Note: make sure that the folder `\usr\local\lib` is in your ldconfig path or in the environment variable `LD_LIBRARY_PATH` and that `\usr\local\lib` is in your environment variable `PATH`. If not, use the following instructions. It may be necessary to add the export instructions in your `.bashrc` file.

        export PATH=/usr/local/lib:$PATH
        export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
        sudo ldconfig

* Compile the ROS packages

        cd catkin_ws
        source devel/setup.bash
        catkin_make


