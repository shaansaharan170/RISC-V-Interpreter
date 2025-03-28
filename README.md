# **RISC-V Interpreter**  

## **Overview**  
This project is a simple **RISC-V instruction set simulator** written in Python. It sequentially executes a subset of RISC-V assembly instructions, provides a functional register file, simulates memory, and tracks execution performance.  

## **Supported Instructions**  
The interpreter currently supports the following RISC-V instructions:  

- **Arithmetic Instructions:** `ADD`, `SUB`  
- **Memory Operations:** `LW` (Load Word), `SW` (Store Word)  
- **Control Flow Instructions:** `BEQ` (Branch if Equal), `JAL` (Jump and Link)  
- **Immediate Loading:** `LI` (Load Immediate)  

## **Project Structure**  
- `riscv_int.py` → Main Python script containing the interpreter.  
- `ProgramX.txt` → Example RISC-V assembly files for execution.  

## **How to Use**  
### **1. Running the Interpreter**  
Ensure you have Python installed (version 3+ recommended). Open a terminal and navigate to the folder containing `riscv_int.py`. Run:  

```sh
python3 riscv_int.py ProgramX.txt
```
Replace `X` with any other program file you want to execute.  

### **2. Expected Output**  
The program will execute the instructions and print:  
1. **Register state** (values of registers after execution).  
2. **Memory state** (values stored in memory after execution).  
3. **Performance metrics** (instruction count, cycle count, memory accesses).  

**Example Output:**  
```
--- Register State ---
x0: 0
x1: 5
x2: 10
x3: 20
...

--- Memory State ---
100: 25
104: 30
...

--- Performance Metrics ---
Total Instructions Executed: 10
Total Cycles: 10
Memory Accesses (LW/SW): 2
```

## **Performance Analysis**  
The interpreter tracks execution performance using the following metrics:  
**Total instructions executed**  
**Cycle count** (assuming a single-cycle processor)  
**Memory accesses** (`LW` and `SW`)  

These results can be compared against **Ripes/Venus** using the same program.

---

## **Challenges & Design Choices**  
### **1. Instruction Parsing**  
Some program files used a **Python list format** (`programX = [...]`), which is not a standard assembly format. To handle this, additional parsing logic was added:  

#### **Example: Handling Python List Format in Assembly Files**
```python
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
```
**Reason:** This ensures the interpreter can correctly read both standard assembly and Python-style list formats.

---

### **2. Jump and Branch Logic**  
Instead of using **named labels**, numeric labels were used for simplicity. This allows for easier execution without needing to track label positions dynamically.  

#### **Example: Handling BEQ (Branch if Equal) with Numeric Labels**
```python
elif opcode == 'BEQ':  # Branch if Equal
    rs1, rs2, label = int(parts[1]), int(parts[2]), parts[3]
    if self.registers[rs1] == self.registers[rs2]:
        self.pc = self.resolve_label(label)
```
#### **Example: Handling JAL (Jump and Link)**
```python
elif opcode == 'JAL':  # Jump and Link
    rd, label = int(parts[1]), parts[2]
    self.registers[rd] = self.pc  # Save return address
    self.pc = self.resolve_label(label)
```
#### **Example: Resolving Numeric Labels**
```python
def resolve_label(self, label):
    """Finds the line number of a given label or uses a numeric address."""
    if label.isdigit():
        return int(label)  # Numeric labels are treated as direct line numbers
    for i, instr in enumerate(self.instructions):
        if instr.endswith(':') and instr[:-1] == label:
            return i
    return self.pc  # Default to next instruction if label not found
```
**Reason:** Numeric labels make jumps and branches easier to handle without requiring extra tracking of named labels.

---

### **3. Memory Handling with a Dictionary**  
Memory is stored in a dictionary instead of an array for **efficient access**. Instead of allocating a large block of memory, only used addresses are stored.

#### **Example: LW (Load Word) and SW (Store Word) with Dictionary Memory**
```python
elif opcode == 'LW':  # Load word from memory
    rd, offset, rs = int(parts[1]), int(parts[2]), int(parts[3])
    self.registers[rd] = self.memory.get(self.registers[rs] + offset, 0)
    self.memory_accesses += 1  # Track memory access

elif opcode == 'SW':  # Store word to memory
    rs2, offset, rs1 = int(parts[1]), int(parts[2]), int(parts[3])
    self.memory[self.registers[rs1] + offset] = self.registers[rs2]
    self.memory_accesses += 1  # Track memory access
```
**Reason:** A dictionary allows **efficient lookups** and avoids wasting memory by only storing used addresses.

---

## **Next Steps & Improvements**  
- Expand the instruction set to support more RISC-V operations.  
- Add support for more complex branching and loops.  
- Implement a cycle counter for performance analysis.  

---
