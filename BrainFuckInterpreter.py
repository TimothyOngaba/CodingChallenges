class ASTNode:
    def __init__(self, command, description="", children=None):
        self.command = command
        self.description = description
        self.children = children or []

class BrainfuckInterpreter:
    def __init__(self):
        self.memory = [0] * 30000  # Brainfuck memory
        self.pointer = 0          # Memory pointer
        self.input_buffer = []    # Input buffer for ',' commands

    def interpret(self, ast):
        for node in ast:
            if node.command == '>':
                self.pointer += 1
                if self.pointer >= len(self.memory):
                    raise MemoryError("Pointer moved out of memory bounds (right).")
            elif node.command == '<':
                self.pointer -= 1
                if self.pointer < 0:
                    raise MemoryError("Pointer moved out of memory bounds (left).")
            elif node.command == '+':
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
            elif node.command == '-':
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
            elif node.command == '.':
                print(chr(self.memory[self.pointer]), end='')
            elif node.command == ',':
                if not self.input_buffer:
                    user_input = input("Input a character: ")
                    self.input_buffer.extend(ord(char) for char in user_input)
                self.memory[self.pointer] = self.input_buffer.pop(0) if self.input_buffer else 0
            elif node.command == 'loop':
                while self.memory[self.pointer] != 0:
                    self.interpret(node.children)

def tokenize(code):
    "Tokenise Brainfuck source code into a list of single-character commands"
    valid_commands = {'>', '<', '+', '-', '.', ',', '[', ']'}
    return [char for char in code if char in valid_commands]

def parse(tokens):
    "    Parse tokens into an abstract syntax tree (AST)"
    ast = []
    stack = []

    for token in tokens:
        if token == '[':
            # Start a loop
            new_node = ASTNode(command='loop')
            if stack:
                stack[-1].children.append(new_node)
            else:
                ast.append(new_node)
            stack.append(new_node)
        elif token == ']':
            # End the current loop
            if not stack:
                raise SyntaxError("Mismatched closing bracket ']'")
            stack.pop()
        else:
            # Regular command
            new_node = ASTNode(command=token)
            if stack:
                stack[-1].children.append(new_node)
            else:
                ast.append(new_node)

    if stack:
        raise SyntaxError("Mismatched opening bracket '['")
    
    return ast

def main():
    # Input Brainfuck code
    code = "++++++++[>+>++>+++>++++>+++++>++++++>+++++++>++++++++>+++++++++>++++++++++>+++++++++++>++++++++++++>+++++++++++++>++++++++++++++>+++++++++++++++>++++++++++++++++<<<<<<<<<<<<<<<<-]>>>>>>>>+++.---<<<<<<<<>>>>>>>>>>>>>.<<<<<<<<<<<<<>>>>>>>>>>>>>>-.+<<<<<<<<<<<<<<>>>>>>>>>>>>>>-.+<<<<<<<<<<<<<<>>>>+.-<<<<>>>>.<<<<>>>>>>>>+++.---<<<<<<<<>>>>>>>>>>>>>.<<<<<<<<<<<<<>>>>>>>>>>>>>>-.+<<<<<<<<<<<<<<>>>>>>>>>>>>>>-.+<<<<<<<<<<<<<<>>>>+.-<<<<>>>>+.-<<<<>>>>.<<<<>>>>>>>>>+.-<<<<<<<<<>>>>.<<<<>>>>>>>>>>>>+.-<<<<<<<<<<<<>>>>>>>>>>>>>>---.+++<<<<<<<<<<<<<<>>>>.<<<<>>>>>>>>>>>>+.-<<<<<<<<<<<<>>>>.<<<<>>>>>>>>>>>>>>>----.++++<<<<<<<<<<<<<<<>>>>>>>>>>>>>>++.--<<<<<<<<<<<<<<>>>>>>>>>>>>+.-<<<<<<<<<<<<>>>>>>>>>>>>>+.-<<<<<<<<<<<<<>>>>>>>>>>>>>>--.++<<<<<<<<<<<<<<>>>>+.-<<<<."
    
    # Tokenising and parsing input code
    tokens = tokenize(code)
    ast = parse(tokens)

    # Runing the interpreter
    print("Output:")
    interpreter = BrainfuckInterpreter()
    interpreter.interpret(ast)

if __name__ == "__main__":
    main()
