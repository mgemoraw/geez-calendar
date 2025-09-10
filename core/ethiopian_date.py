from datetime import date, timedelta

class EthiopianDate:
    """
    Ethiopian Calendar Date with proper handling of 30-day months and Pagume.
    Supports conversion to/from Gregorian.
    """

    MONTHS = [
        "Meskerem", "Tikimt", "Hidar", "Tahesas", "Tir", "Yekatit",
        "Megabit", "Miyazya", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"
    ]

    # Gregorian date for 1 Meskerem 1 (Ethiopian) = 29 August 8 AD (Julian) = 11 September 8 AD (Gregorian)
    ETHIOPIAN_EPOCH = 1723856  # JDN of Meskerem 1, year 1

    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __repr__(self):
        return f"EthiopianDate({self.year}, {self.month}, {self.day})"

    def __str__(self):
        return f"{self.day} {self.MONTHS[self.month - 1]} {self.year}"

    # ---- Leap year ----
    @staticmethod
    def is_leap(year: int) -> bool:
        return (year + 1) % 4 == 0

    # ---- Ethiopian → JDN ----
    @staticmethod
    def _eth_to_jdn(year, month, day):
        jdn = (EthiopianDate.ETHIOPIAN_EPOCH
               + 365 * (year - 1)
               + (year // 4)
               + 30 * (month - 1)
               + day - 1)
        return jdn

    # ---- JDN → Ethiopian ----
    @staticmethod
    def _jdn_to_eth(jdn):
        r = (jdn - EthiopianDate.ETHIOPIAN_EPOCH) % 1461
        n = (r % 365) + 365 * (r // 1460)
        year = 4 * ((jdn - EthiopianDate.ETHIOPIAN_EPOCH) // 1461) + (r // 365) - (r // 1460)
        month = n // 30 + 1
        day = (n % 30) + 1
        return year + 1, month, day

    # ---- Gregorian → JDN ----
    @staticmethod
    def _gregorian_to_jdn(year, month, day):
        a = (14 - month) // 12
        y = year + 4800 - a
        m = month + 12 * a - 3
        jdn = day + ((153 * m + 2) // 5) + 365 * y
        jdn += y // 4 - y // 100 + y // 400 - 32045
        return jdn

    # ---- JDN → Gregorian ----
    @staticmethod
    def _jdn_to_gregorian(jdn):
        j = jdn + 32044
        g = j // 146097
        dg = j % 146097
        c = ((dg // 36524) + 1) * 3 // 4
        dc = dg - c * 36524
        b = dc // 1461
        db = dc % 1461
        a = ((db // 365) + 1) * 3 // 4
        da = db - a * 365
        y = g * 400 + c * 100 + b * 4 + a
        m = (da * 5 + 308) // 153 - 2
        d = da - (m + 4) * 153 // 5 + 122
        year = y - 4800 + (m + 2) // 12
        month = (m + 2) % 12 + 1
        day = d + 1
        return year, month, day

    # ---- Public methods ----
    def to_gregorian(self):
        jdn = self._eth_to_jdn(self.year, self.month, self.day)
        return self._jdn_to_gregorian(jdn)

    @classmethod
    def from_gregorian(cls, year, month, day):
        jdn = cls._gregorian_to_jdn(year, month, day)
        eth_year, eth_month, eth_day = cls._jdn_to_eth(jdn)
        return cls(eth_year, eth_month, eth_day)

    @classmethod
    def today(cls):
        today = date.today()
        return cls.from_gregorian(today.year, today.month, today.day)

    def add_days(self, days: int):
        jdn = self._eth_to_jdn(self.year, self.month, self.day)
        jdn += days
        year, month, day = self._jdn_to_eth(jdn)
        return EthiopianDate(year, month, day)
