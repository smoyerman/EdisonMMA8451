# EdisonMMA8451
Edison Library in python for the MMA8451 accelerometer

Allows Edison to pull data from the MMA accelerometer using python and intel's mraa library. 

This library has a few dependencies. Installation instructions below.

1. Intel's mraa library - Install with 

$ echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
$ opkg update
$ opkg install libmraa0

2. NumPy

Install by sourcing alex T's repos. Instructions here: http://alextgalileo.altervista.org/edison-package-repo-configuration-instructions.html 

Then installing numpy

$ opkg update
$ opkg install python-numpy

An example script is provided with this repo.
