# Reproducing the CSS Class Scope measurements

Everything here is what a third party needs to check our numbers without
taking our word for anything. The fixture, the exact settings each extension
was given, the exact cursor positions and keystrokes, the raw output of our
runs, and the script that turns that output into the published table.

**What is not here:** the virtual-machine wrapper we use to drive VS Code
unattended, and the extension's own source. Neither is needed to check the
numbers — the positions below are ordinary editing positions, and you can
drive VS Code by hand. It does mean the process is manual rather than one
command, and we would rather say that than imply otherwise.

## What is in this directory

| path | what it is |
|---|---|
| `fixture/` | the demo monorepo: 4 packages, 76 class definitions (no `.vscode/` — you supply it in step 2) |
| `settings/` | one `settings.json` per extension configuration measured |
| `plans/` | the positions, keystrokes and waits, one plan per extension |
| `probe_report.py` | counts how many offered names belong only to unrelated packages |
| `../probe-2026-09-09.json` | our raw run output, so you can diff against yours |

## The fixture

```
packages/web               the file being edited      11 classes (4 top level, 7 nested)
packages/design-system     declared shared            15 classes (7 top level, 8 nested)
packages/admin             unrelated                  22 classes
packages/legacy-marketing  unrelated                  30 classes
```

26 names are in scope for `packages/web`. 49 names exist only in the two
unrelated packages. `hero` and `pricing-card` exist on both sides, so they are
not counted as unrelated.

`.cssclassscope.json` at the fixture root declares `design-system` as shared.
That file is read only by CSS Class Scope; it has no effect on the others.

## Running it

1. Copy `fixture/` somewhere scratch. Install **one** extension in an empty
   VS Code profile:

   ```
   code --profile probe --install-extension <extension-id>
   ```

2. Create `fixture/.vscode/settings.json` by copying the matching file from
   `settings/`.
   These are the settings that extension was measured with. The competitor
   files enable the same 15 languages and, for `ecmel-workspace-glob`, point
   `css.styleSheets` at the whole workspace — the configuration its own README
   suggests for a monorepo.

3. Open the fixture **root** as the workspace. Not a package. The whole point
   of the comparison is what happens when one monorepo root is open.

4. Go to `packages/web/src/index.html`, to the `<article class="">` on the
   line the plan names, and put the cursor **inside the empty quotes**.
   Trigger suggestions.

   Measuring at an empty `class=""` matters. Some extensions return their
   whole candidate set and let VS Code filter it; CSS Navigation filters on
   the word already typed before it answers. A count taken at a
   partly-typed position is not comparable between them. Our first published
   table made exactly that mistake and undercounted CSS Navigation; the
   correction is why this position is specified so precisely.

5. Record the **labels** in the list, not just how many there are. The counts
   in the published table are derived from label contents.

6. `python3 probe_report.py <your-run-dir> ...` reproduces the table. Or read
   the labels against `fixture/` yourself; the script is a convenience, not an
   authority.

## The three questions measured

- **Scope.** Of the names offered, how many exist only in a package this file
  has nothing to do with?
- **Nested SCSS.** Do the six compound names (`ds-button__icon`,
  `ds-button__label`, `ds-button--primary`, `ds-button--ghost`,
  `hero__title`, `pricing-card__price`) appear at all?
- **Following the edited package.** `plans/probe-ab.json` opens a page in
  `packages/admin`, then returns to the `packages/web` page, changing no
  settings in between.

## If we got something wrong

If a setting we gave a competing extension is not the setting a real user
would give it, that is a bug in this comparison and we want to fix it.
Open an issue on this repository, or write to shiroipapaapps@gmail.com.
