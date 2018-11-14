`ifndef PARAMETER_H_
`define PARAMETER_H_
// fpga4student.com 
// FPGA projects, VHDL projects, Verilog projects 
// Verilog code for RISC Processor 
// Parameter file
`define col 16 // 16 bits instruction memory, data memory
`define row_i 10 // instruction memory, instructions number, this number can be changed. Adding more instructions to verify your design is a good idea.
`define row_d 8 // The number of data in data memory. We only use 8 data. Do not change this number. You can change the value of each data inside test.data file. Total number is fixed at 8. 
`define filename "./50001111_50001212.o"
`define colprog 8
`define simulation_time #200
`define regdest_size 2
`define regdest_init 2
`define regdest_fin 2
`define regread1_size 2
`define regread1_init 2
`define regread1_fin 2
`define regread2_size 2
`define regread2_init 2
`define regread2_fin 2

`endif