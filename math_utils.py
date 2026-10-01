"""Core number-theory helpers: GCD, extended GCD, and Euclidean division steps."""


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
