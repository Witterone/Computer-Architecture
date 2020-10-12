"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.pc = 0
        self.flag = 0b00000000
        self.mdr = None
        self.reg = []

    def load(self,program = None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if program is None:
            program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self,addrs):
        return self.ram[addrs]
    
    def FLG(self,v_a,v_b):
        if v_a < v_b:
            self.flag = 0b00000100
            
        elif v_a > v_b:
            self.flag = 0b00000010
            
        else:
            self.flag = 0b00000001
        
    
    def ram_write(self,point,update):
        self.ram[point] = update

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
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def HLT(self):
        sys.exit()
    
    
    def run(self):
        """Run the CPU."""
        MAR = None
        stopped = False
        operation = self.ram
        IR = self.pc
        while stopped == False:
            op = operation[IR]
            if op == 0b10000010:
                
                IR += 2
                
            elif op == 0b00000000:
               
                IR += 1
                
            elif op == 0b00001000:
                IR += 1
                
            elif op == 0b01000111:
                MAR = operation[IR-1]
                print(MAR)
                IR += 1
                
            elif op == 0b00000001:
                stopped = True
                IR += 1
                
            else:
                stopped = True
                print("operation incorrect")
                self.HLT()
                
        
        
            
