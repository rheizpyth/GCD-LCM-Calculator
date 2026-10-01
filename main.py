"""Streamlit UI. Run with:  streamlit run app.py"""
import streamlit as st

from solution import build_solution
from divisibility import build_division, build_set_division, build_divisors


def parse_numbers(text: str) -> list:
    # Accept spaces and/or commas as separators
    return [int(piece) for piece in text.replace(",", " ").split()]


st.title("Number Theory Calculator")

tab_gcd, tab_div = st.tabs(["GCD and LCM", "Divisibility and Division"])

# =====================================================================
# TAB 1: GCD / LCM
# =====================================================================
with tab_gcd:
    st.write("Step-by-step Euclidean algorithm, linear combination, and LCM. Works for two or more numbers.")

    user_input = st.text_input(
        "Numbers (separated by spaces or commas)",
        placeholder="e.g. 67 69",
        key="gcd_input",
    )

    if st.button("Calculate", key="gcd_btn"):
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

        st.subheader("Final Answers")
        st.success(sol["gcd_answer"])
        st.success(f"Linear combination: {sol['lin_answer']}")
        st.success(f"Coefficients: {sol['xy_answer']}")
        st.success(sol["lcm_answer"])

        st.divider()

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

# =====================================================================
# TAB 2: Divisibility and Division
# =====================================================================
with tab_div:
    st.write("Division Algorithm (a = qd + r, 0 ≤ r < |d|), divisibility tests, and divisors of integers.")

    mode = st.radio(
        "What do you want to do?",
        [
            "Divide one integer by another",
            "Divide a set of integers by one divisor",
            "Find all divisors of an integer",
        ],
    )

    if mode == "Divide one integer by another":
        col1, col2 = st.columns(2)
        a_text = col1.text_input("Dividend (a)", placeholder="e.g. -17", key="div_a")
        d_text = col2.text_input("Divisor (d)", placeholder="e.g. 5", key="div_d")

        if st.button("Calculate", key="div_btn"):
            try:
                a, d = int(a_text), int(d_text)
            except ValueError:
                st.error("Invalid input. Enter whole numbers only.")
                st.stop()
            if d == 0:
                st.error("The divisor cannot be zero.")
                st.stop()

            res = build_division(a, d)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["divis_answer"])

            st.divider()
            st.subheader("Division Algorithm Solution")
            st.code(res["steps"], language="text")

            st.divider()
            st.subheader("Divisibility")
            st.code(res["divis_steps"], language="text")
            st.info(res["divis_answer"])

    elif mode == "Divide a set of integers by one divisor":
        set_text = st.text_input(
            "Set of integers (separated by spaces or commas)",
            placeholder="e.g. 12 -17 25 40 7",
            key="set_nums",
        )
        d_text = st.text_input("Divisor (d)", placeholder="e.g. 5", key="set_d")

        if st.button("Calculate", key="set_btn"):
            try:
                nums = parse_numbers(set_text)
                d = int(d_text)
            except ValueError:
                st.error("Invalid input. Enter whole numbers only.")
                st.stop()
            if not nums:
                st.error("Enter at least one integer.")
                st.stop()
            if d == 0:
                st.error("The divisor cannot be zero.")
                st.stop()

            res = build_set_division(nums, d)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["not_answer"])

            st.divider()
            st.subheader("Solution")
            st.code(res["steps"], language="text")

    else:
        n_text = st.text_input("Integer (n)", placeholder="e.g. 36", key="divisors_n")

        if st.button("Calculate", key="divisors_btn"):
            try:
                n = int(n_text)
            except ValueError:
                st.error("Invalid input. Enter a whole number.")
                st.stop()
            if n == 0:
                st.error("Every nonzero integer divides 0, so please enter a nonzero integer.")
                st.stop()

            res = build_divisors(n)

            st.subheader("Final Answers")
            st.success(res["answer"])
            st.success(res["all_answer"])

            st.divider()
            st.subheader("Solution (testing each i up to √|n|)")
            st.code(res["steps"], language="text")
