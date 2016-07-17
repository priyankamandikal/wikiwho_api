from __future__ import division
import datetime
from dateutil import parser
import sys
from math import modf

MJD_0 = 2400000.5

def ipart(x):
    """Return integer part of given number."""
    return modf(x)[1]

def gcal2jd(year, month, day):

    a = ipart((month - 14) / 12.0)
    jd = ipart((1461 * (year + 4800 + a)) / 4.0)
    jd += ipart((367 * (month - 2 - 12 * a)) / 12.0)
    x = ipart((year + 4900 + a) / 100.0)
    jd -= ipart((3 * x) / 4.0)
    jd += day - 2432075.5  # was 32075; add 2400000.5

    jd -= 0.5  # 0 hours; above JD is for midday, switch to midnight.

    return MJD_0, jd

def jd2gcal(jd1, jd2):
    jd1_f, jd1_i = modf(jd1)
    jd2_f, jd2_i = modf(jd2)

    jd_i = jd1_i + jd2_i

    f = jd1_f + jd2_f

    # Set JD to noon of the current date. Fractional part is the
    # fraction from midnight of the current date.
    if -0.5 < f < 0.5:
        f += 0.5
    elif f >= 0.5:
        jd_i += 1
        f -= 0.5
    elif f <= -0.5:
        jd_i -= 1
        f += 1.5

    l = jd_i + 68569
    n = ipart((4 * l) / 146097.0)
    l -= ipart(((146097 * n) + 3) / 4.0)
    i = ipart((4000 * (l + 1)) / 1461001)
    l -= ipart((1461 * i) / 4.0) - 31
    j = ipart((80 * l) / 2447.0)
    day = l - ipart((2447 * j) / 80.0)
    l = ipart(j / 11.0)
    month = j + 2 - (12 * l)
    year = 100 * (n - 49) + i + l

    return int(year), int(month), int(day), f

if __name__ == '__main__':

    try:
        ifilename = str(sys.argv[1])    # input file containing dates for the analysis
    except:
        print("Filename missing!")

    with open(ifilename,'r') as ifile:
        jd1_sum = 0.0
        for cnt,line in enumerate(ifile):
            date = parser.parse(line[:10])
            jd1_sum += gcal2jd(date.year, date.month, date.day)[1]
        jd1_mean = jd1_sum/(cnt+1)
        jd_mean = MJD_0 + jd1_mean
        mean_date = jd2gcal(MJD_0, jd1_mean)
        print mean_date[:3]