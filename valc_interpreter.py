# ValC: An esolang based on Val Kilmer quotes

import re

class ValCInterpreter:
    def __init__(self):
        self.variables = {}
        self.lines = []
        self.pointer = 0
        self.functions = {}
        self.call_stack = []

    def parse_value(self, value):
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        elif value.isdigit():
            return int(value)
        elif value in self.variables:
            return self.variables[value]
        else:
            # Instead of error, return the raw string (variable name)
            # or raise with better message if you want strictness
            return value


    def run(self, code):
        self.lines = [line.strip() for line in code.splitlines() if line.strip()]
        self.pointer = 0
        self.print_logo()
        while self.pointer < len(self.lines):
            self.execute_line(self.lines[self.pointer])
            self.pointer += 1

    def execute_line(self, line):
        tokens = line.split()

        if line.startswith("I AM BATMAN"):
            varname = tokens[3]
            self.variables[varname] = 0

        elif line.startswith("I'M JUST YOUR HUCKLEBERRY"):
            varname = tokens[4]
            value = self.parse_value(" ".join(tokens[5:]))
            self.variables[varname] = value

        elif line.startswith("SAY WHEN"):
            value = self.parse_value(" ".join(tokens[2:]))
            print(value)

        elif line.startswith("ASK ME ANYTHING"):
            varname = tokens[3]
            user_input = input(f"Input for {varname}: ")
            self.variables[varname] = int(user_input) if user_input.isdigit() else user_input

        elif line.startswith("I'M YOUR HUCKLEBERRY"):
            varname = tokens[3]
            condition = self.variables.get(varname, False)
            if not condition:
                self.skip_to_else_or_end()

        elif line.startswith("YOU'RE A DAISY IF YOU DO"):
            self.skip_to_end()

        elif line.startswith("POOR SOUL"):
            pass

        elif line.startswith("THIS PARTY'S OVER"):
            varname = tokens[3]
            self.variables[varname] += 1

        elif line.startswith("JUST KISS THE BRIDE"):
            varname = tokens[3]
            self.variables[varname] -= 1

        elif line.startswith("YOU CAN BE MY WINGMAN ANYTIME"):
            self.loop_start = self.pointer
            varname = tokens[6]
            if not self.variables.get(varname):
                self.skip_to_end_while()

        elif line.startswith("BULLSEYE"):
            self.pointer = self.loop_start - 1

        elif line.startswith("REMEMBER WHO YOU ARE"):
            func_name = tokens[4]
            self.functions[func_name] = self.pointer + 1
            self.skip_to_end_function()

        elif line.startswith("FORGET ABOUT IT"):
            pass

        elif line.startswith("CALL ME"):
            func_name = tokens[2]
            if func_name in self.functions:
                self.call_stack.append(self.pointer)
                self.pointer = self.functions[func_name] - 1
            else:
                raise ValueError(f"Function {func_name} not defined")

        elif line.startswith("WHAT'S THE SCORE"):
            var1 = self.parse_value(tokens[3])
            var2 = self.parse_value(tokens[5])
            operation = tokens[4]
            result = None
            if operation == "+":
                result = var1 + var2
            elif operation == "-":
                result = var1 - var2
            elif operation == "*":
                result = var1 * var2
            elif operation == "/":
                result = var1 // var2
            self.variables[tokens[6]] = result

        elif line.startswith("TELL ME MORE"):
            var1 = self.parse_value(tokens[3])
            var2 = self.parse_value(tokens[4])
            self.variables[tokens[5]] = str(var1) + str(var2)

    def skip_to_else_or_end(self):
        depth = 1
        while self.pointer < len(self.lines) - 1:
            self.pointer += 1
            line = self.lines[self.pointer]
            if line.startswith("I'M YOUR HUCKLEBERRY"):
                depth += 1
            elif line.startswith("POOR SOUL"):
                depth -= 1
                if depth == 0:
                    break
            elif line.startswith("YOU'RE A DAISY IF YOU DO") and depth == 1:
                break

    def skip_to_end(self):
        depth = 1
        while self.pointer < len(self.lines) - 1:
            self.pointer += 1
            line = self.lines[self.pointer]
            if line.startswith("I'M YOUR HUCKLEBERRY"):
                depth += 1
            elif line.startswith("POOR SOUL"):
                depth -= 1
                if depth == 0:
                    break

    def skip_to_end_while(self):
        depth = 1
        while self.pointer < len(self.lines) - 1:
            self.pointer += 1
            line = self.lines[self.pointer]
            if line.startswith("YOU CAN BE MY WINGMAN ANYTIME"):
                depth += 1
            elif line.startswith("BULLSEYE"):
                depth -= 1
                if depth == 0:
                    break

    def skip_to_end_function(self):
        while self.pointer < len(self.lines) - 1:
            self.pointer += 1
            if self.lines[self.pointer].startswith("FORGET ABOUT IT"):
                break

    def print_logo(self):
        print("""
 __     ___      _      ____   
 \\ \\   / (_)    | |    |  _ \\  
  \\ \\_/ / _  ___| | __ | | | | 
   \\   / | |/ __| |/ / | | | | 
    | |  | | (__|   <  | |_| | 
    |_|  |_|\\___|_|\\_\\ |____/  
ValC - Val Kilmer esoteric language
        """)


def run_valc_file(filename):
    with open(filename, 'r') as f:
        code = f.read()
    interpreter = ValCInterpreter()
    interpreter.run(code)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ValC - Val Kilmer esoteric language interpreter")
    parser.add_argument("file", help="Path to the .valc source file")
    args = parser.parse_args()
    run_valc_file(args.file)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Example ValC program
        valc_code = """
I AM BATMAN a
I'M JUST YOUR HUCKLEBERRY a 5
I AM BATMAN b
I'M JUST YOUR HUCKLEBERRY b 10
WHAT'S THE SCORE a + b result
SAY WHEN result

I AM BATMAN name
I'M JUST YOUR HUCKLEBERRY name "Val"
TELL ME MORE name " Kilmer" fullname
SAY WHEN fullname
"""
        interpreter = ValCInterpreter()
        interpreter.run(valc_code)
