"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0]*256
        self.pc = 0
        self.flag = 0b00000000
        self.IR = {}
        self.reg = [0] * 8
        self.stopped = False
        self.SP = 0xf4

        HLT = 0b00000001
        LDI = 0b10000010
        MUL = 0b10100010
        PRN = 0b01000111
        POP = 0b01000110
        PUSH = 0b01000101
        RET = 0b00010001
        CALL = 0b01010000
        
        self.IR = {
            HLT:self.HLT,
            LDI:self.LDI,
            MUL:self.MULT,
            PRN:self.PRN,
            POP:self.POP,
            PUSH:self.PUSH,
            RET:self.RET,
            CALL:self.CALL
            }

    def CALL(self):
        self.pc += 1 
        self.push()
        self.pc -= 1
        self.pc = self.reg[self.memory[self.pc+1]]
        
    def RET(self):
        self.pc = self.memory[self.SP]
        self.SP += 1
        

    def LDI(self):
        self.reg[self.memory[self.pc+1]] = self.memory[self.pc+2]
                
    def MULT(self):
        self.alu("MULTI",self.reg[self.pc+1],self.reg[self.pc+2])
    
    def PRN(self):
        print(self.reg[self.pc+1])
    
    def PUSH(self):
        self.SP -= 1
        reg_loc = self.memory[self.pc+1]
        self.memory[self.SP] = self.reg[reg_loc]
        self.reg[7] = self.SP
        
        
    def POP(self):
        value = self.memory[self.reg[7]]
        reg_loc = self.memory[self.pc+1]
        self.SP += 1
        self.reg[7]=self.SP
        self.reg[reg_loc] = value
        

    def load(self,program = None):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)
        address = 0
        if program is None:
            program = f"examples/{sys.argv[1]}"
        

        # # For now, we've just hardcoded a program:
        # if program is None:
        #     program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        #     ]

        try:
            with open(program) as f:
                for line in f:
                    line = line.strip()
                    if line == "" or  line[0] =="#": 
                       continue 
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value,2)
                        
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)
                        
                    self.memory[address] = value
                    address += 1
                    
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)
            
    def ram_read(self,MAR):
        return self.reg[MAR]
    
    def FLG(self,v_a,v_b):
        if v_a < v_b:
            self.flag = 0b00000100
            
        elif v_a > v_b:
            self.flag = 0b00000010
            
        elif v_a == v_b:
            self.flag = 0b00000001
        else:
            self.flag = 0b00000000
       
    
    def ram_write(self,MAR,MDR):
        self.reg[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULTI":
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
    
    def oprt_2(self,op_num):
        if op_num == 0b10000010:
            pass
    def PC_move(self,op):
        move = op & 11000000
        move_num = (move >> 6)+1
        return move_num
    
    def run(self):
        """Run the CPU."""
        
        
        
        operation = self.memory
        PC = self.pc
        while self.stopped == False:
            op = operation[PC]
            if op == 0b10000010:
                
                self.reg[operation[PC+1]] = operation[PC+2]
                
                PC += self.PC_move(op)
                
            elif op == 0b00000000:
               
                PC += self.PC_move(op)
                
            elif op == 0b00001000:
                PC += self.PC_move(op)
                
            elif op == 0b10100010:
                self.alu("MULTI",self.memory[PC+1],self.memory[PC+2])
                
                PC += self.PC_move(op)
                
            elif op == 0b01000111:
                 
                print(self.reg[operation[PC+1]])
                PC += self.PC_move(op)
                
            elif op == 0b00000001:
                self.stopped = True
                self.HLT()
                PC += self.PC_move(op)
                
            elif op == 0b01000101:    
                self.SP -= 1
                reg_loc = self.memory[PC+1]
                self.memory[self.SP] = self.reg[reg_loc]
                self.reg[7] = self.SP
                PC += self.PC_move(op)
                
            elif op == 0b01000110:
                value = self.memory[self.reg[7]]
                reg_loc = self.memory[PC+1]
                self.SP += 1
                self.reg[7]=self.SP
                self.reg[reg_loc] = value
                PC += self.PC_move(op)
                
            elif op == 0b01010000:
                self.SP -= 1
                self.reg[self.SP] = self.memory[PC+2]
                PC = self.reg[self.memory[PC+1]]
                
            elif op == 0b00010001:
                PC = self.reg[self.SP]
                self.SP += 1
                
            else:
                self.stopped = True
                print("operation incorrect")
                self.HLT()
                
    def run2(self):
        while self.pc is not None:
            self.IR[self.memory[self.pc]]()
            if (self.memory[self.pc] & 0b00010000) != 0b00010000:
                self.pc += self.PC_move(self.memory[self.pc])
        
            
