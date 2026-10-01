"""Step-by-step solvers. Each returns text lines plus any numeric results."""
from math_utils import euclid_steps, ext_gcd
from formatting import fmt_expr, full_sum


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
