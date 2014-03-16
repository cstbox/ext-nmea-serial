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

"""
Specialized HAL classes for the implementation of coordinators and devices based on
NMEA serial communications.
"""

from pycstbox.hal.c_serial import SerialCoordinatorServiceObject
from pycstbox.hal.device import HalDevice
from pycstbox.nmea import NMEASentence

_STATE_IDLE, _STATE_IN_SENTENCE = xrange(2)


class NMEACoordinator(SerialCoordinatorServiceObject):
    """ Specialized serial coordinator handling NMEA equipments.
    """

    _parsing_state = _STATE_IDLE
    _rx_bytes = []

    def dispatch_received_data(self, data):
        """ Dedicated incoming data handler.

        Parses the NMEA sentence when complete and pass it to all available devices for it to be
        processed by the one it is related to. This device will be responsible for building the
        corresponding events sequence and return it as processing result.

        :param data: bytes received on the serial link
        :return: the list of corresponding events to be emitted
        """
        events = []
        for c in data:
            if self._parsing_state == _STATE_IDLE:
                if c == '$':
                    self._rx_bytes = []
                    self._parsing_state = _STATE_IN_SENTENCE

            elif self._parsing_state == _STATE_IN_SENTENCE:
                if c in ('\r', '\n'):
                    sentence = NMEASentence(''.join(self._rx_bytes))
                    for id_, cfg, haldev in self._devices.itervalues():
                        self.log_debug("passing sentence '%s' to device %s" %
                                       (sentence, id_)
                                       )
                        outputs = haldev.process_sentence(sentence)
                        if outputs:
                            events.extend(haldev.create_events(outputs))

                    self._parsing_state = _STATE_IDLE

                else:
                    self._rx_bytes.append(c)

        return events


class NMEADevice(HalDevice):
    """ A specialized HalDevice to be used as the basis for NMEA devices
    modeling.

    It adds the provision for the NMEA sentence processing which must be
    implemented by descendants to make the device behaviour comply with the
    multiple outputs device paradigm.
    """
    _hwdev = None

    def process_sentence(self, sentence):
        """ Process a parsed NMEA sentence and returns the values of the
        correspondant outputs if relevant.

        :param NMEAsentence sentence: the instance to be processed
        :returns:
            An object instance containing the values of the device outputs as
            attributes. Attribute names must match with the output names declared in the
            device descriptor file. It can be an equivalent named tuple.
            None is returned if this sentence is not relevant for the device.
        """
        try:
            outputs = self._hwdev.process_sentence(sentence)
            if outputs and type(outputs) is not tuple:
                raise Exception(
                    'returned outputs is not a tuple' % str(self._hw_dev)
                )
            return outputs

        except ValueError as e:
            self.coord.log_error(e)
        except Exception as e:
            self.coord.log_exception(e)

        return None

