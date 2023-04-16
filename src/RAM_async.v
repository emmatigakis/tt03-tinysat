//I copied this from https://8bitworkshop.com/
module RAM_async(clk, addr, din, dout, we);
  
  parameter A = 5; // # of address bits
  parameter D = 4;  // # of data bits
  
  input  clk;		// clock
  input  [A-1:0] addr;	// address
  input  [D-1:0] din;	// data input
  output [D-1:0] dout;	// data output
  input  we;		// write enable
  
  reg [D-1:0] mem [0:(1<<A)-1]; // (1<<A)xD bit memory
  
  always @(posedge clk) begin
    if (we)		// if write enabled
      mem[addr] <= din;	// write memory from din
  end

  assign dout = mem[addr]; // read memory to dout (async)

endmodule