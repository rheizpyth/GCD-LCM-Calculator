import streamlit as st


# =====================================================================
# MANUAL HELPERS (no math library)
# =====================================================================
def gcd_manual(a: int, b: int) -> int:
    """Plain Euclidean loop, used for quiet calculations."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def lcm_manual(a: int, b: int) -> int:
    """LCM of two numbers using the GCD."""
    a, b = abs(a), abs(b)
    return (a * b) // gcd_manual(a, b)


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
    """Lines for the Euclidean divisions. Returns (lines, steps, gcd)."""
    steps = euclid_steps(big, small)
    lines = [f"{a} = {q}({b}) + {r}" for a, b, q, r in steps]
    g = steps[-1][1]  # divisor of the last division (remainder is 0)
    return lines, steps, g


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

        i -= 1

    return lines, x, y


def build_solution(numbers: list) -> str:
    nums = [abs(n) for n in numbers]  # work with absolute values
    count = len(nums)
    lines = []

    # ---------------- GCD ----------------
    lines.append("GCD Solution:")
    lines.append("")

    if count == 2:
        big, small = max(nums), min(nums)
        div_lines, steps, final_gcd = division_lines(big, small)
        lines += div_lines
        lines.append("")
        lines.append(f"Therefore, GCD({numbers[0]}, {numbers[1]}) = {final_gcd}")
    else:
        running = nums[0]
        for idx in range(1, count):
            nxt = nums[idx]
            big, small = max(running, nxt), min(running, nxt)
            lines.append(f"--- Step {idx}: Finding GCD({running}, {nxt}) ---")
            div_lines, steps, g = division_lines(big, small)
            lines += div_lines
            lines.append(f"Sub-GCD: GCD({running}, {nxt}) = {g}")
            lines.append("")
            running = g
        final_gcd = running
        lines.append(f"Therefore, GCD({', '.join(map(str, numbers))}) = {final_gcd}")

    lines.append("")

    # ---------------- Linear combination (2 numbers only) ----------------
    if count == 2:
        big, small = max(nums), min(nums)
        lines.append("Linear Combination Solution:")
        lines.append("")
        bs_lines, x, y = back_substitution_lines(big, small)
        lines += bs_lines
        lines.append("")
        lines.append("Therefore:")
        lines.append(f"{final_gcd} = {big}({x}) + {small}({y})")
        lines.append("")

    # ---------------- LCM ----------------
    lines.append("LCM Solution:")
    lines.append("")

    if count == 2:
        final_lcm = (nums[0] * nums[1]) // final_gcd
        lines.append(f"LCM({numbers[0]}, {numbers[1]}) = ({nums[0]} * {nums[1]}) / {final_gcd} = {final_lcm}")
    else:
        final_lcm = nums[0]
        for idx in range(1, count):
            nxt = nums[idx]
            g = gcd_manual(final_lcm, nxt)
            new_lcm = (final_lcm * nxt) // g
            lines.append(f"Step {idx}: LCM({final_lcm}, {nxt}) = ({final_lcm} * {nxt}) / {g} = {new_lcm}")
            final_lcm = new_lcm

    lines.append("")
    lines.append(f"The overall LCM is: {final_lcm}")

    # ---------------- Self-check (manual, no math library) ----------------
    gcd_ok = all(n % final_gcd == 0 for n in nums)
    lcm_ok = all(final_lcm % n == 0 for n in nums)
    if not (gcd_ok and lcm_ok):
        raise ValueError("Self-check failed: result does not divide/contain every number.")

    return "\n".join(lines)


# =====================================================================
# STREAMLIT UI (basic)
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

    try:
        result = build_solution(values)
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.stop()

    st.subheader("Result")
    st.code(result, language="text")
