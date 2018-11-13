// fpga4student.com 
// FPGA projects, VHDL projects, Verilog projects
// Verilog code for RISC Processor 
// Verilog code for ALU
module ALU( input  [15:0] a, input  [15:0] b, input  [2:0] alu_control, 
  output reg [15:0] result, output zero);
always @(*)
begin
 case(alu_control)
   3'b000: result = a + b;
   3'b001: result = a - b;
   default:result = a + b; 
   endcase
end
assign zero = (result==16'd0) ? 1'b1: 1'b0;
endmodule