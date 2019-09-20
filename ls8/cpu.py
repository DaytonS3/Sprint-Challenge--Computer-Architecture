import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # r0 - r7
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.flag = 0

    def ram_read(self, a):
        return self.ram[a]

    def ram_write(self, v, a):
        self.ram[a] = v

    def load(self, a):
        """Load a program into memory."""

        program = []

        with open(a) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()
                try:
                    program.append(int(num, 2))
                except ValueError:
                    pass

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 2
            else:
                self.flag = 4
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        HTL = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110
        """Run the CPU."""
        self.running = True
        while self.running:
            ram = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc+2)

            if ram == HTL:
                x = False
                sys.exit(1)
            elif ram == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ram == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ram == CMP:  # CMP
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif ram == MUL:  # MUL
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif ram == JMP:
                self.pc = self.reg[operand_a]
            elif ram == JEQ:
                if self.flag == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ram == JNE:
                if self.flag != 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ram == PUSH:
                num = self.ram[self.pc + 1]
                self.ram[self.start] = self.reg[num]
                self.start -= 1
                self.pc += 2
            elif ram == POP:
                num = self.ram[self.pc + 1]
                self.ram[self.start] = self.reg[num]
                self.start += 1
                self.pc += 2
            else:
                print('command not found')
