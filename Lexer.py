import ply.lex as lex
reserved = {
        'BLOCK': 'BLOCK',
        'READ': 'READ',
        'WRITE': 'WRITE',
        "IF": "IF",
        "ELSE": "ELSE",
        "ELIF": "ELIF",
        "DO": "DO",
        "TRUE": "TRUE",
        "FALSE": "FALSE",
        "WHILE": "WHILE",
        "RETURN": "RETURN"
    }


class Lexer(object):

    # List of token names.   This is always required
    tokens = [
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'LCOMPPAREN',
        "RCOMPPAREN",
        "EQUAL",
        "HIGHER",
        "LOWER",
        "TEXT",
        "ASSIGN",
        "QUOMARK",
        'LSQPAREN',
        "RSQPAREN",
        "STRING",
        "COMMA"
    ] + list(reserved)

    states = (
        ('string', 'exclusive'),
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCOMPPAREN = r'\{'
    t_RCOMPPAREN = r'\}'
    t_HIGHER = r'\>'
    t_LOWER = r'\<'
    t_EQUAL = r'\='
    t_ASSIGN = r'\:'
    t_QUOMARK = r'"'
    t_LSQPAREN = r'\['
    t_RSQPAREN = r'\]'
    t_COMMA = r','

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_string(self, t):
        r'\"'
        t.lexer.code_start = t.lexer.lexpos  # Record the starting position
        t.lexer.begin('string')

    def t_string_quotation(self, t):
        r'\"'
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-1]
        t.type = "STRING"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        return t

    # Ignored characters (whitespace)
    t_string_ignore = "\t\n"

    # For bad characters, we just skip over it
    def t_string_error(self, t):
        t.lexer.skip(1)

    def t_TEXT(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'TEXT')  # Check for reserved words
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def run(self, data):
        self.lexer.input(data)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append(tok)
        return result


