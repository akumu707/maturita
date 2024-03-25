import unittest

from Parser import Parser
from Classes import *
import sys
from io import StringIO


class ParserTests(unittest.TestCase):

    def assert_program_output(self, program, expected, line=None):
        parser = Parser()
        parsed = parser.parse(program)
        self.string_output_test(parsed, expected, line)

    def assert_token_output(self, token_line, expected, line=None):
        parser = Parser()
        parser.set_tokens(token_line)
        parsed = parser._command()
        self.string_output_test(parsed, expected, line, {})

    def string_output_test(self, parsed, expected, line, params=None):
        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output
        if params is not None:
            parsed.eval(params)
        else:
            parsed.eval()
        sys.stdout = old_stdout
        self.assertEqual(captured_output.getvalue(), expected, line)

    # Program tests

    def test_program_return(self):
        parser = Parser()
        parsed = parser.parse("")

        self.assertTrue(type(parsed) == Program)

    def test_program_parts(self):
        parser = Parser()
        parsed = parser.parse("")

        self.assertTrue(type(parsed.parts) is dict)

    # BLOCK tests:

    def test_block_params(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK main {}")

        self.assertTrue("Unexpected char {, expected [ on line: 1 char: 11" in str(exc.exception))

    def test_block_name(self):
        parser = Parser()
        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK [] {}")

        self.assertTrue("Expected value type, got [ instead on line: 1 char: 6" in str(exc.exception))

    def test_block_return(self):
        parser = Parser()
        parsed = parser.parse("BLOCK main [] {}")

        self.assertEqual(len(parsed.parts), 1, "Program should contain one BLOCK")

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

        self.assertTrue(isinstance(parsed, CommandPrint))

    def test_write_params(self):
        parser = Parser()
        parser.set_tokens("WRITE ")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Out of bounds on line: 1 char: 5" in str(exc.exception))

    # READ tests

    def test_read_return_type(self):
        parser = Parser()
        parser.set_tokens("READ x")
        parsed = parser._command()

        self.assertTrue(isinstance(parsed, CommandRead))

    def test_read_params(self):
        parser = Parser()
        parser.set_tokens("READ WRITE x")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Expected value type, got WRITE instead on line: 1 char: 5" in str(exc.exception))

    # DO tests
    def test_do_return_type(self):
        parser = Parser()
        parsed = parser.parse("BLOCK x [] {DO x []}")

        self.assertTrue(isinstance(parsed.parts["x"].commands[0], CommandDo))

    def test_do_params(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK x [] {DO x}")

        self.assertTrue("Unexpected char }, expected [ on line: 1 char: 16" in str(exc.exception))

    def test_do_name_param(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("BLOCK x [] {DO []}")

        self.assertTrue("Expected BLOCK name, got [ instead on line: 1 char: 15" in str(exc.exception))

    def test_do_func_doesnt_exist(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK main []{DO hi []}""")

        self.assertTrue("Unknown BLOCK hi on line: 1 char: 17" in str(exc.exception))

    def test_do_func_diff_param_count(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK hi []{DO hi [x]}
                    """)

        self.assertTrue("Expected 0 commands, got 1 instead on line: 1 char: 20" in str(exc.exception))

    # IF tests
    def test_if_return_type(self):
        parser = Parser()
        parser.set_tokens("IF x {}")
        parsed = parser._command()

        self.assertTrue(isinstance(parsed, CommandIf))

    def test_if_block_type(self):
        parser = Parser()
        parser.set_tokens("IF x {}")

        parsed = parser._command()

        self.assertTrue(type(parsed.right) is list)

    def test_if_block_command(self):
        parser = Parser()
        parser.set_tokens("IF x {WRITE x}")

        parsed = parser._command()

        self.assertTrue(len(parsed.right) == 1 and isinstance(parsed.right[0], CommandPrint))

    def test_if_bool_param(self):
        parser = Parser()
        parser.set_tokens("IF {}")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Expected value type, got { instead on line: 1 char: 3" in str(exc.exception))

    def test_if_block_param(self):
        parser = Parser()
        parser.set_tokens("IF x")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Out of bounds on line: 1 char: 4" in str(exc.exception))

    # WHILE tests
    def test_while_return_type(self):
        parser = Parser()
        parser.set_tokens("WHILE x {}")
        parsed = parser._command()

        self.assertTrue(isinstance(parsed, CommandWhile))

    def test_while_block_type(self):
        parser = Parser()
        parser.set_tokens("WHILE x {}")

        parsed = parser._command()

        self.assertTrue(type(parsed.right) is list)

    def test_while_block_command(self):
        parser = Parser()
        parser.set_tokens("WHILE x {WRITE x}")

        parsed = parser._command()

        self.assertTrue(len(parsed.right) == 1 and isinstance(parsed.right[0], CommandPrint))

    def test_while_bool_param(self):
        parser = Parser()
        parser.set_tokens("WHILE {}")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Expected value type, got { instead on line: 1 char: 6" in str(exc.exception))

    def test_while_block_param(self):
        parser = Parser()
        parser.set_tokens("WHILE x")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Out of bounds on line: 1 char: 7" in str(exc.exception))

    # ASSIGN tests
    def test_assign_return_type(self):
        parser = Parser()
        parser.set_tokens("x: x+1")
        parsed = parser._command()

        self.assertTrue(isinstance(parsed, CommandAssign))

    def test_assign_params(self):
        parser = Parser()
        parser.set_tokens("x:")

        with self.assertRaises(Exception) as exc:
            parser._command()

        self.assertTrue("Out of bounds on line: 1 char: 2" in str(exc.exception))

    # Runtime tests
    def test_unexpected_close_paren(self):
        parser = Parser()

        with self.assertRaises(Exception) as exc:
            parser.parse("""BLOCK main [] {x : 2*(x+)
WRITE x DO hi []}
BLOCK hi [] {x:1WRITE x}
        """)

        self.assertTrue("Expected value type, got ) instead on line: 1 char: 24" in str(exc.exception))

    def test_blocks_with_params(self):
        self.assert_program_output("""BLOCK hi [x] {WRITE x}
        BLOCK main [] {
        DO hi [5]}
                """, "5\n", "Parameters transfer incorrect")

    def test_blocks_with_var_params(self):
        self.assert_program_output("""BLOCK hi [x] {WRITE x}
        BLOCK main [] {
        x : 2
        DO hi [x]}
                """, "2\n", "Variable evaluation while transfering params incorrect")

    def test_while_output(self):
        self.assert_program_output("""BLOCK main []{x: 3
        WHILE x<5 {WRITE 5 x: x+1}}
                """, "5\n5\n", "WHILE command not working properly")

    def test_while_variable_consistency(self):
        parser = Parser()
        parsed = parser.parse("""BLOCK main []{x: 3
                            WHILE x<5 {WRITE 5 x: x+1 y: 1} WRITE y}
                                    """)

        with self.assertRaises(Exception) as exc:
            parsed.eval()

        self.assertTrue("Variable y not assigned" in str(exc.exception))

    def test_return_after_do(self):
        self.assert_program_output("""
        BLOCK fn []{
        WRITE 5}
        BLOCK main []{
        x: 3
        DO fn []
        WRITE x
        }
        """, "5\n3\n", "BLOCK doesn't return after DO")

    def test_write_output(self):
        self.assert_program_output("""BLOCK main []{x: 3
                            WRITE x}""", "3\n", "Incorrect WRITE output")

    def test_assign_output(self):
        parser = Parser()
        parser.set_tokens("x: 2")
        parsed = parser._command()
        var_map = parsed.eval({})
        self.assertEqual(var_map["x"], 2, "Incorrect assign")

    def test_if_output(self):
        self.assert_token_output("IF TRUE{WRITE 2}", "2\n", "IF command not working properly")

    def test_expression_output(self):
        self.assert_token_output("WRITE 2+5*(6-3)", "17\n",
                                      "Expression evaluated incorrectly, possibly failure with parenthees")

    def test_write_bool_output(self):
        self.assert_token_output("WRITE TRUE", "TRUE\n", "Print output incorrect")

    def test_negative_number(self):
        self.assert_token_output("WRITE -5", "-5\n", "Parsing of negative number failed")

    def test_recursion(self):
        self.assert_program_output("""BLOCK recur [x]{
IF x>0 {
WRITE x
DO recur [x-1]}}
BLOCK main []{
DO recur [10]}""", "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\n", "Recursion doesn't recursion")

    def test_empty_if(self):
        self.assert_program_output("""
        BLOCK main []{
        x: TRUE IF x{}WRITE x}""", "TRUE\n", "Having no commands for if block doesn't work")

    def test_hello_world(self):
        self.assert_program_output("""BLOCK main []{WRITE \"Hello world!\"}""",
                                        "Hello world!\n", "Having no commands for if block doesn't work")

    def test_return(self):
        self.assert_program_output("""BLOCK main [] {
        a: 21
        IF a > 20 {
            WRITE "a is greater than b"
            RETURN}
        WRITE "a is less than or equal to b"}""","a is greater than b\n")

    def test_params_with_numbers(self):
        self.assert_program_output("""BLOCK fib_inner[pre2 pre1 i n] {
    IF i = n {
        WRITE pre1
        RETURN
    }
    DO fib_inner [pre1 pre2 + pre1 i + 1 n]
}

BLOCK fib [n]{
    IF n=1 {
        WRITE "0"
        RETURN
    } ELSE {
        IF n=2 {
            WRITE "1"
            RETURN
        } ELSE {
            DO fib_inner[0 1 2 n]
        }
    }
}

BLOCK main [] {
        DO fib[10]}""", "34\n")

    def test_elif(self):
        self.assert_program_output("""BLOCK fib_inner[pre2 pre1 i n] {
    IF i = n {
        WRITE pre1
        RETURN
    }
    DO fib_inner[pre1 pre2 + pre1 i + 1 n]
}

BLOCK fib [n]{
    IF n=1 {
        WRITE 0
        RETURN
    } ELIF n=2 {
        WRITE 1
        RETURN
    } ELSE {
        DO fib_inner[0 1 2 n]
    }
}

BLOCK main [] {
        DO fib[10]
}""", "34\n")


if __name__ == '__main__':
    unittest.main()
