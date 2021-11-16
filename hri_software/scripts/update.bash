#!/bin/bash

MAIN_DIR=`pwd`/../src

# Update packages
cd $MAIN_DIR

cd PetriNetPlans; git pull; cd -
cd gradient_based_navigation; git pull; cd -
cd stage_environments; git pull; cd -
cd spqrel_navigation; git pull; cd -
cd rococo_navigation; git pull; cd -
cd laser_analysis; git pull; cd -
cd tcp_interface; git pull; cd -
cd diago_apps; git pull; cd -
cd hri_pnp; git pull; cd -

