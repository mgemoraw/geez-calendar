from core.ethiopian_date import EthiopianDate

# Create Ethiopian date
eth_date = EthiopianDate(2016, 1, 1)  # 1 Meskerem 2016

# Convert to Gregorian
print(eth_date.to_gregorian())   # (2023, 9, 11)

# Convert Gregorian to Ethiopian
eth_from_greg = EthiopianDate.from_gregorian(2023, 9, 11)
print(eth_from_greg)  # EthiopianDate(2016, 1, 1)

# Today's Ethiopian date
print(EthiopianDate.today())
