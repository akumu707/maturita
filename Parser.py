from Classes import *
from Lexer import Lexer
import ply.lex as lex

class Parser:

    def __init__(self):
        self.code = ""
        self.lexer = Lexer()
        self.lexer.build()
        self.tokens = []
        self.next_token = 0
        self.known_funcs = {}

    def _raise_exception(self, msg, token):
        if token is None:
            line_start = self.code.rfind('\n', 0, self.tokens[-1].lexpos) + 1
            raise Exception(f"{msg} on line: {self.tokens[-1].lineno}  char: "
                            f"{(self.tokens[-1].lexpos+len(str(self.tokens[-1].value)))+1 - line_start}")
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
            self._raise_exception(f"Out of bounds", None)
        if self.tokens[self.next_token].value == exp:
            self.next_token += 1
            return True
        self._raise_exception(f"Unexpected char {self.tokens[self.next_token].value}, expected {exp}",
                              self.tokens[self.next_token-1])

    def _get_next_token(self):
        current = self.tokens[self.next_token]
        self.next_token += 1
        return current

    def set_tokens(self, code):
        self.tokens = self.lexer.run(code)

    def parse(self, code):
        self.set_tokens(code)
        program = {}
        while self.next_token < len(self.tokens):
            if self._expect("BLOCK"):
                key = self._get_next_token().value
                params = self._params()
                self.known_funcs[key] = len(params)
                block = self._block()
                program[key] = Block(name=key, commands=block, params=params)
        return Program(program)

    def _block(self):
        result = []
        if self._expect("{"):
            while not self._accept("}"):
                result.append(self._command())
        return result

    def _cmd_block(self):
        result = []
        if self._expect("{"):
            while not self._accept("}"):
                result.append(self._command())
        return result

    def _command(self):
        if self._accept("WRITE"):
            return Command(CommandT.Print, self._bool_expression())
        if self._accept("READ"):
            param = self._object()
            if param is None:
                self._raise_exception(
                    f"Expected SimpleObject type, got {str(None)} "
                    f"instead", None)
            return Command(CommandT.Read, self._object())
        if self._accept("IF"):
            return Command(CommandT.If, l=self._bool_expression(), r=self._cmd_block())
        if self._accept("WHILE"):
            return Command(CommandT.While, l=self._bool_expression(), r=self._cmd_block())
        if self._accept("DO"):
            l = self._get_next_token().value
            if l not in self.known_funcs.keys():
                self._raise_exception(f"Unknown BLOCK {l}", self.tokens[self.next_token - 1])
            if l.isalpha() and not l.isupper():
                return Command(CommandT.Do, l=l, r=self._params())
            self._raise_exception(f"Expected BLOCK name, got {l} instead", self.tokens[self.next_token-1])
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
                    self._raise_exception(f"Expected expression", self.tokens[self.next_token-1])
                self._raise_exception(f"Expected value or expression after {op}", self.tokens[self.next_token-1])
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
                    return None
                self._raise_exception(f"Expected value or expression after {op}", self.tokens[self.next_token-1])
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
                    raise Exception("Missing string indicator")
                current+=str(self._get_next_token().value)
            return SimpleObj(BasicObjT.Str, current)
        current = self._get_next_token()
        if current.type == "NUMBER":
            return SimpleObj(BasicObjT.Int, current.value)
        if current.type == "TRUE":
            return SimpleObj(BasicObjT.Bool, True)
        if current.type == "FALSE":
            return SimpleObj(BasicObjT.Bool, False)
        if current.value.isalpha() and not current.value.isupper():
            return SimpleObj(BasicObjT.Var, current.value)
        self._raise_exception(f"Expected value type, got {current.type} instead", current)



if __name__ == '__main__':
    P = Parser()
    parsed = P.parse()
    print(parsed)
    print("-----------------")
    parsed.eval()