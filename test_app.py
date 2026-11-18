from decimal import Decimal
import unittest
from app import convert


class ConverterTests(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertEqual(convert(0, "c", "f"), Decimal("32"))

    def test_fahrenheit_to_celsius(self):
        self.assertEqual(convert(212, "f", "c"), Decimal("100.00"))

    def test_kilometers(self):
        self.assertEqual(convert(1, "km", "m"), Decimal("1000"))

    def test_grams(self):
        self.assertEqual(convert(1, "kg", "g"), Decimal("1000"))

    def test_incompatible(self):
        with self.assertRaises(ValueError):
            convert(5, "kg", "km")

    def test_below_absolute_zero(self):
        with self.assertRaises(ValueError):
            convert(-300, "c", "k")


if __name__ == "__main__":
    unittest.main()
