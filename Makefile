# CSTBox framework
#
# Makefile for building the Debian distribution package containing 
# the support for NMEA products connected via a serial link.
#
# author = Eric PASCUAL - CSTB (eric.pascual@cstb.fr)

# name of the CSTBox module
MODULE_NAME=ext-nmea-serial

include $(CSTBOX_DEVEL_HOME)/lib/makefile-dist.mk

copy_files: \
	check_metadata_files \
	copy_bin_files \
	copy_python_files \
	copy_init_scripts

