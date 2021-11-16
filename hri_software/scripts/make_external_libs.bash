#!/bin/bash

# Directory in which software packages will be copied
MAIN_DIR=`pwd`/../src

# make external modules
cd $MAIN_DIR/PetriNetPlans/PNP
if [ ! -d build ]; then
  mkdir build
  cd build
  cmake ..
  cd ..
fi
cd build
make
sudo make install

cd ../../PNPgen
if [ ! -d build ]; then
  mkdir build
  cd build
  cmake ..
  cd ..
fi
cd build
make
sudo make install

echo ""
echo "Petri Net Plans built and installed"
echo ""



