﻿# Custom programing language interpret
## EBNF syntax:  
program = {block}, main_block, {block};

main_block = "BLOCK main", "[","]", command_block;

block = "BLOCK", var, "[", var, { var },"]", command_block;

command = "WRITE", bool_expr|"READ", var|var, ":", bool_expr| "DO", var, "[", { var }, "]"| "IF", bool_expr, command_block,{"ELIF", bool_expr, command_block}, ["ELSE",command_block]| "WHILE", bool_expr, command_block| "RETURN";

command_block = "{", {command}, "}";

bool_expr = expr, { ( '>' | '<'| '=') , expr };

expr = term, { ( '+' | '-' ) , term };

term = { factor, ( '*' | '/' ) }, factor;

factor = integer | '(', expr, ')'| string|bool|var;

integer = [ '-' ], digit, { digit };

digit = '0' | '1' | '...' | '9';

bool =  TRUE|FALSE;

string =  '"', string_char, { string_char }, '"';

var = letter, { letter|digit|_ };

string_char = 'A' | 'B' | '...' | 'Z'| digit | letter|" ";

letter = 'a' | 'b' | '...' | 'z'; 

![EBNF syntax](ebnf.png)
  
## Use examples:  

### "Hello world!" print 
	BLOCK main [] {
		WRITE "Hello world!"
	}  
### Arithmetics and boolean expression, if command
	BLOCK main [] {  
	    a : 10  
	    b : 20  
	    WRITE (a + b) * 2  
  
	    IF a > b {  
	        WRITE "a is greater than b"  
	    } ELSE {  
	        WRITE "a is less than or equal to b"  
	    }  
	}                                         
### String manipulation
	BLOCK main [] {  
	    str : "Hello, "  
	    WRITE str + "world!"  
	}  
###  While cycle, input
	BLOCK main [] {   
	    READ y
	    WHILE y > 0 {  
	        WRITE y  
	        y : y - 1  
	    }  
	}
### Recursion
	BLOCK recur [x]{  
		IF x>0 {  
			WRITE x  
			DO recur [x-1]}}  
	BLOCK main []{  
		DO recur [10]}
