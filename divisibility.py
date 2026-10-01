"""Divisibility and the Division Algorithm for integers (step-by-step)."""
from formatting import paren


def division_algorithm(a: int, d: int) -> tuple:
    """Returns (q, r) with a = q(d) + r and 0 <= r < |d|. Works for negative a and d."""
    r = a % abs(d)       # Python's % with a positive modulus is already in [0, |d|)
    q = (a - r) // d     # exact division
    return q, r


def division_lines(a: int, d: int) -> tuple:
    """Step-by-step lines for a divided by d. Returns (lines, q, r)."""
    q, r = division_algorithm(a, d)
    ad = abs(d)
    k = a // ad  # largest k with k|d| <= a

    lines = [
        "Division Algorithm: for integers a and d (d != 0) there are unique",
        "integers q and r such that a = q(d) + r, where 0 <= r < |d|.",
        "",
        f"a = {a}, d = {d}, |d| = {ad}",
        f"So 0 <= r < {ad}.",
        "",
        f"Find the largest multiple of {ad} that is not greater than {a}:",
        f"{paren(k)}({ad}) = {k * ad} <= {a} < {k * ad + ad} = {paren(k + 1)}({ad})",
        "",
        f"r = {a} - {paren(k)}({ad}) = {r}",
    ]

    if d > 0:
        lines.append(f"q = {k}")
    else:
        lines.append(f"d is negative, so q = -({paren(k)}) = {q}")
        lines.append(f"because {paren(k)}({ad}) = {paren(q)}({d})")

    lines += [
        "",
        f"{a} = {paren(q)}({d}) + {r}",
        "",
        "Check:",
        f"{paren(q)}({d}) + {r} = {q * d} + {r} = {q * d + r}",
        f"0 <= {r} < {ad}",
    ]
    return lines, q, r


def build_division(a: int, d: int) -> dict:
    """
    Returns a dict with:
      steps, answer,              (division algorithm)
      divis_steps, divis_answer   (does d divide a?)
    """
    lines, q, r = division_lines(a, d)

    if r == 0:
        divis_lines = [
            f"The remainder is r = 0, so {d} divides {a}.",
            f"{a} = {paren(q)}({d})",
            f"Therefore {d} | {a}  ({a} is a multiple of {d}).",
        ]
        divis_answer = f"{d} | {a}  (q = {q})"
    else:
        divis_lines = [
            f"The remainder is r = {r} != 0, so {d} does not divide {a}.",
            f"Therefore {d} does not divide {a}.",
        ]
        divis_answer = f"{d} does not divide {a}"

    return {
        "steps": "\n".join(lines),
        "answer": f"{a} = {paren(q)}({d}) + {r}   (q = {q}, r = {r})",
        "divis_steps": "\n".join(divis_lines),
        "divis_answer": divis_answer,
    }


def build_set_division(numbers: list, d: int) -> dict:
    """
    Divides every integer in `numbers` by the same divisor d.
    Returns a dict with: steps, answer, divisible, not_divisible.
    """
    lines = [f"Divisor d = {d}, |d| = {abs(d)}, so 0 <= r < {abs(d)}", ""]
    divisible, not_divisible = [], []

    for a in numbers:
        q, r = division_algorithm(a, d)
        verdict = f"{d} | {a}" if r == 0 else f"{d} does not divide {a}"
        lines.append(f"{a} = {paren(q)}({d}) + {r}   ->  {verdict}")
        (divisible if r == 0 else not_divisible).append(a)

    joined = ", ".join(map(str, numbers))
    div_txt = ", ".join(map(str, divisible)) if divisible else "none"
    not_txt = ", ".join(map(str, not_divisible)) if not_divisible else "none"

    return {
        "steps": "\n".join(lines),
        "answer": f"Divisible by {d} in {{{joined}}}: {{{div_txt}}}",
        "divisible": divisible,
        "not_divisible": not_divisible,
        "not_answer": f"Not divisible by {d}: {{{not_txt}}}",
    }


def build_divisors(n: int) -> dict:
    """All integer divisors of n (n != 0), found by testing 1..sqrt(|n|)."""
    m = abs(n)
    lines, small, large = [], [], []
    i = 1
    while i * i <= m:
        q, r = division_algorithm(m, i)
        if r == 0:
            lines.append(f"{m} = {q}({i}) + 0  ->  {i} | {m}")
            small.append(i)
            if q != i:
                large.append(q)
        else:
            lines.append(f"{m} = {q}({i}) + {r}")
        i += 1

    positive = small + large[::-1]
    all_divs = sorted([-p for p in positive] + positive)
    return {
        "steps": "\n".join(lines),
        "answer": f"Positive divisors of {m}: {', '.join(map(str, positive))}",
        "all_answer": f"All divisors of {n}: {', '.join(map(str, all_divs))}",
    }
