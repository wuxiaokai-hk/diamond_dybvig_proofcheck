"""Shared checking helpers. Exact first (identity, factor signs), numerical only as a fallback."""
import itertools
from fractions import Fraction

import mpmath as mp
import sympy as sp

from .status import Status

mp.mp.dps = 40


def is_identity(lhs, rhs):
    """PROVED if lhs - rhs simplifies to exactly zero, else None."""
    d = sp.simplify(sp.expand(sp.cancel(lhs - rhs)))
    return Status.PROVED if d == 0 else None


def positive_under_assumptions(expr):
    """PROVED if SymPy can show expr > 0 from the symbols' declared assumptions (factor by factor)."""
    e = sp.factor(sp.simplify(expr))
    if e.is_positive:
        return Status.PROVED
    num, den = sp.fraction(sp.together(e))
    facs = list(sp.Mul.make_args(sp.factor(num))) + list(sp.Mul.make_args(sp.factor(den)))
    if all(f.is_positive for f in facs):
        return Status.PROVED
    return None


def grid_check(fn, region, n=12, strict=True):
    """Evaluate fn(**point) on an n-point-per-axis grid over region {name: (lo, hi)} with mpmath.

    Returns (Status.NUMERICAL, min_value, argmin) if fn > 0 (or >= 0) everywhere, else
    (None, min_value, argmin) so the caller can try to confirm a counterexample exactly.
    """
    names = list(region)
    axes = [[mp.mpf(lo) + (mp.mpf(hi) - mp.mpf(lo)) * (i + 0.5) / n for i in range(n)]
            for lo, hi in region.values()]
    best, arg = None, None
    for pt in itertools.product(*axes):
        v = fn(**dict(zip(names, pt)))
        if best is None or v < best:
            best, arg = v, dict(zip(names, pt))
    ok = best > 0 if strict else best >= 0
    return (Status.NUMERICAL if ok else None), best, arg


def confirm_counterexample(expr, point, symbols):
    """Snap a numeric point to nearby rationals and substitute exactly. FAILED only if the claim
    (expr > 0) is violated exactly at that rational point."""
    exact = {symbols[k]: sp.Rational(Fraction(str(float(v))).limit_denominator(1000)) for k, v in point.items()}
    val = sp.nsimplify(expr.subs(exact))
    return (Status.FAILED, exact, val) if val <= 0 else (None, exact, val)
