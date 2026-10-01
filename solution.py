"""Builds the complete GCD / linear combination / coefficients / LCM solution."""
from math_utils import gcd_manual
from formatting import full_sum, paren, var_names
from solvers import division_lines, back_substitution_lines, multi_combination


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
