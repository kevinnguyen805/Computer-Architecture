"""CPU functionality."""

import sys

LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001
MUL = 0b10100010
# Stack
PUSH = 0b01000101   # push the value in the given register on the stack
POP = 0b01000110    # pop the value at the top of the register (stack) 

class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        # construct RAM + REG + PC 
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7

    def load(self, filename):
        """Load a program into memory."""
        try: 
            address = 0
            #open the file
            with open(sys.argv[1]) as f:
                # read every line 
                for line in f: 
                    # parse out comments 
                    comment_split = line.strip().split("#")
                    #c cast number string to int 
                    value = comment_split[0].strip() 
                    # ignore blank lines 
                    if value == "":
                        continue 
                    instruction = int(value, 2)
                    # populate memory array 
                    self.ram[address] = instruction 
                    address += 1
        except: 
            print("cant find file")
            sys.exit(2)

        # For now, we've just hardcoded a program:
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
        # ADDING SUBTRACTION
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        ## ADDING MULTIPLICATION
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        #
        
        while True: 
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI: 
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN: 
                print(self.reg[operand_a])
                self.pc += 2 
            elif opcode == MUL:  
                self.alu(opcode, operand_a, operand_b)
                self.pc += 3
            elif opcode == HLT:
                sys.exit(0)
            elif opcode == PUSH: #DAY 3 STACK!!!!!!!!
                # you push from the memory to the register
                # UPDATE THE STACK POINTER TO THE MEMORY 
                # decrement the sp and copy (value in the register) --> (address that is being pointed to)
                self.reg[self.sp] -= 1
                val = self.reg[operand_a]
                self.ram[self.reg[self.sp]] = val 
                self.pc += 2
            elif opcode == POP: 
                # pop from the register to the memory 
                # pop the value from the stack --> copy the value from the address being pointed to 
                reg = operand_a 
                val = self.ram[self.reg[self.sp]]
                self.reg[reg] = val 
                self.reg[self.sp] += 1       #increment?
                self.pc += 2
            else: 
                print(f"Did not work")
                sys.exit(1)

        
    # ADDING 2 MORE METHODS 
    def ram_read(self, mar):
        #mar = memory address register
        #mdr = memory data register 
        # read the address and write out the number (data) 
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
