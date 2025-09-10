import unittest
from core.ethiopian_date import EthiopianDate

class TestEthiopianDate(unittest.TestCase):
    def test_conversion(self):
        eth = EthiopianDate(2016, 1, 1)  # 1 Meskerem 2016
        greg = eth.to_gregorian()
        self.assertEqual(greg, (2023, 9, 11))

    def test_from_gregorian(self):
        eth = EthiopianDate.from_gregorian(2023, 9, 11)
        self.assertEqual((eth.year, eth.month, eth.day), (2016, 1, 1))

    def test_today(self):
        today_eth = EthiopianDate.today()
        self.assertIsInstance(today_eth, EthiopianDate)

if __name__ == "__main__":
    unittest.main()
