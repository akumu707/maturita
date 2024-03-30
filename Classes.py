from enum import Enum
from SimpleObjClasses import *
from CommandClasses import *


class OPchain:

    def __init__(self, chain):
        self.chain = chain

    def __str__(self):
        result = f""
        for var, op in self.chain:
            if op is None:
                result += f"{var}"
            else:
                result += f"{op}({var})"
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


class Block:
    def __init__(self, name, params, commands):
        self.name = name
        self.params = params
        self.commands = commands

    def __str__(self):
        result = f"BLOCK {self.name} ["
        for p in self.params:
            result += f"{p} "
        if self.params:
            result = result[:-1]
        result += "] {\n"
        for command in self.commands:
            result += f"\t{command}"
        return result + "}"

    def get_new_variable_map(self, param_values):
        var_map = {}
        for i in range(len(param_values)):
            var_map[self.params[i].value] = param_values[i]
        return var_map

    def eval(self, variable_map, index=-1):
        for i, command in enumerate(self.commands):
            if i <= index:
                continue
            result = command.eval(variable_map)
            if type(result) == dict:
                variable_map = result
            elif type(result) == tuple:
                param_values = []
                for param in result[1]:
                    param_values.append(param.eval(variable_map))
                return {"block": result[0], "param_values": param_values, "variable_map": variable_map,
                        "to stack": {"index": i, "name": self.name}}
            else:
                return


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
                    result["param_values"])
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
