import decimaldate

print("Test: Leap Year")

assert decimaldate._isleapyear(400) is True
assert decimaldate._isleapyear(1000) is False
assert decimaldate._isleapyear(2000) is True
assert decimaldate._isleapyear(1984) is True
assert decimaldate._isleapyear(387) is False
assert decimaldate._isleapyear(-401) is True
assert decimaldate._isleapyear(-1001) is False
assert decimaldate._isleapyear(-2001) is True
assert decimaldate._isleapyear(-1985) is True
assert decimaldate._isleapyear(-388) is False

print("Test: ISO to Decimal, CE")

decver = decimaldate.iso2dec('2000-01-01')
expect = 2000.001366
assert decver == expect

decver = decimaldate.iso2dec('1999-01-01')
expect = 1999.001370
assert decver == expect

decver = decimaldate.iso2dec('2000-12-31')
expect = 2000.998634
assert decver == expect

decver = decimaldate.iso2dec('+1999-12-31')
expect = 1999.998630
assert decver == expect

decver = decimaldate.iso2dec('+1999-07-01')
expect = 1999.497260
assert decver == expect

print("Test: ISO to Decimal, BCE")

decver = decimaldate.iso2dec('-2000-01-01')
expect = -1999.998634
assert decver == expect

decver = decimaldate.iso2dec('-2000-12-31')
expect = -1999.001366
assert decver == expect

decver = decimaldate.iso2dec('-1000000-01-01')
expect = -999999.998634
assert decver == expect

decver = decimaldate.iso2dec('-1000000-12-31')
expect = -999999.001366
assert decver == expect

print("Test: Decimal to ISO, CE")

isover = decimaldate.dec2iso(2000.001366)
expect = '2000-01-01'
assert isover == expect

isover = decimaldate.dec2iso(1999.001370)
expect = '1999-01-01'
assert isover == expect

isover = decimaldate.dec2iso(2000.998634)
expect = '2000-12-31'
assert isover == expect

isover = decimaldate.dec2iso(1999.998630)
expect = '1999-12-31'
assert isover == expect

isover = decimaldate.dec2iso(1999.497260)
expect = '1999-07-01'
assert isover == expect

isover = decimaldate.dec2iso(1999.5)
expect = '1999-07-02'
assert isover == expect

isover = decimaldate.dec2iso(2000.5)
expect = '2000-07-02'
assert isover == expect

print("Test: ISO to Decimal, BCE")

isover = decimaldate.dec2iso(-2000.998634)
expect = '-2001-01-01'
assert isover == expect

isover = decimaldate.dec2iso(-2000.001366)
expect = '-2001-12-31'
assert isover == expect

isover = decimaldate.dec2iso(-1000000.998634)
expect = '-1000001-01-01'
assert isover == expect

isover = decimaldate.dec2iso(-1000000.001366)
expect = '-1000001-12-31'
assert isover == expect

print("All tests OK.")
