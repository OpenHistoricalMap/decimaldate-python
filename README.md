# decimaldate.py

Convert a ISO-formatted date to a decimal date, accounting for negative years (BCE) and for very large dates (-1000000-01-01).

The returned decimal date is the year plus a decimal portion indicating "how far along" it was into the year on 12 noon of that day. For example, January 1 would be 0.5 days out of 365 so would have a decimal portion of 0.00136986.

This treats the Gregorian calendar as proleptic, continuing with leap years every fourth year (except centuries, except-except 4th centuries) into positive and negative infinity. As such, approximately every fourth year `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)` will have 366 days, as we are accustomed today.


### Usage and Examples

```
import decimaldate

print( decimaldate.iso2dec('2000-02-28') )    # 2000.15984

print( decimaldate.iso2dec('540-01-31')  )    # 540.08333   note the small decimal portion, since Jan 1 is closer to 0 origin when CE
print( decimaldate.iso2dec('-540-01-31')  )   # -539.91667  note the large decimal portion, since Jan 1 is further from 0 origin when BCE

print( decimaldate.iso2dec('1900-02-29')  )   #  error, this would not have been a leap year

print( decimaldate.dec2iso(1999.0013700) )    # 1999-01-01
print( decimaldate.dec2iso(1999.497260) )     # 1999-07-01
print( decimaldate.dec2iso(-550.9164383) )    # -0551-01-31  negative year, large decimal portion because January is further from 0 origin
print( decimaldate.dec2iso(-550.0835617) )    # -0551-12-01  negative year, small decimal portion because December is closer to 0 origin
```


### Dates Less Than 0001-01-01

This follows ISO 8601 in that year 0000 is 1 BCE, -0001 is 2 BCE, and so on. Expect negative dates to seem off by 1.

```
// positive dates are what you expect
print( decimaldate.iso2dec('2000-01-01') )  # 2000.001366
print( decimaldate.dec2iso(2000.001366) )   # 2000-01-01

// off by 1: 0 = 1, -1 = -2, and so on
print( decimaldate.iso2dec('-2000-01-01') )  # -1999.998634
print( decimaldate.dec2iso(-2000.998634) )   # -2001-01-01

// but it unpacks the same
print( decimaldate.dec2iso(decimaldate.iso2dec('-1000-06-30')) )  # -1000-06-30
```


### Year 0 and the Number Line

The Gregorian calendar has no year 0, and the morning after Dec 31 of 1 BCE would be Jan 1 of 1 CE.

On a number line from BCE to CE, the value 0 would appear at the cusp between December 31 1 BCE (0000-12-31) and January 1 1 CE (0001-01-01).

Decimaldate can be thought of as an offset on that number line.
- +0.25 would be 3 months forward into 1 CE (early April)
- +1.5 would be a year and a half forward from 0, so early July of 2 CE
- -0.5 would be half a year backward into 1 BCE (early October)
- -1.5 would be a year and a half backward from 0, so early July of 2 BCE

However, decimaldate shifts the origin by 1 year to make positive dates look more intuitive. While it is mathematically correct that +2022.9 is November 2023, people reading decimal dates visually just didn't like the numbers looking like that. As such, +1 is added to decimal dates.

| true decimal | decimaldate | iso | comment |
| --- | --- | --- | --- |
| -1.998633 | -0.998633 | -0001-01-01 | first day of 2 CE, most negative (highest decimal portion) day of the year |
| -1.001366 | -0.001366 | -0001-12-31 | the last day of 2 BCE, least negative (lowest decimal portion) day of the year |
| -0.998633 | 0.001367 | 0000-01-01 | first day of 1 BCE, most negative (highest decimal portion) day of the year |
| -0.5 | 0.5 | 0000-07-02 | middle of 1 BCE, 6 months before the 0 origin of Jan 1 1 CE |
| -0.001366 | 0.998634 | 0000-12-31 | the last day of 1 BCE, least negative (lowest decimal portion) day of the year |
| 0 | 1 | cusp | the cusp between Dec 31 1 BCE (0000-12-31) and Jan 1 1 CE (0001-01-01) |
| +0.001369 | +1.001369 | 0001-01-01 | the first day of 1 CE, least positive day of the year |
| +0.5 | +1.5 | 0001-07-01 | middle of 1 CE, 6 months after the 0 origin of Jan 1 1 CE |
| +0.998631 | +1.998631 | 0001-12-31 | last day of 1 CE, most positive day of the year |
| +1.001369 | +2.001369 | 0002-01-01 | the first day of 2 CE, least positive day of the year |
| +1.998631 | +2.998631 | 0002-12-31 | last day of 2 CE, most positive day of the year |


### Our Use Case and Technical Challenges

At OpenHistoricalMap, for the purpose of filtering vector tiles, we needed a method of converting dates into a number which could be unequivocally compared as `>=` and `<=`.

* Dates in ISO 8601 string format such as _2000-01-01_ fall flat when dealing with BCE dates, e.g. _-2500-01-01_ is greater than _-2499-12-31_
* We need support outside the range of the Unix epoch (1900-2039) and earlier than that of the Julian calendar (_-4713-01-01_).
  * Existing libraries do not support dates outside of their range. Dates prior to 0 J are out of range in Python and in PostgreSQL, and are silently (erroneously) converted to 0 J by PHP. Underlying C libraries using `struct tm` do not work outside of Unix epoch range.

Effectively, this means we had to create our own implementation of the R `decimal_date()` function, without recourse to underlying libraries.

As such, the technique chosen here is to convert the specified date into a decimal year, without recourse to the underlying date/time libraries.
* Dates are supplied in ISO 8601-like format and support positive and negative years, e.g. _-2000-01-01_ and _2000-01-01_ and _+2000-01-01_
* The Gregorian calendar is treated as proleptic: 365 or 366 says, February 29 existing only when `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`
* The returned decimal value represents the year, plus a decimal portion indicating "how far along" the year is at 12 noon on the given day. Keep in mind that since years vary between 365 and 336 days' length, the decimal "value" of a date may vary between years:
  * Example: 1999 has 365 days, so 12 noon on January 1 would be _1999.00136986_ and on December 31 would be _1999.99863014_
  * Example: 2000 has 366 days, so 12 noon on January 1 would be _2000.00136612_ and on December 31 would be _2000.99863388_
* In the case of negative years (BCE dates) the decimal portion is "inverted" into days from December 31, since December of a BCE year is closer to the 0 mark.
  * Example: Dec 31 2000 BCE is _-2000.00136612_ and Jan 1 2000 BCE is _-2000.99863388_
