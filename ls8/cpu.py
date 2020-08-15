"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""
   

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 memory

        self.running = True
         # 8 general-purpose 8-bit numeric registers R0-R7.
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)

        # 8 general purpose registers
        # start counting from 0: R0 - R7
        self.register = [None] * 8

        # add properties for any internal registers you need, e.g. PC (program counter) 
        #lives at address 00
        self.pc = 0 # program pointer

        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[HLT] = self.hlt
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret

        '''
        FL bits: 00000LGE
        L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
        G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
        E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
        '''
        # self.flag = 3
        # self.register[self.flag] = "00000LGE"


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
            # 
            with open(sys.argv[1]) as file:
                for line in file:
                    # parse out spaces and comments 
                    returned_split = line.strip().split("#")

                    possible_num = returned_split[0].strip()

                    if possible_num == ' ':
                        continue

                    if possible_num[0] == '1' or possible_num[0] == '0':
                        num = possible_num[:8]

                        # print(f'{num}: {int(num, 2)}')

                        self.ram[address] = int(num, 2)
                        address += 1

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit(2)

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

    def ram_read(self, MAR):
        # MAR is mem address register to read data from
        return self.ram[MAR]

        # MDR is the data in the memory register
    def ram_write(self, MAR, MDR):
        self.ram[MDR] = MAR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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
        
        # Assign stack pointer per specs
        registers[7] = 0xF4

        while self.running:
            # Get the first instruction
            IR = self.ram[self.pc]
            # or
            # IR = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1) # register
            operand_b = self.ram_read(self.pc + 2) # immediate

            # Update program pointer
            # Look at first two bits of the instruction for number
            # of agrvs
            self.pc += 1 + (IR >> 6) # 1 + number of argvs
            command = IR # Command

            # If IR is ALU command, send to ALU
            is_alu_command = (IR >> 5) & 0b001

            if is_alu_command:
                self.alu(IR, operand_a, operand_b)


            # Set the value of a register to an integer.
            def ldi(self, operand_a, operand_b):
                self.register[operand_a] = operand_b
                # Jump over operands to go to next instruction
                # self.pc += 3 <-- don't need because of bit shifting

            # Print the register address
            def prn(self, operand_a, _):
                print(self.register[operand_a])
                # self.pc += 2

            def save(self, operand_a, operand_b):
                num = operand_a
                index = operand_b
                registers[index] = num

            def print_register(self, operand_a):
                reg_idx = operand_a
                print(registers[reg_indx])

            def add(self, operand_a, operand_b):
                return self.alu(ADD, operand_a, operand_b)

            def push(self, operand_a, operand_b):
                # decrement the SP
                sp = self.register[7] 
                sp -= 1

                # first operand is address of reg holding value
                # register_address = self.register[operand_a]
                # put in memory
                # self.ram[sp] = registers[register_address]
                self.ram[sp] = self.register[operand_a]

            def pop(self, operand_a, _):
                sp = self.register[7]
                # set the value at the pointer
                self.registers[operand_a] = self.ram[sp]
                
                register[7] += 1

            if command == HLT:
                sys.exit()

            def call(self, operand_a, operand_b):
                # remember where to return to by
                # getting address of next instruction
                next_instruction_address = self.pc + 2
                # Push onto the stack...
                ## decrement the SP
                self.register[7] -= 1
                ## put on the stack at the sp
                sp = registers[7]
                
                self.ram[sp] = next_instruction_address

                reg_address = operand_a

                destination_address = self.register[reg_address]

                self.pc = destination_address

            def ret(self, _):
                sp = registers[7]
                sp += 1

