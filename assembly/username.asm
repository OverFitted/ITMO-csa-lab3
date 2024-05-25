.data:
    STR hello "Hello, "
    BUF username 30
    INT index 0

.code:
    PUSH hello
    SAVE index

print_hello:
    LLOAD index
    JZ after_print_hello
    OUT
    LOAD index
    ADD 1
    SAVE index
    JMP print_hello

after_print_hello:
    PUSH username
    SAVE index

read_name:
    INP
    JZ after_read_name
    SSAVE index
    LOAD index
    ADD 1
    SAVE index
    JMP read_name

after_read_name:
    PUSH username
    SAVE index

print_name:
    LLOAD index
    JZ hlt
    OUT
    LOAD index
    ADD 1
    SAVE index
    JMP print_name

hlt:
    HLT