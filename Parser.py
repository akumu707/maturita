from Classes import *
from Lexer import Lexer
import ply.lex as lex

class Parser:

    def __init__(self, code_file):
        self.code = ""
        with open(code_file) as file:
            for line in file:
                self.code += line
        self.lexer = Lexer()
        self.lexer.build()
        self.tokens = self.lexer.run(self.code)
        self.next_token = 0

    def _raise_exception(self, msg, token):
        line_start = self.code.rfind('\n', 0, token.lexpos) + 1
        raise Exception(f"{msg} on line: {token.lineno}  char: {token.lexpos - line_start}")

    def _accept(self, acc):
        if self.next_token >= len(self.tokens):
            return False
        if self.tokens[self.next_token].value == acc:
            self.next_token += 1
            return True
        return False

    def _expect(self, exp):
        if self.next_token >= len(self.tokens):
            return False
        if self.tokens[self.next_token].value == exp:
            self.next_token += 1
            return True
        self._raise_exception(f"Unexpected char {self.tokens[self.next_token].value}, expected {exp}",
                              self.tokens[self.next_token-1])

    def _get_next_token(self):
        current = self.tokens[self.next_token]
        self.next_token += 1
        return current

    def parse(self):
        program = {}
        while self.next_token < len(self.tokens):
            if self._expect("BLOCK"):
                key = self._get_next_token().value
                block = self._block()
                program[key] = Block(name=key, commands = block)
        return Program(program)

    def _block(self):
        result = []
        if self._expect("{"):
            while not self._accept("}"):
                result.append(self._command())
        return result

    def _command(self):
        if self._accept("WRITE"):
            return Command(CommandT.Print, self._bool_expression())
        if self._accept("READ"):
            return Command(CommandT.Read, self._object())
        if self._accept("IF"):
            return Command(CommandT.If, l=self._bool_expression(), r=self._block())
        if self._accept("DO"):
            return Command(CommandT.Do, l=self._get_next_token().value, r=self._params())
        l = self._object()
        if self._expect(":"):
            r = self._bool_expression()
            return Command(CommandT.Assign, r, l)

    def _params(self):
        result = []
        if self._expect("["):
            while not self._accept("]"):
                result.append(self._object())
        return result

    def _bool_expression(self):
        l = self._expression()
        if self._accept(">"):
            r = self._bool_expression()
            if r is None:
                self._raise_exception(f"Expected value after >", self.tokens[self.next_token])
            return BinOP(">", l=l, r=r)
        if self._accept("<"):
            r = self._bool_expression()
            if r is None:
                self._raise_exception(f"Expected value after <", self.tokens[self.next_token])
            return BinOP("<", l=l, r=r)
        if self._accept("="):
            r = self._bool_expression()
            if r is None:
                self._raise_exception(f"Expected value after =", self.tokens[self.next_token])
            return BinOP("=", l=l, r=r)
        return l

    def _expression(self):
        result = []
        op = None
        while True:
            next_char = self._term()
            if next_char is None:
                if op is None:
                    self._raise_exception(f"Expected expression", self.tokens[self.next_token])
                self._raise_exception(f"Expected value after {op}", self.tokens[self.next_token])
            result.append((next_char, op))
            if self._accept("+"):
                op = "+"
            elif self._accept("-"):
                op = "-"
            else:
                if len(result) == 1:
                    return result[0][0]
                return OPchain(result)


    def _term(self):
        result = []
        op = None
        while True:
            next_char = self._object()
            if next_char is None:
                if op is None:
                    self._raise_exception(f"Expected expression", self.tokens[self.next_token])
                self._raise_exception(f"Expected value after {op}", self.tokens[self.next_token])
            result.append((next_char, op))
            if self._accept("/"):
                op = "/"
            elif self._accept("*"):
                op = "*"
            else:
                if len(result) == 1:
                    return result[0][0]
                return OPchain(result)

    def _object(self):
        if self._accept("("):
            exp = self._expression()
            if self._accept(")"):
                return exp
            self._raise_exception(f"Expected )", self.tokens[self.next_token])
        if self.next_token >= len(self.tokens):
            return None
        if self._accept("\""):
            current = ""
            while not self._accept("\""):
                if self.next_token >= len(self.tokens):
                    raise Exception("Missing string indiciator")
                current+=str(self._get_next_token().value)
            return SimpleObj(BasicObjT.Str, current)
        current = self._get_next_token()
        if current.type == "NUMBER":
            return SimpleObj(BasicObjT.Int, current.value)
        if current.type == "TRUE":
            return SimpleObj(BasicObjT.Bool, True)
        if current.type == "FALSE":
            return SimpleObj(BasicObjT.Bool, False)
        if current.value.isalpha():
            return SimpleObj(BasicObjT.Var, current.value)



P = Parser("test.txt")
parsed = P.parse()
print(parsed)
print("-----------------")
parsed.eval()