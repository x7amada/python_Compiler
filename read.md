# Mini Programming Language (Compiler & Interpreter)

##  Overview
This project is a custom-designed **mini programming language** with its own compiler and interpreter.  
It supports core programming concepts such as loops, conditionals, variables, arrays, and basic data types.

The system translates user-written code into tokens, parses them into commands, performs semantic analysis, and executes them.

---

##  Features
- Variable declaration and reassignment  
- Control structures:
  - `if / else`
  - `while`
  - `for`
- Data types:
  - int, float, string, boolean  
  - array, tuple  
- Basic operations and expressions  
- Print functionality  
- Simple built-in functions for arrays, strings, and tuples  

---

##  How It Works

### 1. Lexical Analysis (Lexer)
- Converts input code into tokens  
- Identifies:
  - numbers, identifiers, keywords, strings  
- Processes input **character-by-character** :contentReference[oaicite:0]{index=0}  

---

### 2. Parsing (Parser)
- Groups tokens into valid commands  
- Detects syntax errors  
- Produces structured command list :contentReference[oaicite:1]{index=1}  

---

### 3. Semantic Analysis
- Validates logic and variable usage  
- Detects semantic errors (e.g., undefined variables) :contentReference[oaicite:2]{index=2}  

---

### 4. Execution Engine
- Executes commands sequentially  
- Supports:
  - Assignments  
  - Loops (`for`, `while`)  
  - Conditions (`if`)  
  - Function calls  
  - Print statements :contentReference[oaicite:3]{index=3}  

---

##  How to Run

### Option 1: Run Code as String
```python
from new_lan import miniLang

mini = miniLang()

code = """
int d = 32
array a = [1]

for (int i = 0, i < d, i = i + 1){
    int count = i
    while(count > 0){
        a.append(count)
        count = count - 1
    }
}

print a
"""
mini.analize(code)
mini.read_code()


### Option 2:Run from File
mini.file_to_code("path/to/code.txt")
mini.read_code() 

