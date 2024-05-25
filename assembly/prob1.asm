.data:
    INT sum 0
    INT i 1000

.code:

while:
    LOAD i
    JZ hlt
    LOAD i
    MOD 3
    JZ add
    LOAD i
    MOD 5
    JZ add
    JMP inc

add:
    LOAD sum
    ADDM i
    SAVE sum

inc:
    LOAD i
    ADD -1
    SAVE i
    JMP while

hlt:
    LOAD sum
    OUT
    HLT