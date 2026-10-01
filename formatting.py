"""Text-formatting helpers used when writing out the step-by-step solutions."""


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
