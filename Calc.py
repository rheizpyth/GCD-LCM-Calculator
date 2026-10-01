import streamlit as st


# =====================================================================
# GCD LCM Calculator
# =====================================================================
def gcd_manual(a: int, b: int) -> int:
    """Plain Euclidean loop, used for quiet calculations."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def euclid_steps(big: int, small: int) -> list:
    """Returns the division steps as (dividend, divisor, quotient, remainder)."""
    steps = []
    while small != 0:
        q = big // small
        r = big % small
        steps.append((big, small, q, r))
        big, small = small, r
    return steps


def fmt_expr(terms: list) -> str:
    """
    Formats a list of (coefficient, text, is_expression) as a sum.
    Example: [(4, "252", False), (-5, "198", False)] -> "4(252) - 5(198)"
    """
    out = ""
    for coef, text, is_expr in terms:
        if coef == 0:
            continue
        mag = abs(coef)
        if mag == 1:
            body = f"({text})" if is_expr else text
        else:
            body = f"{mag}({text})"

        if out == "":
            out = ("-" if coef < 0 else "") + body
        else:
            out += (" - " if coef < 0 else " + ") + body
    return out if out else "0"


# =====================================================================
# STEP-BY-STEP SOLVERS (each returns a list of text lines)
# =====================================================================
def division_lines(big: int, small: int) -> tuple:
    """Lines for the Euclidean divisions. Returns (lines, gcd)."""
    steps = euclid_steps(big, small)
    lines = [f"{a} = {q}({b}) + {r}" for a, b, q, r in steps]
    g = steps[-1][1]  # divisor of the last division (remainder is 0)
    return lines, g


def back_substitution_lines(big: int, small: int) -> tuple:
    """
    Writes the GCD as big(x) + small(y).
    Returns (lines, x, y).
    """
    steps = euclid_steps(big, small)
    k = len(steps)
    g = steps[-1][1]

    # If small divides big, there is nothing to substitute.
    if k == 1:
        return [f"{g} = {big}(0) + {small}(1)"], 0, 1

    # vals[j] = quots[j] * vals[j+1] + vals[j+2]
    vals = [big, small] + [s[3] for s in steps]
    quots = [s[2] for s in steps]

    lines = []
    i = k - 2
    x, y = 1, -quots[i]  # g = x(vals[i]) + y(vals[i+1])
    lines.append(f"{g} = {fmt_expr([(x, str(vals[i]), False), (y, str(vals[i + 1]), False)])}")
    lines.append("")

    while i > 0:
        q = quots[i - 1]
        left, mid = vals[i - 1], vals[i]

        # vals[i+1] = left - q(mid)
        sub_text = f"{left} - {mid}" if q == 1 else f"{left} - {q}({mid})"

        # 1) substitute
        lines.append(f"{g} = {fmt_expr([(x, str(mid), False), (y, sub_text, True)])}")

        # 2) expand
        lines.append(
            f"{g} = {fmt_expr([(x, str(mid), False), (y, str(left), False), (-y * q, str(mid), False)])}"
        )

        # 3) combine like terms: y(left) + (x - y*q)(mid)
        x, y = y, x - y * q
        lines.append(f"{g} = {fmt_expr([(x, str(left), False), (y, str(mid), False)])}")

        # blank line between each round so the rounds are easy to tell apart
        if i > 1:
            lines.append("")

        i -= 1

    return lines, x, y


def build_solution(numbers: list) -> dict:
    """
    Returns a dict with:
      gcd_steps, gcd_answer,
      lin_steps, lin_answer   (None when there are more than 2 numbers),
      lcm_steps, lcm_answer
    """
    nums = [abs(n) for n in numbers]  # work with absolute values
    ordered = sorted(nums, reverse=True)  # highest number first
    count = len(nums)
    joined = ", ".join(map(str, numbers))

    result = {
        "gcd_steps": "",
        "gcd_answer": "",
        "lin_steps": None,
        "lin_answer": None,
        "lcm_steps": "",
        "lcm_answer": "",
    }

    # ---------------- GCD ----------------
    lines = []
    if count == 2:
        big, small = ordered
        div_lines, final_gcd = division_lines(big, small)
        lines += div_lines
    else:
        running = ordered[0]
        for idx in range(1, count):
            nxt = ordered[idx]
            b, s = max(running, nxt), min(running, nxt)
            lines.append(f"Step {idx}: GCD({b}, {s})")
            div_lines, g = division_lines(b, s)
            lines += div_lines
            lines.append(f"→ GCD({b}, {s}) = {g}")
            lines.append("")
            running = g
        final_gcd = running
        if lines and lines[-1] == "":
            lines.pop()

    result["gcd_steps"] = "\n".join(lines)
    result["gcd_answer"] = f"GCD({joined}) = {final_gcd}"

    # ---------------- Linear combination (2 numbers only) ----------------
    if count == 2:
        bs_lines, x, y = back_substitution_lines(big, small)
        result["lin_steps"] = "\n".join(bs_lines)
        result["lin_answer"] = f"{final_gcd} = {big}({x}) + {small}({y})"

    # ---------------- LCM ----------------
    lines = []
    if count == 2:
        final_lcm = (nums[0] * nums[1]) // final_gcd
        lines.append(f"LCM = ({nums[0]} * {nums[1]}) / {final_gcd}")
        lines.append(f"LCM = {final_lcm}")
    else:
        final_lcm = ordered[0]
        for idx in range(1, count):
            nxt = ordered[idx]
            g = gcd_manual(final_lcm, nxt)
            new_lcm = (final_lcm * nxt) // g
            lines.append(f"Step {idx}: LCM({final_lcm}, {nxt}) = ({final_lcm} * {nxt}) / {g} = {new_lcm}")
            lines.append("")
            final_lcm = new_lcm
        if lines and lines[-1] == "":
            lines.pop()

    result["lcm_steps"] = "\n".join(lines)
    result["lcm_answer"] = f"LCM({joined}) = {final_lcm}"

    return result


# =====================================================================
# STREAMLIT UI
# =====================================================================
def parse_numbers(text: str) -> list:
    # Accept spaces and/or commas as separators
    return [int(piece) for piece in text.replace(",", " ").split()]


st.title("GCD and LCM Calculator")
st.write("Step-by-step Euclidean algorithm, back-substitution, and LCM. Works for two or more numbers.")

user_input = st.text_input(
    "Numbers (separated by spaces or commas)",
    placeholder="e.g. 252 198",
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
    if sol["lin_answer"]:
        st.success(f"Linear combination: {sol['lin_answer']}")
    st.success(sol["lcm_answer"])

    st.divider()

    # ---------- SOLUTIONS ----------
    st.subheader("GCD Solution")
    st.code(sol["gcd_steps"], language="text")
    st.info(sol["gcd_answer"])

    if sol["lin_steps"]:
        st.divider()
        st.subheader("Linear Combination Solution")
        st.code(sol["lin_steps"], language="text")
        st.info(f"Therefore: {sol['lin_answer']}")

    st.divider()
    st.subheader("LCM Solution")
    st.code(sol["lcm_steps"], language="text")
    st.info(sol["lcm_answer"])
