.data:
    STR hello "Hello!"
    INT index 0

.code:
    PUSH hello
    SAVE index

print:
    LLOAD index
    JZ hlt
    OUT
    LOAD index
    ADD 1
    SAVE index
    JMP print

hlt:
    HLT
