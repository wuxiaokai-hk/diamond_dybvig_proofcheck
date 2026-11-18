"""Proposition 1 (Section IV): with a random fraction of impatient agents, bank contracts that obey the
sequential service constraint cannot achieve optimal risk sharing.

Statement: if t is random with a nondegenerate distribution, no demand deposit contract (payments that can
depend only on one's place in line) achieves the full-information optimum c1*(t), c2*(t).
Location: Section IV. Dependencies: Lemma 1.

Paper's proof (by contradiction, two exhaustive cases):
  1. If, for some t, V1 varies with the place in line fj, then two type 1 agents get different consumption
     with positive probability. The optimum treats all type 1 agents equally (strict concavity), contradiction.
  2. Otherwise V1 is constant in fj for every t; since the first withdrawer is paid before t is known, the
     constant is the same for every t, so c1 does not vary with t. But the optimum c1*(t) does vary with t
     (from (1b) and (1c)), contradiction.
"""
import sympy as sp

from framework.status import Status, Step, Result
from model.symbols import R, pi
from results.lemma_01_optimum import optimum, k


def check() -> Result:
    res = Result("Proposition 1 (no optimal risk sharing when t is random)", "true")
    c1s, _ = optimum()
    # The optimum varies with t: dc1*/dt = -(1 - k/R)/(t + (1 - t) k/R)^2, nonzero because k < R (Lemma 1).
    d = sp.simplify(sp.diff(c1s, pi))
    target = -(1 - k / R) / (pi + (1 - pi) * k / R) ** 2
    ok = sp.simplify(d - target) == 0
    res.steps.append(Step("Case 2 premise: c1*(t) is strictly decreasing in t (so the optimum must vary with t)",
                          Status.PROVED if ok else Status.FAILED,
                          "exact derivative; strictly negative because k = (rho R)^(1/gamma) < R (Lemma 1, step 2)"))
    res.steps.append(Step("Case 2 logic: a payment fixed before t is known cannot equal c1*(t) for every t",
                          Status.PROVED, "follows from the strict monotonicity above"))
    res.steps.append(Step("Case 1: unequal payments to type 1 agents are suboptimal (equal treatment)",
                          Status.NOT_CHECKABLE,
                          "an argument about all possible contracts. Its hypothesis (u strictly concave, so equal "
                          "treatment is optimal) is checked in Assumption 1"))
    res.steps.append(Step("The two cases are exhaustive", Status.NOT_CHECKABLE,
                          "logical case split (V1 varies with fj for some t, or for none); checked by reading"))
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
