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
        assert isinstance(state, int), "state is not a an int: %s" % on_true
        self.state = state

    def pretty(self):
        return "next(%s)" % self.state


class CondNext(NextState):
    """Docstring for CondNext. """

    def __init__(self, cond: RegRef, on_true: int, on_false: int):
        """TODO: to be defined. """
        assert isinstance(cond, RegRef), "Condition is not RegRef %s" % cond
        assert isinstance(
            on_true, int), "on_true is not a an int: %s" % on_true
        assert isinstance(
            on_false, int), "on_true is not a an int: %s" % on_false

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
        assert isinstance(
            register, RegRef), "register is not a RegRef: %s" % register
        assert isinstance(
            expr, SynthExpr), "expr is not a SynthExpr: %s" % expr

        self.register = register
        self.expr = expr

    def pretty(self):
        return "%s <= %s;" % (self.register.pretty(), self.expr.pretty())


class Action:
    """Docstring for Action. """

    def __init__(self, updates: List[Update], next_state: NextState):
        assert isinstance(
            next_state, NextState), "next_state is not a NextState: %s" % next_state
        assert all(map(lambda upd: isinstance(upd, Update), updates)), \
            "updates contains something that is not an Update: %s" % ", ".join(
                updates)

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
        assert isinstance(
            start_state, int), "start_state is not an int: %s" % start_state
        assert all(map(lambda st: isinstance(st, int), done_states)), \
            "done_states contains something that is not an int: %s" % ", ".join(
                done_states)
        assert all(map(
            lambda kv: isinstance(kv[0], int) and isinstance(kv[1], Action),
            actions.items()
        )), "actions is malformed: %s" % actions

        self.start_state = start_state
        self.done_states = done_states
        self.actions = actions

    def pretty(self):
        pretty_actions = [
            "%s: %s" % (k, v.pretty()) for k, v in self.actions.items()
        ]
        pretty_done = [str(st) for st in self.done_states]
        return "(start = %s, done = [%s]) {\n%s\n}" % (
            self.start_state,
            ", ".join(pretty_done),
            "\n".join(pretty_actions)
        )
