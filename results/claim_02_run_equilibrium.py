"""Claim 2 (Section II): bank runs. For any r1 > 1 there is also an equilibrium in which everyone
withdraws at T=1 (a run); with r1 = 1 runs cannot happen, but then the bank provides no liquidity insurance.
A run leaves everyone worse off than holding the asset directly.
Location: Section II. Dependencies: Lemma 1 (r1 = c1* > 1 in the good contract).

Paper's argument:
  1. If all others withdraw (f -> 1) and r1 > 1, the bank's assets (worth 1 at T=1) run out once a fraction
     1/r1 is paid, so V2 = 0: waiting gets nothing, withdrawing gets r1 with probability 1/r1. Everyone runs.
  2. With r1 = 1, V2(f, 1) = R > 1 = V1 for every f < 1: type 2 always waits, so there is no run.
  3. In a run each agent gets r1 with probability 1/r1 and 0 otherwise: mean 1, but risky, so by strict
     concavity worse than the certain 1 of direct holding (and worse still for type 2, who could get R).
"""
import sympy as sp

from framework.checks import is_identity
from framework.status import Status, Step, Result
from model.symbols import R, r1, f
from results.lemma_01_optimum import check as lemma1_check


def check() -> Result:
    res = Result("Claim 2 (run equilibrium for r1 > 1)", "true")
    # Step 1: for f >= 1/r1 the interior expression is <= 0, so V2 = max(., 0) = 0.
    s = sp.symbols("s", nonnegative=True)                     # f = 1/r1 + s
    expr = sp.simplify((R * (1 - r1 * f)).subs(f, 1 / r1 + s))
    ok = sp.simplify(expr + R * r1 * s) == 0                  # R(1 - r1 f) = -R r1 s <= 0
    res.steps.append(Step("Step 1: V2(f, r1) = 0 whenever f >= 1/r1 (bank exhausted)",
                          Status.PROVED if ok else Status.FAILED,
                          "R(1 - r1 f) = -R r1 s <= 0 with f = 1/r1 + s; so V2 = max(., 0) = 0, and any "
                          "chance of being paid beats 0"))
    l1 = lemma1_check()
    res.steps.append(Step("r1 = c1* > 1 in the optimal contract, so the run equilibrium exists for it",
                          l1.status, "imported from Lemma 1"))
    # Step 2: r1 = 1 gives V2 = R for all f < 1.
    st = is_identity(R * (1 - 1 * f) / (1 - f), R)
    res.steps.append(Step("Step 2: with r1 = 1, V2 = R > 1 = V1 for every f < 1, so no run",
                          st or Status.FAILED, "exact identity; R > 1 by assumption"))
    # Step 3: mean consumption in a run is (1/r1) r1 = 1; strict concavity makes the lottery worse than 1.
    st = is_identity((1 / r1) * r1 + (1 - 1 / r1) * 0, 1)
    res.steps.append(Step("Step 3a: expected consumption in a run equals 1", st or Status.FAILED, "exact"))
    res.steps.append(Step("Step 3b: a nondegenerate lottery with mean 1 is worse than 1 for strictly concave u",
                          Status.PROVED, "this is the definition of strict concavity (Assumption 1): "
                          "lambda u(r1) + (1 - lambda) u(0) < u(lambda r1) with lambda = 1/r1 in (0,1)"))
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
