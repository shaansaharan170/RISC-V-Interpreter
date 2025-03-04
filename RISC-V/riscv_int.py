### ENGG 4540 Final Lab ###
### Shaan Saharan & Dev Mistry ###
### Part 1: Building a Simple RISC-V Interpreter ###

import sys

class RISC_V_Simulator:
    def __init__(self):
        """Initialize registers, memory, program counter, and performance metrics."""
        self.registers = {i: 0 for i in range(32)}  # 32 registers
        self.memory = {}  # Simulated memory as a dictionary
        self.pc = 0  # Program counter
        self.instructions = []  # List to store loaded instructions

        # Performance Metrics
        self.instruction_count = 0
        self.memory_accesses = 0
        self.cycle_count = 0  # Assuming single-cycle execution

    def load_program(self, filename):
        """Loads a RISC-V assembly program from a file."""
        with open(filename, 'r') as f:
            content = f.read().strip()
            if "=" in content:  # Detects Python list-style format
                content = content.split("=", 1)[1].strip()
                content = content.replace("[", "").replace("]", "").strip()
                content = content.split('\n')
                self.instructions = [line.strip().strip(',').replace('"', '') for line in content if line.strip()]
            else:
                self.instructions = [line.strip() for line in f.readlines() if line.strip()]

    def execute(self):
        """Executes the loaded RISC-V program instruction by instruction."""
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.pc += 1
            self.execute_instruction(instr)

    def execute_instruction(self, instr):
        """Decodes and executes a single instruction while tracking performance metrics."""
        self.instruction_count += 1
        self.cycle_count += 1  # Assuming single-cycle execution per instruction

        parts = instr.replace(',', '').split()
        opcode = parts[0]

        if opcode == 'ADD':  # Addition instruction
            rd, rs1, rs2 = map(int, parts[1:4])
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        
        elif opcode == 'SUB':  # Subtraction instruction
            rd, rs1, rs2 = map(int, parts[1:4])
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        
        elif opcode == 'LW':  # Load word from memory
            rd, offset, rs = int(parts[1]), int(parts[2]), int(parts[3])
            self.registers[rd] = self.memory.get(self.registers[rs] + offset, 0)
            self.memory_accesses += 1  # Track memory access
        
        elif opcode == 'SW':  # Store word to memory
            rs2, offset, rs1 = int(parts[1]), int(parts[2]), int(parts[3])
            self.memory[self.registers[rs1] + offset] = self.registers[rs2]
            self.memory_accesses += 1  # Track memory access
        
        elif opcode == 'BEQ':  # Branch if equal
            rs1, rs2, label = int(parts[1]), int(parts[2]), parts[3]
            if self.registers[rs1] == self.registers[rs2]:
                self.pc = self.resolve_label(label)
        
        elif opcode == 'JAL':  # Jump and link
            rd, label = int(parts[1]), parts[2]
            self.registers[rd] = self.pc
            self.pc = self.resolve_label(label)

        elif opcode == 'LI':  # Load immediate
            rd, imm = int(parts[1]), int(parts[2])
            self.registers[rd] = imm

        else:
            print(f'Unknown instruction: {instr}')

    def resolve_label(self, label):
        """Finds the line number of a given label or uses a numeric address."""
        if label.isdigit():
            return int(label)  # Numeric labels are treated as direct line numbers
        for i, instr in enumerate(self.instructions):
            if instr.endswith(':') and instr[:-1] == label:
                return i
        return self.pc  # Default to next instruction if label not found

    def print_performance_metrics(self):
        """Prints execution metrics after program execution."""
        print("\n--- Performance Metrics ---")
        print(f"Total Instructions Executed: {self.instruction_count}")
        print(f"Total Cycles: {self.cycle_count}")
        print(f"Memory Accesses (LW/SW): {self.memory_accesses}")

    def print_state(self):
        """Prints the current state of registers and memory."""
        print("\n--- Register State ---")
        for reg, val in sorted(self.registers.items()):
            print(f"x{reg}: {val}")

        print("\n--- Memory State ---")
        for addr, val in sorted(self.memory.items()):
            print(f"{addr}: {val}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 riscv_int.py <program_file.txt>")
        sys.exit(1)
    
    filename = sys.argv[1]
    simulator = RISC_V_Simulator()
    simulator.load_program(filename)  # This was missing
    simulator.execute()
    simulator.print_state()
    simulator.print_performance_metrics()  # Print metrics
