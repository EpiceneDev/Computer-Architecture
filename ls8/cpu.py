"""CPU functionality."""

import sys

'''
Meanings of the bits in the first byte of each instruction: `AABCDDDD`

* `AA` Number of operands for this opcode, 0-2
* `B` 1 if this is an ALU operation
* `C` 1 if this instruction sets the PC
* `DDDD` Instruction identifier
'''
HALT = 1
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01011000
RET = 0b00011001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

class CPU:
    """Main CPU class."""
   

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 memory

        self.set_pc_flag = False # True if instruction sets the pc

        self.running = True
         # 8 general-purpose 8-bit numeric registers R0-R7.
        # R5 is reserved as the interrupt mask (IM)
        # R6 is reserved as the interrupt status (IS)
        # R7 is reserved as the stack pointer (SP)

        # 8 general purpose registers
        # start counting from 0: R0 - R7
        self.registers = [None] * 8

        # Assign stack pointer per specs
        self.registers[SP] = 0xF4

        # add properties for any internal registers you need, e.g. PC (program counter) 
        #lives at address 00
        self.pc = 0 # program pointer

        # CMP Flags
        self.fl = 0b00000000

        self.branchtable = {
            HALT: self.halt,
            PRN: self.prn,
            LDI: self.ldi,
            MUL: self.mul,
            ADD: self.add,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            CMP: self.cmp,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
                
       



    #     '''
    #     FL bits: 00000LGE
    #     L Less-than: during a CMP, set to 1 if registerA is less than registerB, zero otherwise.
    #     G Greater-than: during a CMP, set to 1 if registerA is greater than registerB, zero otherwise.
    #     E Equal: during a CMP, set to 1 if registerA is equal to registerB, zero otherwise.
    #     '''
    #     # self.flag = 3
    #     # self.register[self.flag] = "00000LGE"



    def load(self, file):
        """Load a program into memory."""

        # if you forget the filename
        if len(sys.argv) < 2:
            print("did you forget the file to open?")
            print('Usage: filename file_to_open')
            sys.exit()

        
        address = 0
        print(sys.argv)
        try: 
            # Load program into memory
            # 
            with open(sys.argv[1]) as file:
                for line in file:
                    # parse out spaces and comments 
                    returned_split = line.split("#")

                    possible_num = returned_split[0].strip()

                    # ignore blanks
                    if possible_num == ' ':
                        continue

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

    def push_val(self, val):
        self.reg[SP] -= 1
        self.ram_write(val, self.reg[7])

    def pop_val(self):
        val = self.ram_read(self.reg[7])
        self.reg[SP] += 1
        return val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "CMP":
             self.fl &= 0b00000000
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")
        
        self.pc += 3

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
        while self.running:
            # Get the first instruction
            ir = self.ram[self.pc]

            # bits for opcode
            num_operands = ((ir >> 6) & 0b11)  == 1

            # flag for allow to set the PC -> true or false
            self.inst_set_pc = ((ir >> 4) & 0b1) == 1

            # retrieve the argvs
            operand_a = self.ram_read(self.pc + 1) # register
            operand_b = self.ram_read(self.pc + 2) # immediate value

            # check if instruction exists
            if ir in self.branchtable:
                self.branchtable[ir](operand_a, operand_b)
            else:
                raise Exception(f"Invalid instruction {hex(ir)} at address {hex(self.pc)}")

            # # If IR is ALU command, send to ALU
            # is_alu_command = (IR >> 5) & 0b001

            # if is_alu_command:
            #     self.alu(IR, operand_a, operand_b)

            if not self.set_pc_flag:
                self.pc += num_operands


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
        self.alu("ADD", operand_a, operand_b)

    def push(self, operand_a, operand_b):
        # decrement the SP
        # sp = self.registers[7] 
        # self.registers[SP] -= 1

        # first operand is address of reg holding value
        # register_address = self.register[operand_a]
        # put in memory
        # self.ram[sp] = registers[register_address]
        self.ram[sp] = self.register[operand_a]

    def pop(self, operand_a, _):
        # sp = self.registers[7]
        # set the value at the pointer
        self.registers[operand_a] = self.ram[sp]
        
        self.registers[SP] += 1

    def halt(self):
        self.running = False
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
        return_address = self.ram[sp]

        registers[7] += 1

        self.pc = return_address

    

    # Add the CMP instruction and equal flag to your LS-8.
    def cmp(self, operand_a, operand_b):
        pass

    # Add the JMP instruction.
    def jmp(self, operand_a):
        pass

    # Add the JEQ and JNE instructions.
    def jeq(self):
        pass

    def jne(self):
        pass

