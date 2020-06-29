"""
Defines a small language that can be directly synthesized.
"""

from abc import ABC


class SynthExpr(ABC):
    pass


class Binop(SynthExpr):
    def __init__(self, op: str, left: SynthExpr, right: SynthExpr):
        self.left = left
        self.right = right
        self.op = op

    def pretty(self):
        return "(%s %s %s)" % (
            self.left.pretty(),
            self.op,
            self.right.pretty())


class RegRef(SynthExpr):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "RegRef(%s)" % self.name

    def pretty(self):
        return self.name


class Num(SynthExpr):
    def __init__(self, val: int):
        self.val = val

    def __str__(self):
        return "Num(%s)" % self.val

    def pretty(self):
        return str(self.val)


class Register:
    """Docstring for Register. """

    def __init__(self, name: str, width: int):
        """TODO: to be defined. """
        self.name = name
        self.width = width
