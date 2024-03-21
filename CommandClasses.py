class CommandT():
    Assign = 1
    Print = 2
    Read = 3
    Do = 4
    If = 5
    While = 6


class CommandAssign:

    def __init__(self, r, l):
        self.right = r
        self.left = l

    def __str__(self):
        return f"{self.left} : {self.right}\n"

    def eval(self, variable_map):
        for char in self.left.value:
            if not ord(char) >= ord("a") and ord(char) <= ord("z"):
                raise Exception("Variable name is not lowercase")
        variable_map[self.left.value] = self.right.eval(variable_map)
        return variable_map


class CommandPrint:

    def __init__(self, r):
        self.right = r

    def __str__(self):
        return f"WRITE {self.right}\n"

    def eval(self, variable_map):
        try:
            value = self.right.eval(variable_map)
            if value is True:
                value = "TRUE"
            if value is False:
                value = "FALSE"
            print(value)
        except:
            raise Exception(f"Trying to print unprintable object {self.right.eval(variable_map)}")
        return variable_map


class CommandRead:

    def __init__(self, r):
        self.right = r

    def __str__(self):
        return f"READ {self.right}\n"

    def eval(self, variable_map):
        result = input()
        if result.isdecimal():
            variable_map[self.right.value] = int(result)
            return variable_map
        raise Exception("Trying to assign string to a variable")


class CommandDo:

    def __init__(self, r, l):
        self.right = r
        self.left = l  # only useful for the jump command

    def __str__(self):
        result = f"DO {self.left} ["
        for p in self.right:
            result += f"{p}"
        result += "]"
        return result

    def eval(self, variable_map):
        return self.left, self.right


class CommandIf:

    def __init__(self, r, l, else_block=None):
        self.right = r
        self.left = l
        self.else_block = else_block

    def __str__(self):
        result = f"IF {self.left} " + "{\n"
        for command in self.right:
            result += f"\t{command}"
        result += "}\n"
        return result

    def eval(self, variable_map):
        if type(self.left.eval(variable_map)) == bool:
            if self.left.eval(variable_map):
                for command in self.right:
                    variable_map = command.eval(variable_map)
            else:
                if self.else_block:
                    for command in self.else_block:
                        variable_map = command.eval(variable_map)
            return variable_map
        else:
            raise Exception("IF first parameter is not a Bool expression")


class CommandWhile:

    def __init__(self, r, l):
        self.right = r
        self.left = l  # only useful for the jump command

    def __str__(self):
        result = f"WHILE {self.left} " + "{\n"
        for command in self.right:
            result += f"\t{command}"
        result += "}\n"
        return result

    def eval(self, variable_map):
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



