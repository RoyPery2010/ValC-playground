import os
import streamlit as st

# ===== ValC Interpreter =====

class ValCInterpreter:
    def __init__(self):
        self.variables = {}
        self.lines = []
        self.pointer = 0
        self.functions = {}
        self.call_stack = []
        self.loop_start = None
        self.output = []

    def parse_value(self, value):
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')
        elif value.isdigit():
            return int(value)
        elif value in self.variables:
            return self.variables[value]
        else:
            raise ValueError(f"Unknown value: {value}")

    def run(self, code):
        self.variables = {}
        self.pointer = 0
        self.output = []
        self.lines = [line.strip() for line in code.splitlines() if line.strip()]
        while self.pointer < len(self.lines):
            self.execute_line(self.lines[self.pointer])
            self.pointer += 1
        return "\n".join(str(line) for line in self.output)

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
            self.output.append(value)
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

# ===== Streamlit app setup =====

st.set_page_config(page_title="ValC Playground 🎭", page_icon="🎬", layout="centered")

st.title("🎭 ValC Playground")
st.write("Write and run Val Kilmer–themed esolang programs!")

# Load example files from ./examples
EXAMPLES_DIR = "examples"
example_files = []
if os.path.exists(EXAMPLES_DIR):
    example_files = [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".valc")]

example_choice = st.selectbox("Load example ValC program:", ["-- Select --"] + example_files)

if example_choice != "-- Select --":
    with open(os.path.join(EXAMPLES_DIR, example_choice), "r", encoding="utf-8") as f:
        code_input = f.read()
    st.session_state["uploaded_code"] = code_input
else:
    code_input = st.session_state.get("uploaded_code", '''I AM BATMAN a\nI'M JUST YOUR HUCKLEBERRY a 10\nSAY WHEN a''')

code_input = st.text_area("📝 Write your ValC code here:", height=350, value=code_input)

if st.button("▶️ Run ValC code"):
    interpreter = ValCInterpreter()
    try:
        output = interpreter.run(code_input)
        st.text_area("Output:", value=output, height=150, disabled=True)
    except Exception as e:
        st.error(f"Error: {e}")

def download_valc_code(code: str, filename: str = "program.valc"):
    st.download_button(
        label="💾 Download your ValC code",
        data=code,
        file_name=filename,
        mime="text/plain",
    )

download_valc_code(code_input)

# Tutorial panel
if 'tutorial_step' not in st.session_state:
    st.session_state.tutorial_step = 0

tutorial_steps = [
    ("Welcome!", "Welcome to ValC! Let's start by declaring a variable:\n\n```\nI AM BATMAN a\nI'M JUST YOUR HUCKLEBERRY a 5\nSAY WHEN a\n```"),
    ("Math", "You can do math like this:\n\n```\nI AM BATMAN x\nI'M JUST YOUR HUCKLEBERRY x 3\nI AM BATMAN y\nI'M JUST YOUR HUCKLEBERRY y 4\nWHAT'S THE SCORE x + y sum\nSAY WHEN sum\n```"),
    ("Functions", "Define and call functions:\n\n```\nREMEMBER WHO YOU ARE greet\n  SAY WHEN \"Hello from greet!\"\n  I’LL BE BACK\nFORGET ABOUT IT\nCALL ME greet\n```"),
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Previous Tutorial Step"):
        st.session_state.tutorial_step = max(0, st.session_state.tutorial_step - 1)
with col2:
    if st.button("Next Tutorial Step ➡️"):
        st.session_state.tutorial_step = min(len(tutorial_steps) - 1, st.session_state.tutorial_step + 1)

step_title, step_code = tutorial_steps[st.session_state.tutorial_step]

st.markdown(f"### Tutorial Step {st.session_state.tutorial_step + 1}: {step_title}")
st.code(step_code, language="plaintext")
