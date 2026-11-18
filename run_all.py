"""Run every result's check() in dependency order (the import graph) and write REPORT.md."""
import ast
import importlib
import os
import pkgutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from framework.status import Status  # noqa: E402

ORDER = ["assumption", "lemma", "claim", "proposition", "theorem", "corollary"]


def modules():
    names = [m.name for m in pkgutil.iter_modules([os.path.join(HERE, "results")])]
    deps = {}
    for n in names:
        tree = ast.parse(open(os.path.join(HERE, "results", n + ".py"), encoding="utf-8").read())
        deps[n] = {node.module.split(".")[1] for node in ast.walk(tree)
                   if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("results.")}
    done, out = set(), []

    def visit(n, stack=()):
        if n in stack:
            raise SystemExit(f"circular dependency: {' -> '.join(stack + (n,))}")
        if n in done:
            return
        for d in sorted(deps[n]):
            visit(d, stack + (n,))
        done.add(n)
        out.append(n)
    for n in sorted(names, key=lambda x: (ORDER.index(x.split("_")[0]), x)):
        visit(n)
    return out, deps


def main():
    order, deps = modules()
    rows, issues, notes = [], [], []
    for n in order:
        r = importlib.import_module(f"results.{n}").check()
        print(f"{r.status.name:<14} {r.name}")
        main_issue = r.issues[0] if r.issues else ""
        rows.append(f"| {r.name} | {r.statement_verdict} | {r.status.name} | {main_issue} |")
        issues += [f"- **{r.name}**: {i}" for i in r.issues]
        for s in r.steps:
            if s.status != Status.PROVED:
                notes.append(f"- **{r.name}**, {s.label}: {s.status.name}. {s.note}")
    graph = "\n".join(f"- `{n}` uses: {', '.join(f'`{d}`' for d in sorted(deps[n])) or 'nothing'}" for n in order)
    report = ["# REPORT: Diamond and Dybvig (1983), checked result by result", "",
              "| Result | Statement | Proof label | Main issue |", "|---|---|---|---|", *rows, "",
              "## Issues", "", *(issues or ["None."]), "",
              "## Steps that are not PROVED, and why", "", *(notes or ["None."]), "",
              "## Dependency graph (from the imports)", "", graph, ""]
    open(os.path.join(HERE, "REPORT.md"), "w", encoding="utf-8").write("\n".join(report))
    print("\nREPORT.md written")


if __name__ == "__main__":
    main()
