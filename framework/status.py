"""Verification labels, steps and results (weakest step decides a result's label)."""
from dataclasses import dataclass, field
from enum import IntEnum


class Status(IntEnum):          # ordered weakest -> strongest, so min() gives the overall label
    FAILED = 0
    NOT_CHECKABLE = 1
    NUMERICAL = 2
    CERTIFIED = 3
    PROVED = 4


@dataclass
class Step:
    label: str                  # e.g. "Step 2: FOC gives eq. (1b)"
    status: Status
    note: str = ""              # what was checked, region, method, counterexample


@dataclass
class Result:
    name: str                   # e.g. "Proposition 1"
    statement_verdict: str      # "true" / "false" / "true on smaller region" / "unchecked"
    steps: list = field(default_factory=list)
    issues: list = field(default_factory=list)   # plain-language issues for REPORT.md

    @property
    def status(self) -> Status:
        return min((s.status for s in self.steps), default=Status.NOT_CHECKABLE)
