module main (
  input logic clk,
  output logic done
);

  logic [3:0] curr_state;
  logic [3:0] i;

  initial begin
    i = 4'd0;
    curr_state = 4'd0;
    next_state = 4'd0;
  end

  always_ff @ (posedge clk) begin
    case (curr_state)
      4'd0 : begin
        i <= 4'd0;
        curr_state <= curr_state + 1;
      end
      4'd1 : begin
        i <= i + 1;
        curr_state <= curr_state + 1;
      end
      default : begin
        i <= i;
        curr_state <= curr_state;
      end
    endcase
    done <= (curr_state == 4'd2) ? 1'd1 : 1'd0;
  end

endmodule
