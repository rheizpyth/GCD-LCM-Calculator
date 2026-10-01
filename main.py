"""Streamlit UI. Run with:  streamlit run app.py"""
import streamlit as st

from solution import build_solution


def parse_numbers(text: str) -> list:
    # Accept spaces and/or commas as separators
    return [int(piece) for piece in text.replace(",", " ").split()]


st.title("GCD and LCM Calculator")
st.write("Step-by-step Euclidean algorithm, linear combination, and LCM. Works for two or more numbers.")

user_input = st.text_input(
    "Numbers (separated by spaces or commas)",
    placeholder="e.g. 67 69",
)

if st.button("Calculate"):
    try:
        values = parse_numbers(user_input)
    except ValueError:
        st.error("Invalid input. Enter whole numbers separated by spaces or commas.")
        st.stop()

    if len(values) < 2:
        st.error("Enter at least two numbers.")
        st.stop()

    if any(v == 0 for v in values):
        st.error("Please enter non-zero integers only.")
        st.stop()

    sol = build_solution(values)

    # ---------- FINAL ANSWERS (this is what you copy) ----------
    st.subheader("Final Answers")
    st.success(sol["gcd_answer"])
    st.success(f"Linear combination: {sol['lin_answer']}")
    st.success(f"Coefficients: {sol['xy_answer']}")
    st.success(sol["lcm_answer"])

    st.divider()

    # ---------- SOLUTIONS ----------
    st.subheader("GCD Solution")
    st.code(sol["gcd_steps"], language="text")
    st.info(sol["gcd_answer"])

    st.divider()
    st.subheader("Linear Combination Solution")
    st.code(sol["lin_steps"], language="text")
    st.info(f"Therefore: {sol['lin_answer']}")

    st.divider()
    st.subheader("Finding the Coefficients")
    st.code(sol["xy_steps"], language="text")
    st.info(sol["xy_answer"])

    st.divider()
    st.subheader("LCM Solution")
    st.code(sol["lcm_steps"], language="text")
    st.info(sol["lcm_answer"])
