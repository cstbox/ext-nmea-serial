#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of CSTBox.
#
# CSTBox is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSTBox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CSTBox.  If not, see <http://www.gnu.org/licenses/>.

""" NMEA serial products hardware abstraction layer daemon. """

import sys
import logging
import serial
import os.path

import pycstbox.log as log
import pycstbox.cli as cli
import pycstbox.dbuslib as dbuslib
import pycstbox.serial_nmeasvc as serial_nmeasvc
import pycstbox.devcfg as devcfg

if __name__ == '__main__':
    log.setup_logging(os.path.basename(__file__))

    parser = cli.get_argument_parser('CSTBox Serial NMEA HAL')
    args = parser.parse_args()

    try:
        dbuslib.dbus_init()

        cfg = devcfg.DeviceNetworkConfiguration(autoload=True)
        svc = serial_nmeasvc.SerialNMEASvc(dbuslib.get_bus())

        svc.log_setLevel_from_args(args)
        # load the configuration data for serial NMEA coordinators
        svc.load_configuration(
            dict([(k, v) for k, v in cfg.iteritems() if v.type == 'serial-nmea'])
        )
        svc.start()

    except serial.SerialException as e:
        logging.critical(e)
        sys.exit(1)

    except Exception as e: #pylint: disable=W0703
        logging.exception(e)
        sys.exit(e)

