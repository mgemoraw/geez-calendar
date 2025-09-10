from core.ethiopian_date import EthiopianDate

# Ethiopian → Gregorian
eth = EthiopianDate(2017, 13, 5)  
print(eth.to_gregorian())  
# (202, 9, 11)

# Gregorian → Ethiopian
eth2 = EthiopianDate.from_gregorian(2023, 9, 11)
print(eth2)  
# 1 Meskerem 2016

# Leap year check
print(EthiopianDate.is_leap(2015))  # False
print(EthiopianDate.is_leap(2016))  # True
