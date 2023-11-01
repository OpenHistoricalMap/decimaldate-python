#!python3

import decimaldate

# a list of tests: function, input, output
tests = [
    ['isleapyear', 2000, True],
    ['isleapyear', 1900, False],
    ['isleapyear', 1, False],
    ['isleapyear', 4, True],
    ['isleapyear', -1, True],
    ['isleapyear', -2000, False],
    ['isleapyear', -1900, False],
    ['isleapyear', -2001, True],
    ['isleapyear', -1901, False],
    ['dec2iso', -0.998633, '-0001-01-01'],
    ['dec2iso', -0.5, '-0001-07-02'],  # non leap year, 1823rd day is July 2
    ['dec2iso', -0.001366, '-0001-12-31'],
    ['dec2iso', 0.001367, '0000-01-01'],
    ['dec2iso', 0.5, '0000-07-01'],  # 1 BCE, leap year; 183rd day is July 1 due to February being longer
    ['dec2iso', 0.998634, '0000-12-31'],  # 1 BCE, leap year; 183rd day is July 1 due to February being longer
    ['dec2iso', +1.001369, '0001-01-01'],
    ['dec2iso', +1.5, '0001-07-02'],  # non leap year, 1823rd day is July 2
    ['dec2iso', +1.998631, '0001-12-31'],
    ['dec2iso', +2.001369, '0002-01-01'],
    ['dec2iso', +2.5, '0002-07-02'],  # non leap year, 1823rd day is July 2
    ['dec2iso', +2.998631, '0002-12-31'],
    ['iso2dec', '-0002-01-01', -1.99863],
    ['iso2dec', '-0002-07-02', -1.5],  # non leap year, 1823rd day is July 2
    ['iso2dec', '-0002-12-31', -1.00137],
    ['iso2dec', '-0001-01-01', -0.99863],
    ['iso2dec', '-0001-07-02', -0.5],  # non leap year, 1823rd day is July 2
    ['iso2dec', '-0001-12-31', -0.00137],
    ['iso2dec', '0000-01-01', 0.00137],  # 1 BCE, leap year; 183rd day is July 1 due to February being longer
    ['iso2dec', '0000-07-02', 0.50137],  # 1 BCE, leap year; 183rd day is July 1 due to February being longer
    ['iso2dec', '0000-12-31', 0.99863],
    ['iso2dec', '0001-01-01', +1.00137],
    ['iso2dec', '0001-07-02', +1.5],  # non leap year, 1823rd day is July 2
    ['iso2dec', '0001-12-31', +1.99863],
    ['iso2dec', '0002-01-01', +2.00137],
    ['iso2dec', '0002-07-02', +2.5],  # non leap year, 1823rd day is July 2
    ['iso2dec', '0002-12-31', +2.99863],
]

print("Starting tests.")
passcount = 0
failcount = 0

for thistest in tests:
    (funcname, argin, expected) = thistest
    func = getattr(decimaldate, funcname)
    result = func(argin)

    if result == expected:
        print(f"OK    {funcname}({argin}) = {expected}")
        passcount += 1
    else:
        print(f"FAIL    {funcname}({argin}) returned {result} instead of expected {expected}")
        failcount += 1

print("");
print("All tests done.")
print(f"{passcount} tests OK.");
print(f"{failcount} tests failed.");
