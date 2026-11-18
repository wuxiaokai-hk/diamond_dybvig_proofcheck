"""Every symbol of Diamond and Dybvig (1983), declared once, with the paper's sign restrictions.

    R      gross return at T=2 on one unit invested at T=0 (liquidated at T=1 it returns 1), R > 1
    rho    type 2's discount factor, 1 >= rho > 1/R
    pi     fraction of type 1 (impatient) agents, 0 < pi < 1   (the paper's t)
    gamma  relative risk aversion of the CRRA instance used for closed forms; the paper needs RRA > 1
    c1, c2 consumption of type 1 at T=1 and type 2 at T=2
    r1     payment promised per unit withdrawn at T=1
    f      fraction of deposits withdrawn at T=1;  fj  fraction withdrawn before agent j
"""
import sympy as sp

R = sp.symbols("R", positive=True)
rho = sp.symbols("rho", positive=True)
pi = sp.symbols("pi", positive=True)
gamma = sp.symbols("gamma", positive=True)
c, c1, c2, r1, f, fj = sp.symbols("c c1 c2 r1 f fj", positive=True)

# Region used for numerical checks (the paper's assumptions, with gamma > 1 for RRA > 1)
REGION = {"R": (1.01, 3.0), "rho": (0.40, 1.0), "pi": (0.05, 0.95), "gamma": (1.01, 8.0)}


def in_region(R_, rho_, pi_, gamma_):
    """The paper's parameter restrictions: R > 1, 1 >= rho > 1/R, 0 < pi < 1, RRA > 1."""
    return R_ > 1 and 1 >= rho_ > 1 / R_ and 0 < pi_ < 1 and gamma_ > 1
