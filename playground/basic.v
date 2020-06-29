/*[> Two input mux <]
module mux2 (in0, in1, sel, out);
	input in0, in1, sel;
	output out;
	wire s0, w0, w1;

	not (s0, sel); // Invert the sel signal.
	and (w0, s0, in0),
			(w1, sel, in1);
	or (out, w0, w1);

endmodule

module mux4 (in0, in1, in2, in3, sel, out);
	input in0, in1, in2, in3;
	input sel[1:0];
	output out;

	wire w0, w1;

	mux2
		m0 (.sel(sel[0]), .in0(in0), .in1(in1), .out(w0)),
		m1 (.sel(sel[0]), .in0(in2), .in1(in3), .out(w1)),
		m2 (.sel(sel[1]), .in0(w0), .in1(w1), .out(out));

endmodule*/

module main(
	input clk,
	output done
);

reg once_every_two_cycles;

wire [3:0] count_out;
counter c(
	.clk(clk),
	.enb(1'b1), // Counter is always enabled.
	.clr(1'b0), // Counter is never cleared.
	.count(count_out)
);

wire enable_seq, inp;
// Enable the load signal once ever 4 cycles.
assign enable_seq = count_out % 4'b0100 == 0;
assign inp = $urandom();
wire seq_out;
ParToSeq pseq(
	.clk(clk),
	.ld(enable_seq),
	.inp(inp[3:0]),
	.out(seq_out)
);

// Finish simulation after 8 clock cycles.
assign done = count_out == 4'b1000;

endmodule

module ParToSeq(
	input clk,
	input ld, /* Load new values */
	input [3:0] inp, /* Inputs. */
	output out
);

	reg [3:0] inp_copy; // Registers to save the values.
	wire [3:0] ns;

	assign ns = ld ? inp : {inp_copy[0], inp_copy[3:1]};

	always @ (posedge clk) begin
		inp_copy <= ns;
		$display("Load: %d, Values: %d%d%d%d",
			ld,
			inp_copy[3],
			inp_copy[2],
			inp_copy[1],
			inp_copy[0]
		);
	end

	assign out = inp_copy[0];

endmodule

module counter(
	input clk, enb, clr,
	output reg [3:0] count
);

always @(posedge clk) begin
	count <= clr ? 4'b0 : (enb ? count + 1 : count);
end

endmodule
