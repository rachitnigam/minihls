# miniHLS: Dead simple high-level synthesis

miniHLS is a educational HLS compiler implemented in Python. It has two goals:
1. Simplicity: The compiler prioritizes design decisions that make implementing
   the tool and understanding the compiler simple.
2. Extensible: The compiler can be easily extended with optimization and analysis
   passes.

The generated code is guaranteed to run on Verilator.

### Usage

To compile programs from FSM to RTL, use:

      python3 -m minihls.main -i fsm -o rtl <file>

For example, for the example file `examples/input.fsm`, do:

      python3 -m minihls.main -i fsm -o rtl examples/input.fsm
