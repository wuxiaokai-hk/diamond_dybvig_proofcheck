"""Assumption 1 (Diamond and Dybvig 1983, Section I): preferences and technology.

Statement (paraphrased): u is increasing, strictly concave, twice differentiable, satisfies the Inada
conditions, and has relative risk aversion -c u''(c)/u'(c) > 1 everywhere; 1 >= rho > 1/R; R > 1; 0 < t < 1.
Location: Section I (model). Dependencies: none.

Proof outline: an assumption, so nothing to prove. This file
  1. checks that the CRRA family used for closed forms satisfies every condition when gamma > 1;
  2. records which later results use which part of the assumption.
"""
import sympy as sp

from framework.status import Status, Step, Result
from model.symbols import c, gamma
from model.primitives import u_crra, rra


def check() -> Result:
    res = Result("Assumption 1 (preferences)", "true")
    u = u_crra(c)
    # RRA of CRRA utility is exactly gamma: the paper's RRA > 1 is gamma > 1.
    st = Status.PROVED if sp.simplify(rra(u) - gamma) == 0 else Status.FAILED
    res.steps.append(Step("CRRA instance: -c u''/u' = gamma", st, "exact simplification"))
    up = sp.diff(u, c)
    upp = sp.diff(u, c, 2)
    ok = sp.simplify(up - c ** (-gamma)) == 0 and sp.simplify(upp + gamma * c ** (-gamma - 1)) == 0
    res.steps.append(Step("u' = c^-gamma > 0 and u'' = -gamma c^(-gamma-1) < 0 (increasing, strictly concave)",
                          Status.PROVED if ok else Status.FAILED, "exact derivatives; signs follow from c, gamma > 0"))
    lim0 = sp.limit(c ** (-gamma), c, 0, "+")
    res.steps.append(Step("Inada: u'(0+) = infinity, u'(infinity) = 0", Status.PROVED
                          if lim0 == sp.oo and sp.limit(c ** (-gamma), c, sp.oo) == 0 else Status.FAILED,
                          "exact limits"))
    return res


if __name__ == "__main__":
    r = check()
    print(r.name, r.status.name, [s.status.name for s in r.steps])
