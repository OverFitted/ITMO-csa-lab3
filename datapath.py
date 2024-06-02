import logging

from microprogram import MP
from op import INP_PORT, OUT_PORT


class DataPath:
    def __init__(self, memory: list, input_buffer: list):
        self.memory = memory
        self.input_buffer = input_buffer
        self.output_buffer = []

        self.addr_reg = 0
        self.acc_reg = 0

        self.mux_addr = None
        self.mux_alu_left = None
        self.mux_alu_right = None

        self.alu_res = 0
        self.instr_arg = 0
        self.zero = False

    def latch_addr_reg(self, val=None):
        if self.mux_addr is MP.MUX_ADDR_ACC:
            self.addr_reg = self.acc_reg
        elif self.mux_addr is MP.MUX_ADDR_MEM:
            if self.addr_reg == INP_PORT:
                self.addr_reg = self._input()
            else:
                self.addr_reg = self.memory[self.addr_reg]["arg"]
        elif self.mux_addr is MP.MUX_ADDR_INSTR:
            self.addr_reg = val
        else:
            raise ValueError(f"Wrong mux: {self.mux_addr}")

    def latch_acc_reg(self):
        self.acc_reg = self.alu_res

    def sel_mux_addr(self, val: MP):
        self.mux_addr = val

    def sel_mux_alu_left(self, val: MP):
        self.mux_alu_left = val

    def sel_mux_alu_right(self, val: MP):
        self.mux_alu_right = val

    def alu(self, operation: MP, val: int = None):
        if self.mux_alu_right is MP.MUX_ALU_R_ACC:
            right = self.acc_reg
        elif self.mux_alu_right is MP.MUX_ALU_R_ZERO:
            right = 0
        else:
            raise ValueError(f"Wrong mux: {self.mux_alu_right}")

        if self.mux_alu_left is MP.MUX_ALU_L_INSTR:
            left = val
        elif self.mux_alu_left is MP.MUX_ALU_L_MEM:
            if self.addr_reg == INP_PORT:
                left = self._input()
            else:
                left = self.memory[self.addr_reg]["arg"]
        else:
            raise ValueError(f"Wrong mux: {self.mux_alu_left}")

        if operation == MP.ALU_ADD:
            self.alu_res = (right + left) % 2**31
        elif operation == MP.ALU_MOD:
            self.alu_res = (right % left) % 2**31

        self.acc_reg = self.alu_res
        self._set_zero()

    def wr(self):
        if self.addr_reg == OUT_PORT:
            self._output()
        else:
            self.memory[self.addr_reg]["arg"] = self.acc_reg

    def _input(self):
        symbol = self.input_buffer.pop(0)
        ord_sym = ord(symbol)
        if ord_sym == 0:
            symbol = ""
        logging.debug(f"input: {symbol}")
        return ord_sym

    def _output(self):
        symbol = self.acc_reg
        self.output_buffer.append(symbol)
        logging.debug(
            f"output: {''.join(map(lambda x: chr(x) if 0 < x < 256 else str(x), self.output_buffer))} << {symbol}"
        )

    def _set_zero(self):
        self.zero = self.acc_reg == 0

    def is_zero(self):
        return self.zero
