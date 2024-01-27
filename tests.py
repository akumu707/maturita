import unittest

from Parser import Parser


class ParserTests(unittest.TestCase):
    def test_sum_tuple(self):
        self.assertEqual(sum((2, 2, 2)), 6, "Should be 6")

    def test_block_params(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK main {x : 2*(x+)}
            """)

        self.assertTrue("Unexpected char" in str(exc.exception))

    def test_do_params(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK main [] {DO main}")

        self.assertTrue("Unexpected char" in str(exc.exception))

    def test_unexpected_close_paren(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK main [] {x : 2*(x+)
WRITE x DO hi []}
BLOCK hi [] {x:1WRITE x}
        """)

        self.assertTrue("Expected value or expression after +" in str(exc.exception))


if __name__ == '__main__':
    unittest.main()