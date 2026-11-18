"""Claim 1 (Section II): a demand deposit contract with r1 = c1* implements the optimum as an equilibrium.

Statement: with r1 = c1*, if type 1 agents withdraw at T=1 and type 2 agents wait (f = t), then
V1 = c1* and V2(t, c1*) = c2*, and no agent wants to deviate. The bank stays solvent.
Location: Section II, after eqs. (2) and (3). Dependencies: Lemma 1, Lemma 2.

Paper's proof outline:
  1. At f = t, V2(t, r1) = R(1 - r1 t)/(1 - t); with r1 = c1* this equals c2* by (1c).
  2. The bank pays r1 t < 1 at T=1, so it is solvent and every withdrawer is paid (V1 = r1).
  3. Type 2 compares V2 = c2* with r1 = c1* (withdraw and store): c2* >= c1* (Lemma 2), so it waits.
"""
from framework.checks import is_identity
from framework.status import Status, Step, Result
from model.symbols import R, pi
from model.primitives import V2_interior
from results.lemma_01_optimum import optimum
from results.lemma_02_self_selection import check as lemma2_check


def check() -> Result:
    res = Result("Claim 1 (good equilibrium of the demand deposit contract)", "true")
    c1s, c2s = optimum()
    st = is_identity(V2_interior(pi, c1s), c2s)
    res.steps.append(Step("Step 1: V2(t, c1*) = c2*", st or Status.FAILED, "exact identity using (1c)"))
    st = is_identity(1 - pi * c1s, (1 - pi) * c2s / R)
    res.steps.append(Step("Step 2: 1 - t c1* = (1 - t) c2*/R > 0, so the bank is solvent at f = t",
                          st or Status.FAILED, "exact identity; positivity because c2*, R > 0 and t < 1"))
    l2 = lemma2_check()
    res.steps.append(Step("Step 3: type 2 waits because c2* > c1* (Lemma 2)", l2.status, "imported from Lemma 2"))
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
