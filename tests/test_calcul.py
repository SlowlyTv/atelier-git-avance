import unittest
from src.calcul import addition

class TestAddition(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(addition(2, 3), 5)

    def test_negative(self):
        self.assertEqual(addition(-2, 3), 1)

if __name__ == '__main__':
    unittest.main()
