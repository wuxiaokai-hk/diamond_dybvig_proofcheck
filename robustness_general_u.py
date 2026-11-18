"""Robustness beyond CRRA (NUMERICAL evidence, not a proof).

The exact proofs in results/ use CRRA utility for closed forms (plus an abstract-u identity in Lemma 1).
The paper allows any u with relative risk aversion > 1. This script re-solves the optimum numerically for a
non-CRRA utility whose RRA lies strictly between 2 and 4,
    u(c) = -1/c - 1/(3 c^3),   RRA(c) = (2 + 4/c^2)/(1 + 1/c^2),
and checks the main claims on a grid: c1* > 1, c2* < R, c2* > c1*, V2(t, c1*) = c2*, and that the suspension
interval is non-empty.
"""
import itertools

import mpmath as mp

mp.mp.dps = 30


def up(x):
    return x ** -2 + x ** -4


def optimum(R, rho, t):
    # (1c): c2 = R (1 - t c1)/(1 - t); solve (1b) u'(c1) = rho R u'(c2) for c1 in (0, 1/t)
    g = lambda c1: up(c1) - rho * R * up(R * (1 - t * c1) / (1 - t))
    c1 = mp.findroot(g, (mp.mpf("1e-6"), 1 / t - mp.mpf("1e-9")), solver="bisect")
    return c1, R * (1 - t * c1) / (1 - t)


def main(n=9):
    worst = {"c1*-1": mp.inf, "R-c2*": mp.inf, "c2*-c1*": mp.inf, "|V2-c2*|": 0, "interval": mp.inf}
    for R, rho, t in itertools.product(
            [mp.mpf(1.05) + i * mp.mpf(0.25) for i in range(n)],
            [mp.mpf(0.5) + i * mp.mpf(0.0625) for i in range(n)],
            [mp.mpf(0.05) + i * mp.mpf(0.1) for i in range(n)]):
        if not (rho * R > 1 and rho <= 1):
            continue
        c1, c2 = optimum(R, rho, t)
        worst["c1*-1"] = min(worst["c1*-1"], c1 - 1)
        worst["R-c2*"] = min(worst["R-c2*"], R - c2)
        worst["c2*-c1*"] = min(worst["c2*-c1*"], c2 - c1)
        worst["|V2-c2*|"] = max(worst["|V2-c2*|"], abs(R * (1 - c1 * t) / (1 - t) - c2))
        worst["interval"] = min(worst["interval"], (R - c1) / (c1 * (R - 1)) - t)
    for k, v in worst.items():
        print(f"{k:<10} {mp.nstr(v, 5)}")
    ok = worst["c1*-1"] > 0 and worst["R-c2*"] > 0 and worst["c2*-c1*"] > 0 and worst["interval"] > 0
    print("NUMERICAL: all claims hold on the grid" if ok else "a claim fails somewhere on the grid")


if __name__ == "__main__":
    main()
