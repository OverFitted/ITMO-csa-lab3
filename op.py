from enum import Enum

INP_PORT = 0
OUT_PORT = 1


class Opcode(Enum):
    JMP = "JMP"
    JZ = "JZ"
    HLT = "HLT"

    PUSH = "PUSH"
    LOAD = "LOAD"
    SAVE = "SAVE"
    LLOAD = "LLOAD"
    SSAVE = "SSAVE"

    ADD = "ADD"
    MOD = "MOD"
    ADDM = "ADDM"

    STR = "STR"
    INT = "INT"
    BUF = "BUF"

    # INP changed to LOAD
    # OUT changed to SAVE
