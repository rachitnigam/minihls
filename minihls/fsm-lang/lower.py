import math

import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

from ..common.synth_lang import *
from .syntax import *
from .lexer import Lexer
from .parser import Parser

BINOP_MAP = {
    "+": vast.Plus,
    "-": vast.Minus,
    "mod": vast.Mod,
    "!=": vast.NotEq,
}


def lower_expr(expr: SynthExpr):
    if isinstance(expr, RegRef):
        return vast.Identifier(expr.name)
    elif isinstance(expr, Num):
        return vast.IntConst(expr.val)
    elif isinstance(expr, Binop):
        return BINOP_MAP[expr.op](
            lower_expr(expr.left),
            lower_expr(expr.right),
        )
    else:
        raise ValueError(
            "Malformed AST, expected expr: %s" % expr.pretty())


def lower_update(upd: Update):
    reg = upd.register.name
    return vast.NonblockingSubstitution(
        vast.Lvalue(vast.Identifier(reg)),
        vast.Rvalue(lower_expr(upd.expr))
    )


def lower_next(done_stage: vast.IntConst, ns: NextState):
    """
        done_stage is the index of the final stage which just
        holds the all the values in the register.
    """
    # The computation is finished; transition to the done stage.
    if isinstance(ns, Done):
        return vast.Rvalue(done_stage)
    elif isinstance(ns, DirectNext):
        return vast.Rvalue(vast.IntConst(ns.state))
    elif isinstance(ns, CondNext):
        return vast.Cond(
            vast.Rvalue(vast.Identifier(ns.cond.name)),
            vast.IntConst(ns.on_true),
            vast.IntConst(ns.on_false),
        )
    else:
        raise ValueError(
            "Malformed AST, expected next: %s" % ns.pretty())


def lower_action(
        fsm_reg: vast.Reg,
        done_stage: vast.IntConst,
        action: Action):
    body = [lower_update(upd) for upd in action.updates]

    # Statement to update the FSM register to next state.
    st_upd = vast.NonblockingSubstitution(
        vast.Lvalue(vast.Identifier(fsm_reg.name)),
        lower_next(done_stage, action.next_state),
    )
    return vast.Block(body + [st_upd])


def lower_fsm(fsm: FSM):
    assert fsm.start_state == 0, "Starting state is not 0"
    zero = vast.IntConst(0)
    all_registers = [
        Register("a", 8),
        Register("b", 8),
        Register("tmp", 8),
        Register("_cond", 1),
    ]
    register_defs = [
        vast.Reg(
            reg.name,
            vast.Width(vast.IntConst(reg.width - 1), zero) if
            reg.width - 1 != 0 else
            None
        ) for reg in all_registers
    ]

    ports = vast.Portlist([
        vast.Ioport(vast.Input('clk')),
        # XXX(rachit): AST can't represent `output reg done`
        # so assign to a local register and use a wire.
        vast.Ioport(vast.Output('done')),
    ])
    done_state = max(fsm.actions.keys()) + 1
    done_reg = vast.Reg('done_out')
    hook_up_done = vast.Assign(
        vast.Lvalue(vast.Identifier('done')),
        vast.Rvalue(vast.Identifier('done_out')),
    )

    # Register to store the FSM state.
    fsm_reg_size = int(math.ceil(math.log2(done_state))) + 1
    fsm_reg = vast.Reg(
        name="fsm_reg",
        width=vast.Width(vast.IntConst(fsm_reg_size - 1), zero)
    )

    # Define all the registers.
    reg_decl = register_defs + [fsm_reg]

    # Define the initial process
    inits = vast.Initial(vast.Block([
        vast.BlockingSubstitution(
            vast.Lvalue(vast.Identifier(reg.name)),
            vast.Rvalue(vast.IntConst(0)),
        ) for reg in reg_decl
    ]))

    # Default case, assigns to the done register.
    done = vast.IntConst(done_state)
    default_case = vast.Case(
        cond=None,
        statement=vast.Block([
            vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier(reg.name)),
                vast.Rvalue(vast.Identifier(reg.name)),
            ) for reg in reg_decl
        ] + [
            vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier('done_out')),
                vast.Rvalue(vast.IntConst(1))
            )
        ])
    )

    # Generate Case conditions for each transition.
    cases = [
        vast.Case(
            [vast.IntConst(cond_val)],
            lower_action(fsm_reg, done, action)
        ) for (cond_val, action) in fsm.actions.items()
    ]
    case_statement = vast.CaseStatement(
        comp=vast.Identifier(fsm_reg.name),
        caselist=cases + [default_case]
    )
    always_ff = vast.Always(
        vast.SensList([vast.Sens(vast.Identifier('clk'), 'posedge')]),
        vast.Block([case_statement])
    )

    return vast.ModuleDef(
        name="main",
        paramlist=vast.Paramlist([]),
        portlist=ports,
        items= reg_decl + [done_reg, hook_up_done, inits, always_ff]
    )


if __name__ == '__main__':
    text_input = """
(start = 0, done = [6]) {
  0: { a <= 4; b <= 12; next(1) }
  1: { _cond <= b != 0; next(2) }
  2: { next(_cond, 3, 6) }
  3: { tmp <= b; next(4) }
  4: { b <= a mod b; next(5) }
  5: { a <= tmp; next(1) }
  6: { b <= a; done }
}
    """
    lexer = Lexer().get_lexer()
    tokens = lexer.lex(text_input)

    pg = Parser()
    pg.parse()
    ast = pg.get_parser().parse(tokens)

    out = lower_fsm(ast)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(out)
    print(rslt)
