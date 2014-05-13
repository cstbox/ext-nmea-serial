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

__author__ = 'Eric PASCUAL - CSTB (eric.pascual@cstb.fr)'
__copyright__ = 'Copyright (c) 2013 CSTB'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'


class NMEASentence(object):
    """ Convenient decomposition of a NMEA sentence.

    Sentence is split into the following attributes:
        formatter:
            the first token, itself split into :
                typ:
                    the sentence type (first 2 chars of the formatter)
                talker_id:
                    the kind of equipment having produced the sentence
                    (remaining chars)
        fields:
            the data fields of the sentence
        crc:
            the sentence CRC if any (last token, past the '*')

    """
    talker_id = typ = formatter = crc = None
    fields = []

    def __init__(self, s = None):
        """ Constructor.

        :param str s: the sentence as a string (can include the opening '$')
        """
        self.clear()
        if s:
            self.parse(s)

    def clear(self):
        """ Empties all fields."""
        self.talker_id = self.typ = self.formatter = self.crc = None
        self.fields = []

    def parse(self, s):
        """ Parses a string supposed to be a complete NMEA sentence.

        :param str s: the string to be parsed (can omit the opening '$')
        """
        if s.startswith('$'):
            s = s[1:]
        if '*' in s:
            (flds, self.crc,) = s.split('*')
            self.fields = flds.split(',')
        else:
            self.fields = s.split(',')
        self.formatter = f0 = self.fields.pop(0)
        self.talker_id = f0[:2]
        self.typ = f0[2:]

    def __str__(self):
        """ Returns the rebuilt sentence as a string."""
        if self.crc:
            return '$%s%s,%s*%s' % (self.talker_id,
             self.typ,
             ','.join(self.fields),
             self.crc)
        else:
            return '$%s%s,%s' % (self.talker_id, self.typ, ','.join(self.fields))

    def pprint(self):
        """ Returns a pretty print form of the sentence."""
        return 'tlk=%s stype=%s flds=%s crc=%s' % (
            self.talker_id, self.typ, self.fields, self.crc
        )
