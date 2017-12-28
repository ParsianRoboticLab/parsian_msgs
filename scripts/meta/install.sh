#! /bin/bash

# install header files
rm -f ../../../parsian_util/include/parsian_util/action/autogenerate/*
cp ./out/*.h ../../../parsian_util/include/parsian_util/action/autogenerate/

# install source files
rm -f ../../../parsian_util/src/action/autogenerate/*
cp ./out/*.cpp ../../../parsian_util/src/action/autogenerate/
