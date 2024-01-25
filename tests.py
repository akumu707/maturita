import unittest

from Parser import Parser


class ParserTests(unittest.TestCase):
    def test_sum_tuple(self):
        self.assertEqual(sum((2, 2, 2)), 6, "Should be 6")

    def test_unexpected_close_paren(self):
        with open("unexpected_close_paren_test.txt", mode="w") as file:
            file.writelines("""BLOCK main {x : 2*(x+)
WRITE x DO hi}
BLOCK hi {x:1WRITE x}
        """)
        parser = Parser("unexpected_close_paren_test.txt")

        with self.assertRaises(Exception) as exc:
            parser.parse()

        self.assertTrue("Expected value or expression after +" in str(exc.exception))


if __name__ == '__main__':
    unittest.main()