"""Lemma 2 (footnote 4): the optimum satisfies self-selection, so it can be implemented.

Statement: at the optimum, c2* >= c1*, so a type 2 agent does not want to pose as type 1 (withdraw at T=1
and store), and a type 1 agent does not want to wait. Hence the optimum is incentive compatible.
Location: Section I, footnote 4. Dependencies: Lemma 1 (the optimum).

Paper's proof outline:
  1. From (1b), u'(c1*)/u'(c2*) = rho R > 1 (because rho > 1/R), and u' is decreasing, so c2* > c1*.
  2. Type 1 values only T=1 consumption, so waiting gives it nothing: it withdraws.
"""
import sympy as sp

from framework.checks import is_identity
from framework.status import Status, Step, Result
from model.symbols import R, rho, pi, gamma
from results.lemma_01_optimum import optimum, k


def check() -> Result:
    res = Result("Lemma 2 (footnote 4: self-selection)", "true")
    c1s, c2s = optimum()
    st = is_identity(c2s / c1s, k)
    res.steps.append(Step("c2*/c1* = (rho R)^(1/gamma)", st or Status.FAILED, "exact, from the closed form"))
    # c2* > c1*  <=>  ln(rho R)/gamma > 0  <=>  rho R > 1. With rho R = 1 + e (e > 0):
    e = sp.symbols("e", positive=True)
    m = sp.log(1 + e) / gamma
    res.steps.append(Step("Step 1: c2* > c1* because rho R > 1", Status.PROVED if m.is_positive else Status.NUMERICAL,
                          "ln(rho R)/gamma > 0 exactly when rho R > 1 (the paper's rho > 1/R); if rho R < 1 the "
                          "inequality reverses"))
    res.steps.append(Step("Step 2: type 1 withdraws (it values only T=1 consumption)", Status.PROVED,
                          "follows from the preferences in Assumption 1"))
    # Scope: show the assumption rho > 1/R is needed.
    v = (c2s - c1s).subs({R: 2, rho: sp.Rational(2, 5), pi: sp.Rational(1, 2), gamma: 2})
    res.issues.append(f"Scope (not an error): the paper's rho > 1/R is needed. With R = 2, rho = 2/5, gamma = 2, "
                      f"t = 1/2, c2* - c1* = {sp.nsimplify(sp.simplify(v))} < 0, so type 2 would mimic type 1.")
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
