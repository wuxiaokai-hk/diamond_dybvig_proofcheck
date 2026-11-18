"""Lemma 1 (eq. 1 and footnote 3): the full-information optimum and why it insures against liquidity risk.

Statement: the optimal consumptions c1* (type 1, at T=1) and c2* (type 2, at T=2) satisfy
  (1a) each type consumes only in the period it values,
  (1b) u'(c1*) = rho R u'(c2*),
  (1c) t c1* + (1 - t) c2*/R = 1,
and (footnote 3) rho R u'(R) < u'(1), which implies c1* > 1 and c2* < R: the optimum gives type 1 more than the
liquidation value and type 2 less than the full return, i.e. it insures against being impatient.
Location: Section I, eq. (1a)-(1c) and footnote 3. Dependencies: Assumption 1.

Paper's proof outline (footnote 3):
  1. RRA > 1 means c u'(c) is strictly decreasing, so R u'(R) < 1 u'(1); with rho <= 1, rho R u'(R) < u'(1).
  2. If c1* <= 1 then by (1c) c2* >= R, so u'(c1*) >= u'(1) > rho R u'(R) >= rho R u'(c2*), contradicting (1b).
     Hence c1* > 1, and then (1c) gives c2* < R.
"""
import sympy as sp

from framework.checks import is_identity, grid_check
from framework.status import Status, Step, Result
from model.symbols import R, rho, pi, gamma, c, REGION
from model.primitives import u_general, resource_constraint, foc

# Closed form for CRRA: (1b) gives c2/c1 = (rho R)^(1/gamma) =: k; (1c) then pins c1.
k = (rho * R) ** (1 / gamma)


def optimum(pi_=pi):
    """(c1*, c2*) for CRRA utility, as SymPy expressions in R, rho, gamma and pi_."""
    c1s = 1 / (pi_ + (1 - pi_) * k / R)
    return c1s, k * c1s


def check() -> Result:
    res = Result("Lemma 1 (eq. 1, footnote 3: the optimum)", "true")
    c1s, c2s = optimum()

    # Step 0: the closed form solves (1b) and (1c) exactly.
    ok = is_identity(resource_constraint(c1s, c2s), 0) and \
        is_identity(sp.simplify(foc(c1s, c2s) / c1s ** (-gamma)), 0)
    res.steps.append(Step("Closed form (CRRA) solves (1b) and (1c)", ok or Status.FAILED, "exact substitution"))

    # Step 1 (general u): d/dc [c u'(c)] = u'(c) (1 - RRA(c)); negative when u' > 0 and RRA > 1.
    u = u_general
    lhs = sp.diff(c * sp.diff(u(c), c), c)
    rra_c = -c * sp.diff(u(c), c, 2) / sp.diff(u(c), c)
    st = is_identity(lhs, sp.diff(u(c), c) * (1 - rra_c))
    res.steps.append(Step("Footnote 3, step 1: d/dc[c u'(c)] = u'(c)(1 - RRA) < 0, so R u'(R) < u'(1) "
                          "and rho R u'(R) < u'(1)", st or Status.FAILED,
                          "exact identity for an abstract u; the sign uses u' > 0, RRA > 1, R > 1 and rho <= 1 "
                          "(all assumed)"))

    # Step 2 (CRRA, exact): c1* > 1  <=>  k < R  <=>  ((gamma-1) ln R - ln rho)/gamma > 0.
    # Substitute gamma = 1 + a, R = 1 + b, rho = exp(-d) with a, b > 0 and d >= 0.
    a, b = sp.symbols("a b", positive=True)
    d = sp.symbols("d", nonnegative=True)
    margin = ((gamma - 1) * sp.log(R) - sp.log(rho)) / gamma
    m = sp.simplify(margin.subs({gamma: 1 + a, R: 1 + b, rho: sp.exp(-d)}))
    st = Status.PROVED if m.is_positive else None
    res.steps.append(Step("Footnote 3, step 2: c1* > 1 (equivalently (rho R)^(1/gamma) < R)",
                          st or Status.NUMERICAL,
                          f"log margin = {m} > 0 for a, b > 0, d >= 0 (gamma = 1 + a, R = 1 + b, rho = e^-d)"))

    # Step 3: given c1* > 1, (1c) gives c2* = R (1 - t c1*)/(1 - t) < R.
    st = is_identity(c2s, R * (1 - pi * c1s) / (1 - pi))
    res.steps.append(Step("c2* = R(1 - t c1*)/(1 - t), hence c2* < R exactly when c1* > 1", st or Status.FAILED,
                          "exact identity from (1c)"))

    # Direct check of the statement on the paper's region (independent of the proof route).
    f1 = sp.lambdify((R, rho, pi, gamma), c1s - 1, "mpmath")
    s, mn, at = grid_check(lambda R, rho, pi, gamma: f1(R, rho, pi, gamma) if rho > 1 / R else 1, REGION, n=10)
    res.steps.append(Step("Direct: c1* - 1 > 0 on the paper's region", Status.PROVED if res.steps[2].status ==
                          Status.PROVED else (s or Status.FAILED),
                          f"also sampled 10^4 points: minimum margin {float(mn):.3g} (exact proof above)"))

    # Why RRA > 1 is needed: with gamma < 1, c1* < 1 (no insurance). Not an error, a scope note.
    val = c1s.subs({R: 2, rho: 1, pi: sp.Rational(1, 2), gamma: sp.Rational(1, 2)})
    res.issues.append(f"Scope (not an error): when rho = 1, RRA > 1 is necessary as well as sufficient for c1* > 1 "
                      f"in the CRRA family. With gamma = 1/2, R = 2, rho = 1, t = 1/2 the optimum gives c1* = {sp.nsimplify(val)} < 1.")
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name)
    for s in r.steps:
        print(" ", s.status.name, s.label, "|", s.note)
