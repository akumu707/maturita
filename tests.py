import unittest

from Parser import Parser
from Classes import *
import sys
from io import StringIO
#"BLOCK main {READ x; x:= x+6; DO [x > x - 2] other; GIVE x} BLOCK other {y := 9*x + 56; GIVE y} BLOCK otter {DO [x + 3 < 5 *4] other}"


class ParserTests(unittest.TestCase):
    def test_sum_tuple(self):
        self.assertEqual(sum((2, 2, 2)), 6, "Should be 6")

    #Program tests

    def test_program_return(self):
        parser = Parser()
        parsed = parser.parse("")

        self.assertTrue(type(parsed) == Program)

    def test_program_parts(self):
        parser = Parser()
        parsed = parser.parse("")

        self.assertTrue(type(parsed.parts) is dict)

    #BLOCK tests:

    def test_block_params(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK main {}")

        self.assertTrue("Unexpected char" in str(exc.exception))

    def test_block_name(self):
        parser = Parser()
        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK [] {}")

        self.assertTrue("Unexpected char" in str(exc.exception))

    def test_block_return(self):
        parser = Parser()
        parsed = parser.parse("BLOCK main [] {}")

        self.assertEqual(len(parsed.parts), 1, "Should be 1")

    def test_block_return_name(self):
        parser = Parser()
        parsed = parser.parse("BLOCK main [] {}")

        self.assertTrue("main" in parsed.parts)

    def test_block_return_type(self):
        parser = Parser()
        parsed = parser.parse("BLOCK main [] {}")

        self.assertTrue(type(parsed.parts["main"]) is Block)

    # WRITE tests

    def test_write_return_type(self):
        parser = Parser()
        parser.set_tokens("WRITE x")
        parsed = parser._command()

        self.assertTrue(type(parsed) is Command)

    def test_write_params(self):
        parser = Parser()
        parser.set_tokens("WRITE ")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()


        self.assertTrue("Expected" in str(exc.exception))

    def test_write_type(self):
        parser = Parser()
        parser.set_tokens("WRITE x")

        parsed = parser._command()

        self.assertTrue(parsed.type is CommandT.Print)

    # READ tests

    def test_read_return_type(self):
        parser = Parser()
        parser.set_tokens("READ x")
        parsed = parser._command()

        self.assertTrue(type(parsed) is Command)

    def test_read_params(self):
        parser = Parser()
        parser.set_tokens("READ WRITE x")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Expected" in str(exc.exception))

    def test_read_type(self):
        parser = Parser()
        parser.set_tokens("READ x")

        parsed = parser._command()

        self.assertTrue(parsed.type is CommandT.Read)

    #DO tests
    def test_do_return_type(self):
        parser = Parser()
        parser.set_tokens("DO x []")
        parsed = parser._command()

        self.assertTrue(type(parsed) is Command)

    def test_do_type(self):
        parser = Parser()
        parser.set_tokens("DO x []")

        parsed = parser._command()

        self.assertTrue(parsed.type is CommandT.Do)

    def test_do_params(self):
        parser = Parser()
        parser.set_tokens("DO x")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Out" in str(exc.exception))

    def test_do_name_param(self):
        parser = Parser()
        parser.set_tokens("DO []")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Expected" in str(exc.exception))

    #IF tests
    def test_if_return_type(self):
        parser = Parser()
        parser.set_tokens("IF x {}")
        parsed = parser._command()

        self.assertTrue(type(parsed) is Command)

    def test_if_type(self):
        parser = Parser()
        parser.set_tokens("IF x {}")

        parsed = parser._command()

        self.assertTrue(parsed.type is CommandT.If)

    def test_if_block_type(self):
        parser = Parser()
        parser.set_tokens("IF x {}")

        parsed = parser._command()

        self.assertTrue(type(parsed.right) is list)

    def test_if_block_command(self):
        parser = Parser()
        parser.set_tokens("IF x {WRITE x}")

        parsed = parser._command()

        self.assertTrue(len(parsed.right) == 1 and type(parsed.right[0]) is Command)

    def test_if_bool_param(self):
        parser = Parser()
        parser.set_tokens("IF {}")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Expected value type, got LCOMPPAREN instead" in str(exc.exception))

    def test_if_block_param(self):
        parser = Parser()
        parser.set_tokens("IF x")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Out" in str(exc.exception))

    # ASSIGN tests
    def test_assign_return_type(self):
        parser = Parser()
        parser.set_tokens("x: x+1")
        parsed = parser._command()

        self.assertTrue(type(parsed) is Command)

    def test_assign_params(self):
        parser = Parser()
        parser.set_tokens("x:")

        with self.assertRaises(Exception) as exc:
            parsed = parser._command()

        self.assertTrue("Expected expression" in str(exc.exception))

    def test_assign_type(self):
        parser = Parser()
        parser.set_tokens("x: x+1")

        parsed = parser._command()

        self.assertTrue(parsed.type is CommandT.Assign)


    def test_unexpected_close_paren(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK main [] {x : 2*(x+)
WRITE x DO hi []}
BLOCK hi [] {x:1WRITE x}
        """)

        self.assertTrue("Expected value " in str(exc.exception))

    def test_blocks_with_params(self):
        parser = Parser()
        parsed = parser.parse("""BLOCK main [] {
        DO hi [5]}
        BLOCK hi [x] {WRITE x}
                """)
        capturedOutput = StringIO()  # Make StringIO.
        sys.stdout = capturedOutput  # Redirect stdout.
        parsed.eval()  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(int(capturedOutput.getvalue()), 5, "Should be 5")

    def test_blocks_with_var_params(self):
        parser = Parser()
        parsed = parser.parse("""BLOCK main [] {
        x : 2
        DO hi [x]}
        BLOCK hi [x] {WRITE x}
                """)

        capturedOutput = StringIO()  # Make StringIO.
        sys.stdout = capturedOutput  # Redirect stdout.
        parsed.eval()  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.
        self.assertEqual(int(capturedOutput.getvalue()), 2, "Should be 2")



if __name__ == '__main__':
    unittest.main()