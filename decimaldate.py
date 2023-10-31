"""
Convert a ISO-formatted date to a decimal date
Accounts for negative years (BCE) and for very large dates.
"""

import re
import math

RE_YEARMONTHDAY = re.compile(r'^(\-?\+?)(\d+)\-(\d\d)\-(\d\d)$')


def iso2dec(isodate):
    datepieces = re.match(RE_YEARMONTHDAY, isodate)
    if not datepieces:
        raise ValueError("Invalid date format {}".format(isodate))

    (plusminus, yearstring, monthstring, daystring) = datepieces.groups()
    if not _isvalidmonth(monthstring) or not _isvalidmonthday(yearstring, monthstring, daystring):
        raise ValueError("Invalid date {}".format(isodate))

    decbit = _propotionofdayspassed(yearstring, monthstring, daystring)
    if plusminus == '-':
        decbit = 1 - decbit

    yeardecimal = int(yearstring) + decbit
    if plusminus == '-' and yeardecimal > 0:  # ISO 8601 shift year<=0 by 1, 0=1BCE, -1=2BCE
        yeardecimal -= 1
    if plusminus == '-':
        yeardecimal *= -1

    return round(yeardecimal, 6)


def dec2iso(decdate):
    # strip the integer/year part
    # find how many days were in this year, multiply back out to get the day-of-year number
    if decdate >= 0:
        yearint = int(math.floor(decdate))
        plusminus = ''
    else:
        yearint = int(math.ceil(decdate))
        plusminus = '-'

    yearstring = str(abs(yearint))
    daysinyear = _daysinyear(yearstring)
    targetday = round(daysinyear * (decdate % 1), 1)

    # count up days months at a time, until we reach our target month
    # the the remainder days is the day of the month, offset by 1 cuz we count from 0
    dayspassed = 0
    for monthstring in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
        dtm = _daysinmonth(yearstring, monthstring)
        if dayspassed + dtm < targetday:
            dayspassed += dtm
        else:
            break

    daynumber = int(math.floor(targetday - dayspassed + 1))
    daystring = "{:02d}".format(daynumber)

    if plusminus == '-':  # ISO 8601 shift year<=0 by 1, 0=1BCE, -1=2BCE
        yearstring = str(abs(yearint) + 1)

    return "{}{}-{}-{}".format(plusminus, yearstring, monthstring, daystring)


def _propotionofdayspassed(yearstring, monthstring, daystring):
    # count the number of days to get to this day of this month
    dayspassed = 0
    for tms in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
        if tms < monthstring:
            dayspassed += _daysinmonth(yearstring, tms)
    dayspassed += int(daystring)

    # subtract 1 cuz day 0 is January 1 and not January 0
    # add 0.5 to get us 12 noon
    dayspassed -= 1
    dayspassed += 0.5

    # divide by days in year, to get decimal portion since noon of Jan 1
    daysinyear = _daysinyear(yearstring)
    return dayspassed / daysinyear


def _isvalidmonth(monthstring):
    validmonths = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    return monthstring in validmonths


def _isvalidmonthday(yearstring, monthstring, daystring):
    days = int(daystring)
    return days > 0 and days <= _daysinmonth(yearstring, monthstring)


def _daysinmonth(yearstring, monthstring):
    monthdaycounts = {
        '01': 31,
        '02': 28,  # February
        '03': 31,
        '04': 30,
        '05': 31,
        '06': 30,
        '07': 31,
        '08': 31,
        '09': 30,
        '10': 31,
        '11': 30,
        '12': 31,
    }

    if _isleapyear(yearstring):
        monthdaycounts['02'] = 29

    return monthdaycounts[monthstring]


def _daysinyear(yearstring):
    return 366 if _isleapyear(yearstring) else 365


def _isleapyear(yearstring):
    yearnumber = int(yearstring)
    isleap = yearnumber % 4 == 0 and (yearnumber % 100 != 0 or yearnumber % 400 == 0)
    return isleap
