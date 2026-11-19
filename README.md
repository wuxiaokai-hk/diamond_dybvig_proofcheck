# diamond_dybvig_proofcheck: every result of Diamond and Dybvig (1983), checked in code

Diamond and Dybvig, "Bank Runs, Deposit Insurance, and Liquidity" (*Journal of Political Economy*, 1983) is
the standard model of why banks are fragile and why deposit insurance works. This project re-derives each
of its formal results in Python, one file per result. The files import each other in the same order that the
paper's proofs depend on each other. Each check gets an honest label: exact proof, numerical evidence only,
or not checkable by code.

**Result: no error found.** 7 of the 8 results are PROVED exactly with SymPy. The 8th, Proposition 1, is
NOT_CHECKABLE: its key step is an argument about *all possible contracts*, which code cannot enumerate.
Even there, the computable step is proved: the optimum varies with the share of impatient depositors.

| Result | Proof label |
|---|---|
| Assumption 1 (preferences) | PROVED |
| Lemma 1, eq. (1) and footnote 3: the optimum gives c1* > 1 and c2* < R | PROVED |
| Lemma 2, footnote 4: self-selection (c2* > c1*) | PROVED |
| Claim 1: the good equilibrium of the demand deposit contract | PROVED |
| Claim 2: runs are an equilibrium for any r1 > 1, and hurt everyone | PROVED |
| Claim 3: suspension of convertibility prevents runs when t is known | PROVED |
| Proposition 1: no optimal risk sharing when t is random | NOT_CHECKABLE |
| Proposition 2: deposit insurance with an optimal tax reaches the optimum | PROVED, for the reconstructed tax schedule |

Full detail is in [REPORT.md](REPORT.md), which `run_all.py` writes.

**What the checks add beyond "it's right":**
- **The assumptions are not just convenient; they are needed.** With rho = 1, the optimum gives
  c1* = 2/3 < 1 when risk aversion is 1/2, so there is no liquidity insurance to provide (Lemma 1). With
  rho = 2/5 and R = 2, c2* < c1*, so the patient type would pose as impatient (Lemma 2).
- **Suspension of convertibility** works because V2(fbar) − r1 = (R − 1) r1 (fbar_max − fbar)/(1 − fbar)
  exactly. The admissible interval is non-empty if and only if c2* ≥ c1*, which links Claim 3 directly to
  footnote 4.

## Labels

| Label | Meaning |
|---|---|
| PROVED | exact symbolic identity, or signs that follow from the stated assumptions |
| CERTIFIED | exact, via an algebraic certificate (none needed here) |
| NUMERICAL | evidence on a grid, not a proof |
| NOT_CHECKABLE | a kind of argument code cannot establish; its computable hypotheses are checked instead |
| FAILED | an exact counterexample |

A result's label is the weakest label among its steps.

## Scope and limits

- **Utility.** Closed forms use CRRA utility (relative risk aversion gamma > 1). The general-u step of
  footnote 3, d/dc[c u'(c)] = u'(c)(1 − RRA), is proved for an abstract u. `robustness_general_u.py`
  re-solves the model numerically for a non-CRRA utility with RRA between 2 and 4, and all claims hold on the
  grid. That is NUMERICAL evidence, not a proof.
- **Source text.** The scanned copy available to us garbles some formulas. The tax schedule of Proposition 2
  is checked in its standard form, as the report says. Re-check it against the published PDF before citing it.

## Run

```bash
pip install -r requirements.txt
python run_all.py                           # all results, in dependency order; writes REPORT.md
python -m results.claim_03_suspension       # one result alone
python robustness_general_u.py
```

## Layout

```
framework/status.py   labels, Step, Result
framework/checks.py   is_identity, positivity, grid_check, confirm_counterexample
model/symbols.py      every symbol once, with the paper's sign restrictions
model/primitives.py   utility, resource constraint (1c), FOC (1b), V1 (2), V2 (3)
results/              one file per result; dependencies are imports
run_all.py            topological run + REPORT.md
inventory.md          every formal result, where it is and what it uses
```

## License

MIT, see [LICENSE](LICENSE). Free to use, change and share. Data downloaded from public sources stay under their providers' terms. Independent open-source project, not affiliated with or endorsed by any employer, regulator or data vendor.
