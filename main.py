import sys
from Parser import Parser

if __name__ == "__main__":
    code = ""
    with open(sys.argv[1]) as file:
        for line in file:
            code += line
    parser = Parser()
    parsed = parser.parse(code)
    parsed.eval()
