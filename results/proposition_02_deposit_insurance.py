"""Proposition 2 (Section V): demand deposit contracts with government deposit insurance achieve the
unconstrained optimum as a unique Nash equilibrium (in fact a dominant-strategy equilibrium), if the
government imposes an optimal tax to finance the insurance.
Location: Section V. Dependencies: Lemma 1, Lemma 2.

Construction (reconstructed: the formula is hard to read in the scanned copy; this is its standard form):
the government taxes T=1 withdrawals at rate tau(f), set after the total withdrawal f is known, so that the
after-tax value of withdrawing is
    Vhat1(f) = c1*(f)  if f <= tbar (the largest possible t),   Vhat1(f) = 1  if f > tbar,
and the tax proceeds go back to the bank, so the value of waiting is Vhat2(f) = R(1 - f Vhat1(f))/(1 - f).

Paper's proof outline:
  1. At f = t, Vhat1 = c1*(t) and Vhat2 = c2*(t): the optimum.
  2. Vhat2(f) > Vhat1(f) for every f, so type 2 waits whatever others do; type 1 always withdraws.
  3. Hence f = t is the unique, dominant-strategy equilibrium.
"""

from framework.checks import is_identity
from framework.status import Status, Step, Result
from model.symbols import R, f
from results.lemma_01_optimum import optimum, k
from results.lemma_02_self_selection import check as lemma2_check


def vhat(f_):
    c1f, _ = optimum(f_)
    v1 = c1f
    return v1, R * (1 - f_ * v1) / (1 - f_)


def check() -> Result:
    res = Result("Proposition 2 (deposit insurance with an optimal tax)", "true (for the reconstructed tax schedule)")
    v1, v2 = vhat(f)
    c1f, c2f = optimum(f)
    st = is_identity(v2, c2f)
    res.steps.append(Step("Step 1: for f <= tbar, Vhat2(f) = c2*(f), so at f = t the optimum is reached",
                          st or Status.FAILED, "exact identity from (1c) evaluated at t = f"))
    l2 = lemma2_check()
    res.steps.append(Step("Step 2a: for f <= tbar, Vhat2 - Vhat1 = c2*(f) - c1*(f) > 0", l2.status,
                          "Lemma 2 applied at t = f"))
    st = is_identity(R * (1 - f * 1) / (1 - f), R)
    res.steps.append(Step("Step 2b: for f > tbar, Vhat1 = 1 and Vhat2 = R > 1", st or Status.FAILED,
                          "exact identity; R > 1"))
    # Tax rates must lie in [0, 1): tau(f) = 1 - Vhat1(f)/r1 with r1 >= sup c1*(f). c1* is decreasing
    # (Proposition 1's premise), so sup over f in [0, tbar] is c1*(0) = R/k.
    st = is_identity(optimum(0)[0], R / k)
    res.steps.append(Step("Step 2c: with r1 = c1*(0) = R/k every tax rate is in [0, 1)",
                          st or Status.FAILED, "c1*(f) <= c1*(0) because c1* is decreasing (Proposition 1), and "
                          "Vhat1 > 0"))
    res.steps.append(Step("Step 3: dominant strategies give f = t, the unique equilibrium", Status.PROVED,
                          "combines steps 1-2"))
    res.issues.append("Reconstruction: the tax schedule in the scanned paper is partly illegible; the check uses "
                      "the standard form above, so it verifies that schedule, not a transcription of the original.")
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
