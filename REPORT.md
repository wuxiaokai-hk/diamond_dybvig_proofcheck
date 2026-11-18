# REPORT: Diamond and Dybvig (1983), checked result by result

| Result | Statement | Proof label | Main issue |
|---|---|---|---|
| Assumption 1 (preferences) | true | PROVED |  |
| Lemma 1 (eq. 1, footnote 3: the optimum) | true | PROVED | Scope (not an error): when rho = 1, RRA > 1 is necessary as well as sufficient for c1* > 1 in the CRRA family. With gamma = 1/2, R = 2, rho = 1, t = 1/2 the optimum gives c1* = 2/3 < 1. |
| Lemma 2 (footnote 4: self-selection) | true | PROVED | Scope (not an error): the paper's rho > 1/R is needed. With R = 2, rho = 2/5, gamma = 2, t = 1/2, c2* - c1* = -7/2 + 3*sqrt(5)/2 < 0, so type 2 would mimic type 1. |
| Claim 1 (good equilibrium of the demand deposit contract) | true | PROVED |  |
| Claim 2 (run equilibrium for r1 > 1) | true | PROVED |  |
| Claim 3 (suspension of convertibility) | true | PROVED | Scope (as the paper says): this works only because t is known; Proposition 1 shows why it fails when t is random. |
| Proposition 1 (no optimal risk sharing when t is random) | true | NOT_CHECKABLE |  |
| Proposition 2 (deposit insurance with an optimal tax) | true (for the reconstructed tax schedule) | PROVED | Reconstruction: the tax schedule in the scanned paper is partly illegible; the check uses the standard form above, so it verifies that schedule, not a transcription of the original. |

## Issues

- **Lemma 1 (eq. 1, footnote 3: the optimum)**: Scope (not an error): when rho = 1, RRA > 1 is necessary as well as sufficient for c1* > 1 in the CRRA family. With gamma = 1/2, R = 2, rho = 1, t = 1/2 the optimum gives c1* = 2/3 < 1.
- **Lemma 2 (footnote 4: self-selection)**: Scope (not an error): the paper's rho > 1/R is needed. With R = 2, rho = 2/5, gamma = 2, t = 1/2, c2* - c1* = -7/2 + 3*sqrt(5)/2 < 0, so type 2 would mimic type 1.
- **Claim 3 (suspension of convertibility)**: Scope (as the paper says): this works only because t is known; Proposition 1 shows why it fails when t is random.
- **Proposition 2 (deposit insurance with an optimal tax)**: Reconstruction: the tax schedule in the scanned paper is partly illegible; the check uses the standard form above, so it verifies that schedule, not a transcription of the original.

## Steps that are not PROVED, and why

- **Proposition 1 (no optimal risk sharing when t is random)**, Case 1: unequal payments to type 1 agents are suboptimal (equal treatment): NOT_CHECKABLE. an argument about all possible contracts. Its hypothesis (u strictly concave, so equal treatment is optimal) is checked in Assumption 1
- **Proposition 1 (no optimal risk sharing when t is random)**, The two cases are exhaustive: NOT_CHECKABLE. logical case split (V1 varies with fj for some t, or for none); checked by reading

## Dependency graph (from the imports)

- `assumption_01_preferences` uses: nothing
- `lemma_01_optimum` uses: nothing
- `lemma_02_self_selection` uses: `lemma_01_optimum`
- `claim_01_good_equilibrium` uses: `lemma_01_optimum`, `lemma_02_self_selection`
- `claim_02_run_equilibrium` uses: `lemma_01_optimum`
- `claim_03_suspension` uses: `lemma_01_optimum`, `lemma_02_self_selection`
- `proposition_01_no_optimal_risk_sharing` uses: `lemma_01_optimum`
- `proposition_02_deposit_insurance` uses: `lemma_01_optimum`, `lemma_02_self_selection`
