"""Claim 3 (Section III): suspension of convertibility prevents runs when t is known.

Statement: if the bank sets r1 = c1* and suspends withdrawals once a fraction fbar of deposits has been
withdrawn, with t <= fbar <= (R - r1)/(r1 (R - 1)), then type 2 agents never withdraw, whatever others do,
so the optimum is the unique (dominant-strategy) equilibrium.
Location: Section III. Dependencies: Lemma 1, Lemma 2.

Paper's argument:
  1. With suspension at fbar, at most fbar is paid out at T=1, so V2 >= V2(fbar, r1) for every f.
  2. V2(fbar, r1) >= r1  <=>  fbar <= (R - r1)/(r1 (R - 1)), so waiting dominates for type 2.
  3. The interval [t, (R - r1)/(r1 (R - 1))] is non-empty when r1 = c1*.
"""
import sympy as sp

from framework.checks import is_identity
from framework.status import Status, Step, Result
from model.symbols import R, pi, r1, f
from model.primitives import V2_interior
from results.lemma_01_optimum import optimum
from results.lemma_02_self_selection import check as lemma2_check


def fbar_max(r1_=r1):
    return (R - r1_) / (r1_ * (R - 1))


def check() -> Result:
    res = Result("Claim 3 (suspension of convertibility)", "true")
    # Step 1: V2 is decreasing in f when r1 > 1: dV2/df = R (1 - r1)/(1 - f)^2.
    st = is_identity(sp.diff(V2_interior(f, r1), f), R * (1 - r1) / (1 - f) ** 2)
    res.steps.append(Step("Step 1: dV2/df = R(1 - r1)/(1 - f)^2 < 0 for r1 > 1, so the worst case is f = fbar",
                          st or Status.FAILED, "exact derivative; sign from R > 0, r1 > 1"))
    # Step 2: V2(fbar) - r1 = (R - 1) r1 (fbar_max - fbar)/(1 - fbar): same sign as fbar_max - fbar.
    fb = sp.symbols("fbar", positive=True)
    st = is_identity(V2_interior(fb, r1) - r1, (R - 1) * r1 * (fbar_max() - fb) / (1 - fb))
    res.steps.append(Step("Step 2: V2(fbar, r1) >= r1 exactly when fbar <= (R - r1)/(r1(R - 1))",
                          st or Status.FAILED, "exact factorization; (R - 1) r1/(1 - fbar) > 0"))
    # Step 3: non-empty interval with r1 = c1*:  fbar_max(c1*) - t = (c2* - c1*)(1 - t)/(c1* (R - 1)).
    c1s, c2s = optimum()
    st = is_identity(fbar_max(c1s) - pi, (c2s - c1s) * (1 - pi) / (c1s * (R - 1)))
    l2 = lemma2_check()
    res.steps.append(Step("Step 3: (R - c1*)/(c1*(R - 1)) - t = (c2* - c1*)(1 - t)/(c1*(R - 1)) >= 0",
                          min(st or Status.FAILED, l2.status), "exact identity; sign from Lemma 2 (c2* > c1*)"))
    res.issues.append("Scope (as the paper says): this works only because t is known; Proposition 1 shows why "
                      "it fails when t is random.")
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
