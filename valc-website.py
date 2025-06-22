import streamlit as st
from io import StringIO
import sys

# Import your interpreter
from valc_interpreter import ValCInterpreter  # Make sure valc_interpreter.py is in the same folder

st.set_page_config(page_title="ValC Playground", layout="wide")

def run_valc_code(code):
    interpreter = ValCInterpreter()
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        interpreter.run(code)
        output = mystdout.getvalue()
    except Exception as e:
        output = f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout
    return output

st.title("🎬 ValC Playground")
st.markdown("**The Val Kilmer Esoteric Programming Language**")

with st.expander("💡 Example Program"):
    st.code("""
I AM BATMAN a
I'M JUST YOUR HUCKLEBERRY a 10
I AM BATMAN b
I'M JUST YOUR HUCKLEBERRY b 20
WHAT'S THE SCORE a + b result
SAY WHEN result
    """, language="valc")

valc_code = st.text_area("📝 Write your ValC code below:", height=300, placeholder='Type ValC code here...')

if st.button("▶️ Run"):
    output = run_valc_code(valc_code)
    st.text_area("🖨️ Output:", value=output, height=200)
