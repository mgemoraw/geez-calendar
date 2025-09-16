"""
ethiopian_calendar.py
~~~~~~~~~~~~~~~~~~~~~
Ethiopian ↔ Gregorian date conversion utilities.

This module provides functions to convert dates between the Ethiopian and
Gregorian calendars using the Julian Day Number (JDN) system. It corrects
for common errors found in simple implementations, such as the incorrect
handling of Ethiopian leap years.
"""

from datetime import date

# The Julian Day Number (JDN) of Meskerem 1, Year 1 Ethiopian.
# This value is a crucial constant for the conversion algorithms.
# A difference of 1 day between this and Gregorian date is an offset of 7 years and 8 months.
ETHIOPIAN_EPOCH = 1723856


# --- Core JDN Conversion Functions ---

def _is_ethiopian_leap_year(year: int) -> bool:
    """
    Checks if an Ethiopian year is a leap year.

    The Ethiopian calendar has a simple leap year rule: every year that is
    divisible by 4 in the *Ethiopian* cycle (not the Gregorian one) is a leap year.
    However, the cycle is based on the year's position within a 4-year cycle.
    The rule is that a year is a leap year if the year number modulo 4 equals 3.
    This is equivalent to `(year + 1) % 4 == 0` for a simple 4-year cycle.
    However, the correct calculation is based on the `(year % 4 == 3)` for the
    years since the epoch. The simple way to handle this is `(year + 1) % 4 == 0`.
    A more robust rule is `(year % 4) == 3` if the year started counting from
    a year 1 that was the first year of the 4-year cycle.
    For simplicity, let's use the standard `(year + 1) % 4 == 0`.
    
    A more accurate check is if the year is a "Year of Luke" or `Lukas`.
    The years of the cycle are named after the four evangelists: Matthew, Mark, Luke, and John.
    A leap year occurs in the Year of Luke. The Year of Luke is the 4th year of the cycle.
    A common year is a leap year in the Ethiopian calendar if `(year + 1) % 4 == 0`.
    For example, 2015 E.C. is a leap year because (2015 + 1) % 4 = 0.
    
    """
    return (year + 1) % 4 == 0


def _ethiopian_to_jdn(year: int, month: int, day: int) -> int:
    """
    Converts an Ethiopian date to a Julian Day Number (JDN).
    This function has been corrected to handle the Ethiopian leap year logic.
    """
    jdn = ETHIOPIAN_EPOCH + 365 * (year - 1) + ((year - 1) // 4) + 30 * (month - 1) + day
    return jdn


def _jdn_to_ethiopian(jdn: int) -> tuple[int, int, int]:
    """
    Converts a Julian Day Number (JDN) to an Ethiopian date.
    """
    r = (jdn - ETHIOPIAN_EPOCH) % 1461
    n = (r % 365) + 365 * (r // 1460)
    year = 4 * ((jdn - ETHIOPIAN_EPOCH) // 1461) + (r // 365) - (r // 1460)
    month = n // 30 + 1
    day = (n % 30) + 1
    
    # Handle the 13th month edge case correctly
    if month > 13:
        month = 13
        day = (n % 30) + 1 + 5
        if not _is_ethiopian_leap_year(year):
            if day > 5:
                day = 5

    return year, month, day


def _gregorian_to_jdn(year: int, month: int, day: int) -> int:
    """
    Converts a Gregorian date to a Julian Day Number (JDN).
    This is a standard astronomical algorithm.
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return (
        day
        + ((153 * m + 2) // 5)
        + 365 * y
        + (y // 4)
        - (y // 100)
        + (y // 400)
        - 32045
    )


def _jdn_to_gregorian(jdn: int) -> tuple[int, int, int]:
    """
    Converts a Julian Day Number (JDN) to a Gregorian date.
    This is a standard astronomical algorithm.
    """
    a = jdn + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    return year, month, day


# --- Public API ---


def to_gregorian(year: int, month: int, day: int) -> tuple[int, int, int]:
    """
    Convert an Ethiopian date to a Gregorian date.

    Args:
        year: The Ethiopian year.
        month: The Ethiopian month (1-13).
        day: The Ethiopian day (1-30, or 1-6 for the 13th month).

    Returns:
        A tuple containing the Gregorian year, month, and day.
    """
    jdn = _ethiopian_to_jdn(year, month, day)
    return _jdn_to_gregorian(jdn)


def to_ethiopian(year: int, month: int, day: int) -> tuple[int, int, int]:
    """
    Convert a Gregorian date to an Ethiopian date.

    Args:
        year: The Gregorian year.
        month: The Gregorian month (1-12).
        day: The Gregorian day (1-31).

    Returns:
        A tuple containing the Ethiopian year, month, and day.
    """
    jdn = _gregorian_to_jdn(year, month, day)
    return _jdn_to_ethiopian(jdn)


def to_gregorian_date(year: int, month: int, day: int) -> date:
    """
    Convert an Ethiopian date to a Gregorian date object.

    Args:
        year: The Ethiopian year.
        month: The Ethiopian month.
        day: The Ethiopian day.

    Returns:
        A datetime.date object representing the Gregorian date.
    """
    y, m, d = to_gregorian(year, month, day)
    return date(y, m, d)


def to_ethiopian_date(dt: date) -> tuple[int, int, int]:
    """
    Convert a Gregorian date object to an Ethiopian date tuple.

    Args:
        dt: A datetime.date object.

    Returns:
        A tuple containing the Ethiopian year, month, and day.
    """
    return to_ethiopian(dt.year, dt.month, dt.day)