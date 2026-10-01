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


def ext_gcd(a: int, b: int) -> tuple:
    """Returns (g, u, v) with g = a(u) + b(v), for non-negative a and b."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


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


def paren(n: int) -> str:
    """Wraps negative numbers in parentheses so signs never collide."""
    return f"({n})" if n < 0 else str(n)


def full_sum(values: list, coefs: list) -> str:
    """Shows every term, even zero coefficients: 4312(22) + 2205(-43)"""
    return " + ".join(f"{paren(v)}({c})" for v, c in zip(values, coefs))


SUBSCRIPT = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def var_names(count: int) -> list:
    """x, y for two numbers. x₁, x₂, x₃, ... for more."""
    if count == 2:
        return ["x", "y"]
    return [f"x{str(i + 1).translate(SUBSCRIPT)}" for i in range(count)]


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


def multi_combination(values: list, final_gcd: int) -> tuple:
    """
    Linear combination for 3 or more numbers, built pair by pair.
    Works on absolute values, then flips signs for negative inputs.
    Returns (lines, coefs) where coefs match `values` in the typed order.
    """
    absvals = [abs(v) for v in values]
    lines = []

    running = absvals[0]
    coefs = [1]  # running = absvals[0](1)

    for i in range(1, len(absvals)):
        m = absvals[i]
        g_new, u, v = ext_gcd(running, m)  # g_new = running(u) + m(v)
        prev_expr = full_sum(absvals[:i], coefs)

        lines.append(f"Step {i}: GCD({running}, {m}) = {g_new}")
        lines.append(f"{g_new} = {running}({u}) + {m}({v})")
        if i == 1:
            coefs = [u, v]
            running = g_new
            continue
        if i > 1:
            lines.append(f"where {running} = {prev_expr}")
            sub = fmt_expr([(u, " + ".join(f"{a}({c})" for a, c in zip(absvals[:i], coefs)), True),
                            (v, str(m), False)])
            lines.append(f"{g_new} = {sub}")

        coefs = [c * u for c in coefs] + [v]
        lines.append(f"{g_new} = {full_sum(absvals[:i + 1], coefs)}")
        lines.append("")
        running = g_new

    if lines and lines[-1] == "":
        lines.pop()

    # flip signs for negative inputs so the result works with the typed numbers
    signs = [1 if v > 0 else -1 for v in values]
    final_coefs = [c * s for c, s in zip(coefs, signs)]
    return lines, final_coefs


def build_solution(numbers: list) -> dict:
    """
    Returns a dict with:
      gcd_steps, gcd_answer,
      lin_steps, lin_answer,
      xy_steps, xy_answer,
      lcm_steps, lcm_answer
    """
    nums = [abs(n) for n in numbers]  # work with absolute values
    ordered = sorted(nums, reverse=True)  # highest number first
    count = len(nums)
    joined = ", ".join(map(str, numbers))
    has_negative = any(n < 0 for n in numbers)

    result = {
        "gcd_steps": "",
        "gcd_answer": "",
        "lin_steps": None,
        "lin_answer": None,
        "xy_steps": None,
        "xy_answer": None,
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

    # ---------------- Linear combination ----------------
    if count == 2:
        bs_lines, bx, by = back_substitution_lines(big, small)  # g = big(bx) + small(by)

        # map back to the order the user typed (ties: first typed number is "big")
        if nums[0] >= nums[1]:
            c_abs = [bx, by]
        else:
            c_abs = [by, bx]
        coefs = [c_abs[0] * (1 if numbers[0] > 0 else -1),
                 c_abs[1] * (1 if numbers[1] > 0 else -1)]
        lin_lines = list(bs_lines)
    else:
        lin_lines, coefs = multi_combination(numbers, final_gcd)

    # sign note for negative inputs
    if has_negative:
        lin_lines += ["", "Negative input: the steps above use absolute values.",
                      "Flip the sign of the coefficient for each negative number."]

    result["lin_steps"] = "\n".join(lin_lines)
    result["lin_answer"] = f"{final_gcd} = {full_sum(numbers, coefs)}"

    # ---------------- Finding x, y (z, ...) ----------------
    names = var_names(count)
    label = " + ".join(f"{paren(v)}{n}" for v, n in zip(numbers, names))
    products = [v * c for v, c in zip(numbers, coefs)]
    check_terms = " + ".join(f"{paren(v)}({c})" for v, c in zip(numbers, coefs))
    check_sum = " + ".join(paren(p) for p in products)

    xy_lines = [f"{final_gcd} = {label}", ""]
    for n, c in zip(names, coefs):
        xy_lines.append(f"{n} = {c}")
    xy_lines += ["", "Check:", f"{check_terms} = {check_sum} = {sum(products)}"]
    result["xy_steps"] = "\n".join(xy_lines)
    result["xy_answer"] = ",  ".join(f"{n} = {c}" for n, c in zip(names, coefs))

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
