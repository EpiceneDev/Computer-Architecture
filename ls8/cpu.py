"""CPU functionality."""

import sys



HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0 # program pointer
        self.ram = [0] * 256 # 256k memory
        self.register = [0] * 8 # 8k register

    def ram_read(self, MAR):
        # MAR is mem address register to read data from
        return self.ram[MAR]

        # MDR is the data in the memory register
    def ram_write(self, MAR, MDR):
        self.ram[MDR] = MAR

    def load(self, file):
        """Load a program into memory."""

        # if you forget the filename
        if len(sys.argv) < 2:
            print("did you forget the file to open?")
            print('Usage: filename file_to_open')
            sys.exit()


        address = 0

        try: 
            # Load program into memory
            with open(sys.argv[1]) as file:
                for line in file:
                    returned_split = line.split('#')
                    possible_num == returned_split[0]
                    if possible_num == ' ':
                        continue

                    if possible_num == '1' or possible_num[0] == '0':
                        num = possible_num[:8]

                    print(f'{num}: {int(num, 2)}')

                    self.ram[address] = int(num, 2)
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # read the memory address that's stored in register PC, 
        # and store that result in IR, the Instruction Register. 
        running = True

        while running:
            # Get the first instruction
            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1) # register
            operand_b = self.ram_read(self.pc + 2) # immediate

            opcode = IR

            if opcode == HLT:
                sys.exit()

            # Set the value of a register to an integer.
            elif opcode == LDI:
                self.register[operand_a] = operand_b
                # Jump over operands to go to next instruction
                self.pc += 3

            # Print the register address
            elif opcode == PRN:
                print(self.register[operand_a])
                self.pc += 2
