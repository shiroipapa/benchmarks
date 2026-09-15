# Shiroipapa Apps — benchmark evidence

Every comparative claim on a Shiroipapa Apps product page is measured, and the
measurement lives here. If a number appears in a listing and not on one of
these pages, treat it as unsupported and tell us.

| product | evidence |
|---|---|
| CSS Class Scope (VS Code) | [css-class-scope/](css-class-scope/) |

Measurements run one extension at a time, each in its own empty profile,
inside a disposable virtual machine with no network access. The fixtures and
the exact positions measured are described on each page, so the fixture-based
numbers can be reproduced rather than taken on trust.

Where a competitor does something better than us, it is on the page too.

---

## About Shiroipapa Apps

**Small tools for developers.** One job each, done properly, and measured
rather than claimed. Website: **[shiroipapa.github.io](https://shiroipapa.github.io/)**

Nothing is on sale yet. When a product can be bought, the website will say where.

### CSS Class Scope — for VS Code · *In development / not yet published*

Autocomplete for CSS class names that stays inside the package you are
editing. In a monorepo, some popular CSS completion extensions can offer
classes from unrelated packages, so typing `btn-` in `packages/web` suggests
classes from `packages/admin` too. CSS Class Scope narrows completion, *go to
definition* and *find references* to the package you are in plus the shared
design system you declared, resolves common nested SCSS selectors, and reports
classes defined in scope that nothing in scope uses.

Not yet published to the Visual Studio Marketplace. Pricing and licensing will
be announced when it is.

### Support

**shiroipapaapps@gmail.com** — questions and bug reports.
