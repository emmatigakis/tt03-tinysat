module mymux (
    input wire signed [3:0] lit,
    input wire [5:0] x,
    output reg c
);
localparam LOG2_NUM_CLAUSES = 5;
always @(*) begin
    case(lit)
      0: c = 1'b0;
      1: c = x[0];
      -1: c = !x[0];
      2: c = x[1];
      -2: c = !x[1];
      3: c = x[2];
      -3: c = !x[2];
      4: c = x[3];
      -4: c = !x[3];
      5: c = x[4];
      -5: c = !x[4];
      6: c = x[5];
      -6: c = !x[5];
      default: c = 1'b1;
    endcase
  end

endmodule

