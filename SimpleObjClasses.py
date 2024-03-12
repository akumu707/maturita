class SimpleObjInt:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def eval(self, variable_map):
        return int(self.value)


class SimpleObjVar:

    def __init__(self,  value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def eval(self, variable_map):
        if self.value in variable_map.keys():
            return variable_map[self.value]
        raise Exception("Variable " + self.value + " not assigned")


class SimpleObjBool:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "TRUE" if self.value else "FALSE"

    def eval(self, variable_map):
        return self.value


class SimpleObjStr:

    def __init__(self, t, value):
        self.value = value

    def __str__(self):
        return f"\"{self.value}\""

    def eval(self, variable_map):
        return self.value


