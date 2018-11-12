//===- RISCVInstrInfoM.td - Multiply Divide RISCV instructions ----*- tblgen-*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//

//RV32
def MUL   : InstR<"mul"  , 0b0110011, 0b0000001, 0b000, mul   , GR32, GR32>, Requires<[IsRV32, HasM]>;
def MULH  : InstR<"mulh" , 0b0110011, 0b0000001, 0b001, mulhs , GR32, GR32>, Requires<[HasM]>;
//TODO: no corresponding llvm ir instruction
//def MULHSU: InstR<"mulh", 0b0110011, 0b0000001, 0b010, mulhs , GR32, GR32>, Requires<[HasM]>;
def MULHU : InstR<"mulhu", 0b0110011, 0b0000001, 0b011, mulhu , GR32, GR32>, Requires<[HasM]>;
def DIV   : InstR<"div"  , 0b0110011, 0b0000001, 0b100, sdiv  , GR32, GR32>, Requires<[IsRV32, HasM]>;
def DIVU  : InstR<"divu" , 0b0110011, 0b0000001, 0b101, udiv  , GR32, GR32>, Requires<[IsRV32, HasM]>;
def REM   : InstR<"rem"  , 0b0110011, 0b0000001, 0b110, srem  , GR32, GR32>, Requires<[IsRV32, HasM]>;
def REMU  : InstR<"remu" , 0b0110011, 0b0000001, 0b111, urem  , GR32, GR32>, Requires<[IsRV32, HasM]>;
