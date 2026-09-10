#!/usr/bin/env python3
"""probe_report.py — turn the four probe runs into one comparable table.

    python3 scripts/probe_report.py <evidence-dir-ours> <evidence-dir-cssnav> ...

Why this exists: the extensions do not answer the same question. Some return
their whole candidate set and let VS Code filter it; CSS Navigation filters on
the word already typed before it answers. So "how many candidates came back"
is not comparable between them, and the 2026-09-09 independent review was
right to ask for a fair measurement.

What is comparable is the content of the list: given the class definitions in
the fixture, how many of the names offered belong ONLY to a package this file
has nothing to do with. That question has the same meaning for every provider.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIXTURE = os.path.join(ROOT, "test/fixtures/demo-monorepo")

IN_SCOPE = [
    ("web (the file's own package)", ["packages/web/src/styles/hero.scss"]),
    ("design-system (declared shared)", ["packages/design-system/src/button.scss",
                                         "packages/design-system/src/layout.scss"]),
]
UNRELATED = [
    ("admin", ["packages/admin/src/admin.css"]),
    ("legacy-marketing", ["packages/legacy-marketing/src/legacy.css"]),
]


def class_names(path: str) -> set[str]:
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)
    names = set()
    base = None
    for line in text.splitlines():
        top = re.match(r"\s*\.([A-Za-z_][A-Za-z0-9_-]*)\s*\{", line)
        if top:
            base = top.group(1)
        nested = re.match(r"\s*&([_-][A-Za-z0-9_-]*)\s*\{", line)
        if nested and base:
            names.add(base + nested.group(1))
    for match in re.finditer(r"(^|[\s,>+~])\.([A-Za-z_][A-Za-z0-9_-]*)", text):
        names.add(match.group(2))
    return names


def group(spec) -> dict[str, set[str]]:
    return {name: set().union(*[class_names(os.path.join(FIXTURE, f)) for f in files])
            for name, files in spec}


def load(evidence_dir: str) -> dict:
    text = open(os.path.join(evidence_dir, "results.txt"), encoding="utf-8").read()
    return json.loads(text[text.index("{"):])


def main() -> int:
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        print(__doc__)
        print("usage: probe_report.py <label> <evidence-dir> [<label> <evidence-dir> ...]")
        return 2

    in_scope = set().union(*group(IN_SCOPE).values())
    unrelated_only = set().union(*group(UNRELATED).values()) - in_scope

    print(f"fixture: {len(in_scope)} class names in scope "
          f"(the file's own package plus the declared shared package), "
          f"{len(unrelated_only)} that exist only in packages this file does not use\n")

    rows = []
    pairs = list(zip(sys.argv[1::2], sys.argv[2::2]))
    for label, directory in pairs:
        data = load(directory)
        row = {"label": label, "evidence": os.path.basename(directory), "shots": {}}
        for shot in data.get("shots", []):
            completions = shot.get("completions") or {}
            labels = completions.get("labels") or []
            leaked = sorted(set(labels) & unrelated_only)
            row["shots"][shot["name"]] = {
                "offered": completions.get("count"),
                "from_unrelated_packages": len(leaked),
                "examples": leaked[:6],
            }
        rows.append(row)

    name_width = max(len(r["label"]) for r in rows) + 2
    shot_names = ["p1-empty-class", "p2-unrelated-prefix", "p3-shared-prefix"]
    header = ("extension".ljust(name_width) + "".join(s.ljust(30) for s in shot_names))
    print(header)
    print("-" * len(header))
    for row in rows:
        line = row["label"].ljust(name_width)
        for shot_name in shot_names:
            shot = row["shots"].get(shot_name)
            if shot is None:
                line += "—".ljust(30)
            else:
                line += f"{shot['offered']} offered / {shot['from_unrelated_packages']} unrelated".ljust(30)
        print(line)
    print()
    for row in rows:
        for shot_name, shot in row["shots"].items():
            if shot["examples"]:
                print(f"  {row['label']} {shot_name}: leaked e.g. {', '.join(shot['examples'])}")
    print()
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
