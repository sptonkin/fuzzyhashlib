#!/bin/bash

# This is a reminder of what to do to build these libraries.
#
# Install pre-requisites:
# (general) git wget
# (ssdeep) automake build-essential libtool
# (tlsh) python-dev cmake
# (sdhash) TODO
#
# Putting it all together, try:
#    sudo apt-get install git wget automake build-essential libtool python-dev cmake


$BUILD_DIR=~/build

mkdir -p $BUILD_DIR

# Build ssdeep
pushd .
cd $BUILD_DIR
wget https://github.com/ssdeep-project/ssdeep/releases/download/release-2.14.1/ssdeep-2.14.1.tar.gz
tar xf ssdeep-2.14.1.tar.gz
cd ssdeep-2.14.1
./bootstrap && ./configure && make
popd
echo "######################################################################"
echo "LIB (SSDEEP): $BUILD_DIR/ssdeep-2.14.1/.libs/libfuzzy.so.VER"
echo "######################################################################"


# Build tlsh
pushd .
cd $BUILD_DIR
git clone https://github.com/trendmicro/tlsh.git
cd tlsh
./make.sh && cd py_ext && python setup.py build && cd ..
popd
echo "######################################################################"
echo "LIB (TLSH): $BUILD_DIR/py_ext/build/lib.linux-ARCH-PYVER/tlsh.so"
echo "######################################################################"


# Build sdhash
# TODO
