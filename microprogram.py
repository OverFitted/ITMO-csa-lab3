from enum import Enum

from op import Opcode


class MP(Enum):
    MUX_ADDR_MEM = 0
    MUX_ADDR_ACC = 1
    MUX_ADDR_INSTR = 2

    MUX_ALU_L_INSTR = 10
    MUX_ALU_L_MEM = 11

    MUX_ALU_R_ACC = 15
    MUX_ALU_R_ZERO = 16

    MUX_PC_NEXT = 20
    MUX_PC_JMP = 21
    MUX_PC_JZ = 22

    MUX_MPC_NEXT = 30
    MUX_MPC_ZERO = 31
    MUX_MPC_INSTR = 32

    LATCH_ADDR = 40
    LATCH_ACC = 41
    LATCH_PC = 42
    LATCH_MPC = 43
    LATCH_INSTR = 44

    ALU_ADD = 50
    ALU_MOD = 51

    WR = 60
    OE = 61

    HALT = 70


