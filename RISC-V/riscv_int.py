### ENGG 4540 Final Lab ###
### Shaan Saharan ###

import sys

class RISC_V_Simulator:
    def __init__(self):
        """Initialize registers, memory, program counter, and performance metrics."""
        self.registers = {i: 0 for i in range(32)}  # 32 registers
        self.memory = {}  # Simulated memory as a dictionary
        self.pc = 0  # Program counter
        self.instructions = []  # List to store loaded instructions
        self.labels = {}  # Dictionary to store label locations

        # Performance Metrics
        self.instruction_count = 0
        self.memory_accesses = 0
        self.cycle_count = 0  # Assuming single-cycle execution per instruction

    def load_program(self, filename):
        """Loads a RISC-V assembly program from a file and processes labels."""
        with open(filename, 'r') as f:
            content = f.read().strip()
            if "=" in content:  # Detects Python list-style format
                content = content.split("=", 1)[1].strip()
                content = content.replace("[", "").replace("]", "").strip()
                content = content.split('\n')
                self.instructions = [line.strip().strip(',').replace('"', '') for line in content if line.strip()]
            else:
                self.instructions = [line.strip() for line in f.readlines() if line.strip()]
        
        # Identify labels in the program
        self.process_labels()

    def process_labels(self):
        """Stores label locations in a dictionary."""
        for i, instr in enumerate(self.instructions):
            if ":" in instr:  # Detects labels like 'start:', 'done:'
                label = instr.replace(":", "").strip()
                self.labels[label] = i

    def execute(self):
        """Executes the loaded RISC-V program instruction by instruction."""
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            
            # Stop execution if we reach the 'done' label
            #if instr.strip().startswith("done:"):
                #break  # Exit the loop
            
            self.pc += 1
            self.execute_instruction(instr)

    def execute_instruction(self, instr):
        """Decodes and executes a single instruction while tracking performance metrics."""
        parts = instr.replace(',', '').split()
        opcode = parts[0].lower()  # Convert instruction to lowercase for case insensitivity

        # Skip label lines
        if ":" in opcode:
            return

        # Always increment cycle count
        self.cycle_count += 1  # Assuming single-cycle execution per instruction

        if opcode == 'add':  # Addition instruction
            self.instruction_count += 1
            rd, rs1, rs2 = map(int, parts[1:4])
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]

        elif opcode == 'addi':  # Add immediate instruction
            self.instruction_count += 1
            rd, rs1, imm = int(parts[1]), int(parts[2]), int(parts[3])
            self.registers[rd] = self.registers[rs1] + imm

        elif opcode == 'sub':  # Subtraction instruction
            self.instruction_count += 1
            rd, rs1, rs2 = map(int, parts[1:4])
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        
        elif opcode == 'li':  # Load immediate
            self.instruction_count += 1
            rd, imm = int(parts[1]), int(parts[2])
            self.registers[rd] = imm

        elif opcode == 'beq':  # Branch if Equal
            rs1, rs2, label = int(parts[1]), int(parts[2]), parts[3]
            self.instruction_count += 1  # Ensure `beq` counts as an instruction
            if self.registers[rs1] == self.registers[rs2]:  
                self.pc = self.resolve_label(label)  # Jump to the label

        elif opcode == 'jal':  # Jump and Link
            self.instruction_count += 1
            if len(parts) == 3:  # Case: jal x1, label
                rd, label = int(parts[1]), parts[2]
                self.registers[rd] = self.pc  # Save return address
            else:  # Case: jal label
                label = parts[1]
                self.registers[1] = self.pc  # Default return register (x1 as RA)
            self.pc = self.resolve_label(label)  # Jump to label

        elif opcode == 'j':  # Unconditional Jump
            self.instruction_count += 1
            label = parts[1]
            self.pc = self.resolve_label(label)  # Jump to the label

        else:
            print(f'Unknown instruction: {instr}')

    def resolve_label(self, label):
        """Finds the instruction index of a given label."""
        if label in self.labels:
            return self.labels[label]
        else:
            print(f"Error: Label '{label}' not found.")
            return self.pc  # Default to current PC if label not found

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
    simulator.load_program(filename)  
    simulator.execute()
    simulator.print_state()
    simulator.print_performance_metrics()
