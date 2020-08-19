"""CPU functionality"""
import sys
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.fl = 0b00000000
        self.pc = 0
        self.running = True
    def alu(self, ir, reg_a, reg_b):
        if ir == "CMP":
            self.fl &= 0b00000000
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            self.pc += 3
    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 3
    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2
    def jmp(self, reg_num):
        self.pc = self.reg[reg_num]
    def jeq(self, reg_num):
        if self.fl & 1 == 1:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
    def jne(self, reg_num):
        if self.fl & 1 == 0:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2
    def hlt(self):
        self.running = False
    def load(self):
        if len(sys.argv) < 2:
            print(
                "Please pass in a second filename: python3 in_and_out.py second_filename.py")
            sys.exit()
        program = sys.argv[1]
        try:
            address = 0
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue
                    ir = int(command, 2)
                    self.ram[address] = ir
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()
    def run(self):
        self.load()
        while self.running:
            ir = self.ram[self.pc]
            if ir == CMP:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu("CMP", reg_a, reg_b)
            elif ir == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.ldi(reg_num, value)
            elif ir == PRN:
                reg_num = self.ram[self.pc + 1]
                self.prn(reg_num)
            elif ir == JMP:
                reg_num = self.ram[self.pc + 1]
                self.jmp(reg_num)
            elif ir == JEQ:
                reg_num = self.ram[self.pc + 1]
                self.jeq(reg_num)
            elif ir == JNE:
                reg_num = self.ram[self.pc + 1]
                self.jne(reg_num)
            elif ir == HLT:
                self.hlt()
            else:
                print(f"Unknown instruction {ir}")
                
if __name__ == "__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()