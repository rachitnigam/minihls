from enum import Enum
from functools import total_ordering

from .fsm_lang.parser import parse_fsm
from .fsm_lang.lower import fsm_to_rtl

@total_ordering
class Lang(Enum):
    RTL = 0
    FSM = 1
    FIL = 2
    IMP = 3

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @staticmethod
    def argparse(s):
        try:
            return Lang[s.upper()]
        except KeyError:
            return s

    def as_parser(self):
        """
        Return parser associated with this language.
        """
        if self == Lang.FSM:
            return parse_fsm
        else:
            raise ValueError("No parser for %s" % self)


    def lower_to(self, other):
        if self == Lang.FSM and other == Lang.RTL:
            return fsm_to_rtl
        else:
            raise ValueError("No function to lower %s to %s." % (self, other))
