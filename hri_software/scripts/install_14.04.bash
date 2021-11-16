#!/bin/bash

# Directory in which software packages will be copied
MAIN_DIR=../src

# Catkin workspace fot his project
ROS_CATKIN_SRC=../catkin_ws/src


# Install required Linux libs and applications

echo "Install system libraries"

sudo apt-get update
sudo apt-get install cmake g++ xterm libboost1.54-dev libxml2 libxml2-dev libxml++2.6-dev flex libfltk1.1-dev

# Install ROS addons
sudo apt-get install ros-indigo-joystick-drivers ros-indigo-navigation


# Install libraries and ROS packages

echo "Install software libraries and ROS packages"

mkdir -p $MAIN_DIR
cd $MAIN_DIR

# PetriNetPlans

if [ ! -d PetriNetPlans ]; then
    git clone https://github.com/iocchi/PetriNetPlans
else
    cd PetriNetPlans; git pull; cd -
fi

# gradient_based_navigation
if [ ! -d gradient_based_navigation ]; then
    git clone https://github.com/Imperoli/gradient_based_navigation
else
    cd gradient_based_navigation; git pull; cd -
fi

# Stage environments

if [ ! -d stage_environments ]; then
	git clone https://bitbucket.org/iocchi/stage_environments.git
else
    cd stage_environments; git pull; cd -
fi

# SPQReL navigation

if [ ! -d spqrel_navigation ]; then
    git clone https://github.com/LCAS/spqrel_navigation
else
    cd spqrel_navigation; git pull; cd -
fi

# Rococo Navigation

if [ ! -d rococo_navigation ]; then
	git clone https://bitbucket.org/iocchi/rococo_navigation.git
else
    cd rococo_navigation; git pull; cd -
fi

# Rococo Laser Analysis

if [ ! -d laser_analysis ]; then
    git clone https://bitbucket.org/iocchi/laser_analysis.git
else
    cd laser_analysis; git pull; cd -
fi

# TCP interface

if [ ! -d tcp_interface ]; then
    git clone https://github.com/gennari/tcp_interface
else
    cd tcp_interface; git pull; cd -
fi

# DIAGO apps

if [ ! -d diago_apps ]; then
	git clone https://bitbucket.org/iocchi/diago_apps.git
else
    cd diago_apps; git pull; cd -
fi

# HRI-PNP

if [ ! -d hri_pnp ]; then
    git clone https://bitbucket.org/iocchi/hri_pnp.git
else
    cd hri_pnp; git pull; cd -
fi




# Setup catkin workspace

echp "Setup catkin workspace"

mkdir -p $ROS_CATKIN_SRC
cd $ROS_CATKIN_SRC

catkin_init_workspace
cd ..
catkin_make

# Create symbolic links to catkin/src

cd $ROS_CATKIN_SRC
ln -sf $MAIN_DIR/PetriNetPlans/PNPros/ROS_bridge/pnp_msgs .
ln -sf $MAIN_DIR/PetriNetPlans/PNPros/ROS_bridge/pnp_ros .
ln -sf $MAIN_DIR/gradient_based_navigation .
ln -sf $MAIN_DIR/stage_environments .
ln -sf $MAIN_DIR/spqrel_navigation .
ln -sf $MAIN_DIR/rococo_navigation .
ln -sf $MAIN_DIR/laser_analysis .
ln -sf $MAIN_DIR/tcp_interface .
ln -sf $MAIN_DIR/diago_apps .
ln -sf $MAIN_DIR/hri_pnp .
cd -



echo ""
echo "***** INSTALLATION INSTRUCTIONS *****"
echo ""
echo "1. Build external libraries (PNP) with 'make_external_libs.bash'"
echo "   You will be prompted for the sudo password to install PNP"
echo ""
echo "2. Setup the environment on your terminal"
echo "   $ cd <path_to>/hri_software/catkin_ws"
echo "   $ source devel/setup.bash"
echo ""
echo ""
echo "3. Run catkin_make from the catkin folder to build ROS packages"
echo ""

