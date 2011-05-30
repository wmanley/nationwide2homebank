#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  nationwide2homebank - Nationwide to Homebank csv format converter
#
#  Copyright (C) 2011 William Manley <will@williammanley.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from itertools import izip_longest
import csv
import sys
import cStringIO
import unittest2
import nose

def reformat_date(nat):
    """Reformat the date from Nationwide format to a format understood by
    homebank
    
    >>> reformat_date("03 May 2011")
    '03/05/11'
    >>> reformat_date("15 December 2008")
    '15/12/08'
    >>> reformat_date("08 Jan 2010")
    '08/01/10'
    >>> reformat_date("11 Mar 2011")
    '11/03/11'
    >>> reformat_date("05 Jun 2010")
    '05/06/10'
    >>> reformat_date("10 Dec 2010")
    '10/12/10'
    >>> reformat_date("15 December 2008")
    '15/12/08'
    >>> reformat_date("05 March 2010")
    '05/03/10'
    """
    (day, month, year) = nat.split(" ")
    monthno = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }[month[:3]]
    return "%s/%s/%s" % (day, monthno, year[-2:])

def print_reformatted_csv(infile, outfile):
    r = csv.reader(infile)
    headings=None
    for i in iter(r):
        if headings == None:
            if len(i) > 1 and i[0] == "Date":
                headings = [x.strip() for x in i]
        else:
            m = dict(zip(headings, i))
            if "Date" in m and "Transactions" in m and "Debits" in m and "Credits" in m:
                if len(m["Debits"]) > 0:
                    diff = -float(m["Debits"].split("\xa3")[1])
                else:
                    diff = float(m["Credits"].split("\xa3")[1])
                outfile.write('%s;;;;"%s";%.02f;\n' % (reformat_date(m["Date"]), m["Transactions"], diff))

def assert_files_equal(expected, result):
    for i in izip_longest(iter(expected), iter(result)):
        nose.tools.eq_(i[0], i[1])

def flexaccount_parsing_test():
    result = cStringIO.StringIO()
    print_reformatted_csv(open("test/FlexAccount_test_input.csv", "r"), result)
    result.seek(0)
    assert_files_equal(open("test/FlexAccount_expected_output.csv", "r"), result)

def esavings_parsing_test():
    result = cStringIO.StringIO()
    print_reformatted_csv(open("test/esavings_test_input.csv", "r"), result)
    print "".join(result)
    result.seek(0)
    assert_files_equal(open("test/esavings_expected_output.csv", "r"), result)

def main(argv):
    if len(argv) < 2:
        infile = sys.stdin
    else:
        infile = open(argv[1], "r")
    print_reformatted_csv(infile, sys.stdout)

if __name__ == "__main__":
    main(sys.argv)

