# CSS Class Scope — benchmark evidence

Everything the extension's README claims about competing extensions was measured
here, and this page carries enough detail to reproduce it. If a number in the
Marketplace listing is not on this page, treat it as unsupported and tell us.

Measured on VS Code 1.136, inside a disposable, network-isolated virtual machine,
one extension at a time, each in its own empty profile.

---

## 1. Do suggestions stay inside the package you are editing?

**Fixture.** A pnpm monorepo with four packages:

| package | role | class definitions |
|---|---|---|
| `web` | the file being edited | 11 (4 top level, 7 nested) |
| `design-system` | declared shared, via `.cssclassscope.json` | 15 (7 top level, 8 nested) |
| `admin` | unrelated (an internal console) | 22 |
| `legacy-marketing` | unrelated (2019 landing pages) | 30 |

26 class names belong to the file's own package plus the shared one. 49 names exist
**only** in the two unrelated packages. Two of the unrelated names (`hero`,
`pricing-card`) also exist in scope, so they are not counted as unrelated.

**Position.** `packages/web/src/index.html` line 30, inside an empty `class=""`.
Empty on purpose: extensions differ in whether they pre-filter on the word already
typed, so a position with text in it produces lists that cannot be compared.

**Question.** Of the class names the extension offers, how many exist only in a
package this file has nothing to do with?

| extension | version | settings given | offered | of those, from unrelated packages |
|---|---|---|---|---|
| **CSS Class Scope** | 0.1.1 | none beyond the repo's `.cssclassscope.json` | 26 | **0** |
| pucelle.vscode-css-navigation | 2.15.1 | defaults | 75 | 49 |
| ecmel.vscode-html-css | 2.0.14 | `css.styleSheets` set to the whole workspace, plus the same 15-language `css.enabledLanguages` list | 61 | 49 |
| Zignd.html-css-class-completion | 1.20.0 | defaults | 51 | 49 |

ecmel is given a workspace-wide `css.styleSheets` because it indexes nothing without
it — with no settings its list is empty, which would not be a fair comparison.

**Second probe.** At the same position, type `admin-`, a prefix that exists only in
the unrelated admin package:

| extension | candidates offered | example |
|---|---|---|
| **CSS Class Scope** | **0** | — |
| pucelle.vscode-css-navigation | 6 | `admin-shell`, `admin-table__row--selected` |
| ecmel.vscode-html-css | 61 (unfiltered list) | contains all 49 |
| Zignd.html-css-class-completion | 51 (unfiltered list) | contains all 49 |

Raw output: [`probe-2026-09-09.json`](probe-2026-09-09.json).

---

## 2. Are nested SCSS selectors resolved?

Classes written as `&__element` / `&--modifier` compile to a compound name. Six of
them exist in the fixture: `ds-button__icon`, `ds-button__label`,
`ds-button--primary`, `ds-button--ghost`, `hero__title`, `pricing-card__price`.

| extension | resolved |
|---|---|
| **CSS Class Scope** | 6 / 6 |
| pucelle.vscode-css-navigation | 6 / 6 |
| ecmel.vscode-html-css | 0 / 6 |
| Zignd.html-css-class-completion | 0 / 6 |

**CSS Navigation resolves nested selectors correctly.** The extensions that do not
are the two most-installed ones. We do not claim this as something only CSS Class
Scope does.

---

## 3. Public repositories, 2026-09-08

Measured before CSS Navigation was added to the comparison, so **these three rows do
not include it**. Same VS Code build, cloned public repositories, identical
completion positions, and the normalising settings above.

| metric | repository | ecmel 2.0.14 | Zignd 1.20.0 | CSS Class Scope 0.1.1 |
|---|---|---|---|---|
| classes offered from other packages | adobe/spectrum-css | 17,003 | 2,417 | **0** |
| known classes found, 25 positions | elastic/eui | 5 / 25 | not measured | **25 / 25** |
| completion reflects a saved edit | four repositories | 30–60 ms | not detected within 20–60 s | 4–73 ms |
| initial workspace indexing | adobe/spectrum-css | 344 ms | 46 ms | **879 ms** |

The last row is the one we lose. Initial indexing of a large monorepo is currently
slower than both established competitors. It happens once per workspace and does not
affect the numbers above it, but it is a real gap and it is on the roadmap.

---

## Reproducing this

The harness, the fixture and the probe script ship in the extension's repository:

- `test/fixtures/demo-monorepo/` — the fixture, plus one copy per competitor whose
  only difference is `.vscode/settings.json`
- `test/visual/plans/probe-*.json` — the positions and keystrokes, one plan per extension
- `scripts/probe_report.py` — counts how many offered names are unrelated
- `bench/run.sh` and `bench/README.md` — the 2026-09-08 public-repository harness

Each run records the candidate labels, not just how many there were, so the counts
above can be recomputed from the raw output rather than taken on trust.

Corrections are welcome. If a setting we gave a competing extension is not the
setting a real user would give it, that is a bug in this comparison and we want to
fix it.
