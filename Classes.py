from enum import Enum


class BasicObjT(Enum):
    Int = 1
    Var = 2
    Bool = 3
    Str = 4


class SimpleObj:

    def __init__(self, t, value):
        self.type = t
        self.value = value

    def __str__(self):
        if self.type == BasicObjT.Bool:
            return "TRUE" if self.value else "FALSE"
        if self.type == BasicObjT.Str:
            return f"\"{self.value}\""
        return str(self.value)

    def eval(self, variable_map):
        if self.type == BasicObjT.Int:
            return int(self.value)
        if self.type == BasicObjT.Bool or self.type == BasicObjT.Str:
            return self.value
        if self.value in variable_map.keys():
            return variable_map[self.value]
        raise Exception("Variable " + self.value + " not assigned")

class OPchain:

    def __init__(self, chain):
        self.chain = chain

    def __str__(self):
        result = f""
        for var, op in self.chain:
            if op is None:
                result+=f"{var}"
            else:
                result+=f"{op}({var})"
        return result

    def eval(self, variable_map):
        result = None
        for var, op in self.chain:
            value = var.eval(variable_map)
            if result is None:
                result = value
            else:
                if op == "+":
                    result += value
                if op == "-":
                    result -= value
                if op == "*":
                    result *= value
                if op == "/":
                    result /= value
        return result


class BinOP:

    def __init__(self, op, l, r):
        self.op = op
        self.left = l
        self.right = r

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def eval(self, variable_map):
        left = self.left.eval(variable_map)
        right = self.right.eval(variable_map)
        try:
            if self.op == "-":
                return left+(-right)
            if self.op == "+":
                return left+right
            if self.op == "/":
                return left*(1/right)
            if self.op == "*":
                return left*right
            if self.op == ">":
                return left > right
            if self.op == "<":
                return left < right
            if self.op == "=":
                return left == right
        except TypeError as tperror:
            raise Exception("Type Error: " + str(tperror))


class CommandT(Enum):
    Assign = 1
    Print = 2
    Read = 3
    Do = 4
    If = 5
    While = 6


class Command:

    def __init__(self, t, r, l=None):
        self.type = t
        self.right = r
        self.left = l  # only useful for the jump command

    def __str__(self):
        if self.type == CommandT.Assign:
            return f"{self.left} : {self.right}\n"
        if self.type == CommandT.Print:
            return f"WRITE {self.right}\n"
        if self.type == CommandT.Read:
            return f"READ {self.right}\n"
        if self.type == CommandT.Do:
            result = f"DO {self.left} ["
            for p in self.right:
                result += f"{p}"
            result += "]"
            return result
        if self.type == CommandT.If:
            result = f"IF {self.left} " + "{\n"
            for command in self.right:
                result += f"\t{command}"
            result +="}\n"
            return result
        if self.type == CommandT.While:
            result = f"WHILE {self.left} " + "{\n"
            for command in self.right:
                result += f"\t{command}"
            result +="}\n"
            return result

    def eval(self, variable_map):
        if self.type == CommandT.Assign:
            for char in self.left.value:
                if not ord(char) >= ord("a") and ord(char) <= ord("z"):
                    raise Exception("Variable name is not lowercase")
            variable_map[self.left.value] = self.right.eval(variable_map)
            return variable_map
        if self.type == CommandT.Print:
            if self.right.type == BasicObjT.Var:
                print(self.right.eval(variable_map))
            elif self.right.type == BasicObjT.Int:
                print(self.right.eval(variable_map))
            else:
                raise Exception("Trying to print unprintable object")
            return variable_map
        if self.type == CommandT.Read:
            result = input()
            if result.isdecimal():
                variable_map[self.right.value] = int(result)
                return variable_map
            raise Exception("Trying to assign string to a variable")
        if self.type == CommandT.Do:
            return self.left, self.right
        if self.type == CommandT.If:
            if type(self.left.eval(variable_map)) == bool:
                if self.left.eval(variable_map):
                    for command in self.right:
                        variable_map = command.eval(variable_map)
                return variable_map
            else:
                raise Exception("IF first parameter is not a Bool expression")
        if self.type == CommandT.While:
            if type(self.left.eval(variable_map)) == bool:
                prev_variable_map = variable_map.copy()
                while self.left.eval(variable_map):
                    for command in self.right:
                        variable_map = command.eval(variable_map)
                for key in prev_variable_map.keys():
                    prev_variable_map[key] = variable_map[key]
                return prev_variable_map
            else:
                raise Exception("WHILE first parameter is not a Bool expression")


class Block:
    def __init__(self, name, params, commands):
        self.name = name
        self.params = params
        self.commands = commands

    def __str__(self):
        result = f"BLOCK {self.name} ["
        for p in self.params:
            result += f"{p}"
        result+= "] {\n"
        for command in self.commands:
            result += f"\t{command}"
        return result + "}"

    def get_new_variable_map(self, param_values, variable_map):
        var_map = {}
        for i in range(len(param_values)):
            if param_values[i].type == BasicObjT.Var:
                var_map[self.params[i].value] = variable_map[param_values[i].value]
            else:
                var_map[self.params[i].value] = param_values[i]
        return var_map

    def eval(self, variable_map, index=-1):
        for i, command in enumerate(self.commands):
            if i <= index:
                continue
            result = command.eval(variable_map)
            if type(result) == dict:
                variable_map = result
            else:
                return {"block": result[0], "param_values": result[1], "variable_map": variable_map,
                        "to stack": {"index": i, "name": self.name}}


class Program:
    def __init__(self, parts):
        self.parts = parts
        # dictionary in the form {block_name : Block}

    def __str__(self):
        result = ""
        for part in self.parts.values():
            result += f"{part}\n"
        return result

    def next_block_handle(self, result, variable_map, stack):
        while result is not None:
            if result["block"] in self.parts:
                variable_map[result["block"]] = self.parts[result["block"]].get_new_variable_map(
                    result["param_values"], result["variable_map"])
                stack.append(result["to stack"])
                result = self.parts[result["block"]].eval(variable_map[result["block"]])
            else:
                raise Exception("No block named " + result["block"] + " in code")

    def eval(self):
        """Program should start to evaluate the 'main' block and run its commands.
        If there is no 'main' block, throw an error."""
        variable_map = {}
        if "main" in self.parts.keys():
            stack = []
            variable_map["main"] = {}
            result = self.parts["main"].eval(variable_map["main"])
            self.next_block_handle(result, variable_map, stack)
            while stack:
                block = stack.pop()
                result = self.parts[block["name"]].eval(variable_map[block["name"]], block["index"])
                self.next_block_handle(result, variable_map, stack)

        else:
            raise Exception("No 'main' block in code")
