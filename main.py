from core import to_gregorian, to_ethiopian
from core.calendar import EthiopianDate

print(to_gregorian(2018, 5, 5))   # Ethiopian → Gregorian
print(to_ethiopian(2025, 1, 13))  # Gregorian → Ethiopian

ed = EthiopianDate(2017, 12, 12)
print(ed.is_leap_year())

print(ed)