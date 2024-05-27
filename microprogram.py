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


opcode_to_mp = {
    Opcode.JMP: 2,
    Opcode.JZ: 3,
    Opcode.HLT: 4,
    Opcode.LOAD: 5,
    Opcode.SAVE: 7,
    Opcode.LLOAD: 9,
    Opcode.SSAVE: 12,
    Opcode.ADD: 15,
    Opcode.MOD: 16,
    Opcode.ADDM: 17,
    Opcode.PUSH: 19,
}

memory = [
    # 0 instr fetch
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.LATCH_INSTR],
    [MP.MUX_MPC_INSTR, MP.LATCH_MPC],
    # 2 Opcode.JMP
    [MP.MUX_MPC_ZERO, MP.LATCH_MPC, MP.MUX_PC_JMP, MP.LATCH_PC],
    # 3 Opcode.JZ
    [MP.MUX_MPC_ZERO, MP.LATCH_MPC, MP.MUX_PC_JZ, MP.LATCH_PC],
    # 4 Opcode.HLT
    [MP.HALT],
    # 5 Opcode.LOAD
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_INSTR, MP.LATCH_ADDR],
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_R_ZERO,
        MP.MUX_ALU_L_MEM,
        MP.ALU_ADD,
        MP.LATCH_ACC,
    ],
    # 7 Opcode.SAVE
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_INSTR, MP.LATCH_ADDR],
    [MP.MUX_MPC_ZERO, MP.LATCH_MPC, MP.MUX_PC_NEXT, MP.LATCH_PC, MP.WR],
    # 9 Opcode.LLOAD
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_INSTR, MP.LATCH_ADDR],
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_MEM, MP.LATCH_ADDR],
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_R_ZERO,
        MP.MUX_ALU_L_MEM,
        MP.ALU_ADD,
        MP.LATCH_ACC,
    ],
    # 12 Opcode.SSAVE
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_INSTR, MP.LATCH_ADDR],
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_MEM, MP.LATCH_ADDR],
    [MP.MUX_MPC_ZERO, MP.LATCH_MPC, MP.MUX_PC_NEXT, MP.LATCH_PC, MP.WR],
    # 15 Opcode.ADD
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_L_INSTR,
        MP.MUX_ALU_R_ACC,
        MP.ALU_ADD,
        MP.LATCH_ACC,
    ],
    # 16 Opcode.MOD
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_L_INSTR,
        MP.MUX_ALU_R_ACC,
        MP.ALU_MOD,
        MP.LATCH_ACC,
    ],
    # 17 Opcode.ADDM
    [MP.MUX_MPC_NEXT, MP.LATCH_MPC, MP.MUX_ADDR_INSTR, MP.LATCH_ADDR],
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_L_MEM,
        MP.MUX_ALU_R_ACC,
        MP.ALU_ADD,
        MP.LATCH_ACC,
    ],
    # 19 Opcode.PUSH
    [
        MP.MUX_MPC_ZERO,
        MP.LATCH_MPC,
        MP.MUX_PC_NEXT,
        MP.LATCH_PC,
        MP.MUX_ALU_L_INSTR,
        MP.MUX_ALU_R_ZERO,
        MP.ALU_ADD,
        MP.LATCH_ACC,
    ],
]
