"""
ethiopian_calendar.py
~~~~~~~~~~~~~~~~~~~~~

A modern, object-oriented module for converting and manipulating
dates between the Ethiopian and Gregorian calendars.
"""

from datetime import date as PyDate, timedelta
from typing import NamedTuple

# --- Core Julian Day Number (JDN) Conversion Logic ---
# Ethiopian epoch: Meskerem 1, 1 EC = 29 Aug 8 AD (Julian)
_ETHIOPIAN_EPOCH = 1724220  


def _eth_to_jdn(year: int, month: int, day: int) -> int:
    """Converts an Ethiopian date to JDN."""
    if not (1 <= month <= 13 and 1 <= day <= 30):
        raise ValueError("Invalid Ethiopian date. Months are 1-13, days 1-30.")
    if month == 13 and day > 6:
        raise ValueError("Pagume (13th month) has a maximum of 6 days.")

    return (
        _ETHIOPIAN_EPOCH
        + 365 * (year - 1)
        + (year // 4)
        + 30 * (month - 1)
        + day
        - 1
    )


def _jdn_to_eth(jdn: int) -> tuple[int, int, int]:
    """Converts a JDN to an Ethiopian date tuple."""
    r = (jdn - _ETHIOPIAN_EPOCH) % 1461
    n = (r % 365) + 365 * (r // 1460)
    year = 4 * ((jdn - _ETHIOPIAN_EPOCH) // 1461) + (r // 365) - (r // 1460)
    month = n // 30 + 1
    day = (n % 30) + 1
    return year, month, day


def _greg_to_jdn(year: int, month: int, day: int) -> int:
    """Converts a Gregorian date to JDN."""
    return PyDate(year, month, day).toordinal() + 1721425


def _jdn_to_greg(jdn: int) -> PyDate:
    """Converts a JDN to a Gregorian date object."""
    return PyDate.fromordinal(jdn - 1721425)


# --- Modern Date Objects (Public API) ---

class EthDate(NamedTuple):
    """Represents an Ethiopian date with conversion capabilities."""
    year: int
    month: int
    day: int

    def to_gregorian(self) -> "GregDate":
        jdn = _eth_to_jdn(self.year, self.month, self.day)
        greg_date = _jdn_to_greg(jdn)
        return GregDate.from_py_date(greg_date)

    @classmethod
    def from_gregorian(cls, greg_date: "GregDate") -> "EthDate":
        jdn = _greg_to_jdn(greg_date.year, greg_date.month, greg_date.day)
        y, m, d = _jdn_to_eth(jdn)
        return cls(year=y, month=m, day=d)


class GregDate(NamedTuple):
    """Represents a Gregorian date with conversion capabilities."""
    year: int
    month: int
    day: int

    def to_ethiopian(self) -> EthDate:
        jdn = _greg_to_jdn(self.year, self.month, self.day)
        y, m, d = _jdn_to_eth(jdn)
        return EthDate(year=y, month=m, day=d)

    @classmethod
    def from_py_date(cls, py_date: PyDate) -> "GregDate":
        return cls(year=py_date.year, month=py_date.month, day=py_date.day)


# --- Calendar Generator ---

def generate_ethiopian_calendar(year: int):
    """Yields EthDate objects for all days of a given Ethiopian year."""
    eth_date = EthDate(year, 1, 1)
    greg_date = eth_date.to_gregorian()
    py_date = PyDate(greg_date.year, greg_date.month, greg_date.day)

    while True:
        eth = GregDate.from_py_date(py_date).to_ethiopian()
        if eth.year != year:
            break
        yield eth
        py_date += timedelta(days=1)


# --- Example Usage ---

if __name__ == "__main__":
    eth_new_year = EthDate(2018, 1, 1)
    print("Ethiopian New Year 2018:", eth_new_year)
    print("→ Gregorian:", eth_new_year.to_gregorian())  # Expected: 2025-09-11

    today = GregDate(2025, 9, 16)
    print("\nGregorian today:", today)
    print("→ Ethiopian:", today.to_ethiopian())  # Expected: 2018-01-06

    print("\n--- First 5 days of Ethiopian 2018 ---")
    for i, eth_day in enumerate(generate_ethiopian_calendar(2018)):
        print(f"Day {i+1}: {eth_day}")
        if i >= 4:
            break
