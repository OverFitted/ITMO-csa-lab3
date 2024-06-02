import microprogram
from datapath import DataPath
from microprogram import MP


class ControlUnit:
    def __init__(self, memory: list, microprogram: list, datapath: DataPath):
        self.memory = memory
        self.microprogram = microprogram
        self.datapath = datapath

        self.pc_reg = 0
        self.instr_reg = None
        self.mpc_reg = 0

        self.mux_pc = None
        self.mux_mpc = None

        self._tick = 0

    def tick(self):
        self._tick += 1

    def cur_tick(self):
        return self._tick

    def latch_pc_reg(self):
        if self.mux_pc is MP.MUX_PC_JZ:
            if self.datapath.is_zero():
                self.pc_reg = self.instr_reg["arg"]
            else:
                self.pc_reg += 1
        elif self.mux_pc is MP.MUX_PC_JMP:
            self.pc_reg = self.instr_reg["arg"]
        elif self.mux_pc is MP.MUX_PC_NEXT:
            self.pc_reg += 1
        else:
            raise ValueError(f"Wrong mux: {self.mux_pc}")

    def latch_instr_reg(self):
        self.instr_reg = self.memory[self.pc_reg]

    def latch_mpc_reg(self):
        if self.mux_mpc is MP.MUX_MPC_NEXT:
            self.mpc_reg += 1
        elif self.mux_mpc is MP.MUX_MPC_ZERO:
            self.mpc_reg = 0
        elif self.mux_mpc is MP.MUX_MPC_INSTR:
            self.mpc_reg = microprogram.opcode_to_mp[self.instr_reg["opcode"]]
        else:
            raise ValueError(f"Wrong mux: {self.mux_mpc}")

    def sel_mux_pc(self, val: MP):
        self.mux_pc = val

    def sel_mux_mpc(self, val: MP):
        self.mux_mpc = val

    def decode_and_execute(self):
        signals = self.microprogram[self.mpc_reg]

        for signal in signals:
            if signal in [MP.MUX_ADDR_MEM, MP.MUX_ADDR_ACC, MP.MUX_ADDR_INSTR]:
                self.datapath.sel_mux_addr(signal)
            elif signal in [MP.MUX_ALU_L_INSTR, MP.MUX_ALU_L_MEM]:
                self.datapath.sel_mux_alu_left(signal)
            elif signal in [MP.MUX_ALU_R_ACC, MP.MUX_ALU_R_ZERO]:
                self.datapath.sel_mux_alu_right(signal)
            elif signal in [MP.MUX_PC_NEXT, MP.MUX_PC_JMP, MP.MUX_PC_JZ]:
                self.sel_mux_pc(signal)
            elif signal in [MP.MUX_MPC_NEXT, MP.MUX_MPC_ZERO, MP.MUX_MPC_INSTR]:
                self.sel_mux_mpc(signal)
            elif signal in [MP.ALU_ADD, MP.ALU_MOD]:
                self.datapath.alu(signal, self.instr_reg["arg"])
            elif signal is MP.LATCH_ADDR:
                self.datapath.latch_addr_reg(self.instr_reg["arg"])
            elif signal is MP.LATCH_ACC:
                self.datapath.latch_acc_reg()
            elif signal is MP.LATCH_PC:
                self.latch_pc_reg()
            elif signal is MP.LATCH_MPC:
                self.latch_mpc_reg()
            elif signal is MP.LATCH_INSTR:
                self.latch_instr_reg()
            elif signal is MP.WR:
                self.datapath.wr()
            elif signal is MP.HALT:
                raise StopIteration()
            else:
                raise ValueError(f"Wrong signal: {signal}")

        self.tick()

    def __repr__(self):
        state_repr = (
            f"TICK: {self._tick:3} "
            f"{self.instr_reg['opcode'].name:6} "
            f"PC: {self.pc_reg:3} "
            f"MPC: {self.mpc_reg:2} "
            f"AR: {self.datapath.addr_reg:3} "
            f"ACC: {self.datapath.acc_reg:3} "
        )
        return state_repr
