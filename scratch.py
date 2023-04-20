def div(n):
    result = 10 / n
    return result


# test_div.py

import unittest


class TestDiv(unittest.TestCase):
    def test_div_by_two(self):
        res = div(2)
        self.assertEqual(res, 5)
        self.assertNotIn(res, [1, 2, 3, 4, 6])

    def test_div_by_five(self):
        res = div(5)
        self.assertEqual(res, 2)
        self.assertNotIn(res, [1, 3, 4, 6])


if __name__ == "__main__":
    unittest.main()
