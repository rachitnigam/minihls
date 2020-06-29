from abc import ABC
from typing import List, Dict
from ..common.synth_lang import SynthExpr, Register, RegRef


class NextState(ABC):
    """Abstract class that defines next states"""
    pass


class Done(NextState):
    """Docstring for DirectNext. """

    def pretty(self):
        return "done"


class DirectNext(NextState):
    """Docstring for DirectNext. """

    def __init__(self, state: int):
        """TODO: to be defined. """
        self.state = state

    def pretty(self):
        return "next(%s)" % self.state


class CondNext(NextState):
    """Docstring for CondNext. """

    def __init__(self, cond: RegRef, on_true: int, on_false: int):
        """TODO: to be defined. """
        self.cond = cond
        self.on_true = on_true
        self.on_false = on_false

    def pretty(self):
        return "next(%s, %s, %s)" % (
            self.cond.pretty(),
            self.on_true,
            self.on_false
        )


class Update:
    def __init__(self, register: RegRef, expr: SynthExpr):
        self.register = register
        self.expr = expr

    def pretty(self):
        return "%s <= %s;" % (self.register.pretty(), self.expr.pretty())


class Action:
    """Docstring for Action. """

    def __init__(self, updates: List[Update], next_state: NextState):
        self.updates = updates
        self.next_state = next_state

    def pretty(self):
        pretty_updates = map(lambda upd: upd.pretty(), self.updates)
        return "{ %s %s }" % (" ".join(pretty_updates), self.next_state.pretty())


class FSM:
    """Internal representation for an FSM."""

    def __init__(self,
                 start_state: int,
                 done_states: List[int],
                 actions: Dict[int, Action]):
        """TODO: to be defined. """
        self.start_state = start_state
        self.done_states = done_states
        self.actions = actions

    def pretty(self):
        pretty_actions = [
            "%s: %s" % (k, v.pretty()) for k, v in self.actions.items()
        ]
        pretty_done = [ str(st) for st in self.done_states ]
        return "(start = %s, done = [%s]) {\n%s\n}" % (
            self.start_state,
            ", ".join(pretty_done),
            "\n".join(pretty_actions)
        )
