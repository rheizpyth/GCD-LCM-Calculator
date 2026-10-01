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
