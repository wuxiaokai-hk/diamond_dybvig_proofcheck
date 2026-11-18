"""Building blocks of the model, defined once and imported by every result file."""
import sympy as sp

from .symbols import R, rho, pi, gamma, c

u_general = sp.Function("u")          # abstract utility for the general-u steps


def u_crra(x, g=gamma):
    """CRRA utility x^(1-g)/(1-g): relative risk aversion is exactly g (the paper needs g > 1)."""
    return x ** (1 - g) / (1 - g)


def u_prime(x, g=gamma):
    return x ** (-g)


def rra(u_expr, x=c):
    """Relative risk aversion -x u''(x) / u'(x)."""
    return sp.simplify(-x * sp.diff(u_expr, x, 2) / sp.diff(u_expr, x))


def resource_constraint(c1_, c2_, pi_=pi):
    """Eq. (1c): pi*c1 + (1 - pi)*c2/R = 1  (returns the left side minus one)."""
    return pi_ * c1_ + (1 - pi_) * c2_ / R - 1


def foc(c1_, c2_, g=gamma):
    """Eq. (1b): u'(c1) = rho R u'(c2)  (returns the left side minus the right side)."""
    return u_prime(c1_, g) - rho * R * u_prime(c2_, g)


def V1(fj_, r1_):
    """Eq. (2): payment per unit withdrawn at T=1 under sequential service: r1 while assets last."""
    return sp.Piecewise((r1_, fj_ < 1 / r1_), (0, True))


def V2(f_, r1_):
    """Eq. (3): payment per unit left in the bank until T=2."""
    return sp.Max(R * (1 - r1_ * f_) / (1 - f_), 0)


def V2_interior(f_, r1_):
    """V2 where the bank is solvent (r1 f < 1): R(1 - r1 f)/(1 - f)."""
    return R * (1 - r1_ * f_) / (1 - f_)
