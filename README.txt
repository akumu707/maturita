EBNF syntax:
program = {block}, main_block, {block};

main_block = "BLOCK main", "[", var, { var },"]", "{", command, {command}, "}";

block = "BLOCK", var, "[", var, { var },"]", "{", command, {command}, "}";

command = "WRITE", bool_expr|"READ", var|var, ":", bool_expr| "DO", var, "[", { var }, "]"| "IF", bool_expr, "{", {command}, "}"| "WHILE", bool_expr, "{", {command}, "}";

bool_expr = expr, { ( '>' | '<'| '=') , expr };

expr = term, { ( '+' | '-' ) , term };

term = { factor, ( '*' | '/' ) }, factor;

factor = integer | '(', expr, ')'| string|bool|var;

integer = [ '-' ], digit, { digit };

digit = '0' | '1' | '...' | '9';

bool =  TRUE|FALSE;

string =  '"', letter, { letter }, '"';

var = letter, { letter };

string_char = 'A' | 'B' | '...' | 'Z'| digit | letter;

letter = 'a' | 'b' | '...' | 'z';
