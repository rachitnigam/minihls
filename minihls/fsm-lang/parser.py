from rply import ParserGenerator
from .syntax import *
from ..common.synth_lang import *
from .lexer import TOKENS, Lexer


class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            TOKENS,
            precedence=[
                ('left', ['ADD', 'SUB']),
                ('left', ['MOD']),
                ('left', ['NOT_EQ']),
            ]
        )

    def parse(self):
        @self.pg.production('fsm : fsm_pre LBRACE fsm_rules RBRACE')
        def fsm(p) -> FSM:
            (start, dones) = p[0]
            rules = {k: v for (k, v) in p[2]}
            return FSM(start.val, [n.val for n in dones], rules)

        @self.pg.production('number : NUMBER')
        @self.pg.production('expr : number')
        def number(p) -> SynthExpr:
            if isinstance(p[0], Num):
                return p[0]
            return Num(int(p[0].value))

        @self.pg.production('id : ID')
        @self.pg.production('expr : id')
        def id(p) -> SynthExpr:
            if isinstance(p[0], RegRef):
                return p[0]
            return RegRef(p[0].value)

        @self.pg.production('expr : expr ADD expr')
        @self.pg.production('expr : expr SUB expr')
        @self.pg.production('expr : expr MOD expr')
        @self.pg.production('expr : expr NOT_EQ expr')
        def expr(p) -> SynthExpr:
            left = p[0]
            right = p[2]
            operator = p[1]
            return Binop(operator.value, left, right)

        @self.pg.production('number_rep : number COMMA number_rep')
        @self.pg.production('number_rep : number')
        def number_rep(p) -> List[SynthExpr]:
            if len(p) == 1:
                return [p[0]]
            else:
                return [p[0]] + [p[2]]

        @self.pg.production('next : NEXT LPAREN number RPAREN')
        def direct_next(p) -> NextState:
            return DirectNext(p[2].val)

        @self.pg.production('next : NEXT LPAREN id COMMA number COMMA number RPAREN')
        def cond_next(p) -> NextState:
            return CondNext(p[2], p[4].val, p[6].val)

        @self.pg.production('next : DONE')
        def done_next(p) -> NextState:
            return Done()

        @self.pg.production('update : id LEFT_ARROW expr')
        def update(p) -> Update:
            return Update(p[0], p[2])

        @self.pg.production('updates : update SEMI updates')
        @self.pg.production('updates : update SEMI')
        def updates(p) -> List[Update]:
            if len(p) == 2:
                return [p[0]]
            else:
                return [p[0]] + p[2]

        @self.pg.production('action : LBRACE updates next RBRACE')
        @self.pg.production('action : LBRACE next RBRACE')
        def action(p) -> Action:
            if len(p) == 3:
                return Action([], p[1])
            else:
                return Action(p[1], p[2])

        @self.pg.production('fsm_pre : LPAREN START EQUAL number COMMA DONE EQUAL LBRACKET number_rep RBRACKET RPAREN')
        def fsm_pre(p):
            return (p[3], p[8])

        @self.pg.production('fsm_rule : number COLON action')
        def fsm_rule(p):
            return (p[0].val, p[2])

        @self.pg.production('fsm_rules : fsm_rule fsm_rules')
        @self.pg.production('fsm_rules : fsm_rule')
        def fsm_rules(p):
            if len(p) == 1:
                return [p[0]]
            else:
                return [p[0]] + p[1]

        @self.pg.error
        def error_handle(token):
            pos = token.getsourcepos()
            raise ValueError(
                "Failed to parse `%s' on line %s, column %s." % (token.value, pos.lineno, pos.colno))

    def get_parser(self):
        return self.pg.build()

