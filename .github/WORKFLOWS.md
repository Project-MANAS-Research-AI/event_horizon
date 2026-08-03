# GitHub Automation

Project Event Horizon uses GitHub Actions for visible smoke tests, held-out
diagnostic tests, dependency checks, security scanning, and pull-request
labeling.

## Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `pr-policy.yml` | Every PR change to `main` | Validates issue references and blocks unapproved infrastructure changes without executing contributor code. |
| `regular-tests.yml` | Pushes and PRs to `main` | Runs the public test suite on Python 3.9 and 3.11. |
| `pr-tests.yml` | PRs to `main` | Fetches held-out tests and runs only the diagnostics referenced or affected by the PR. |
| `codeql.yml` | Pushes and PRs to `main`, weekly | Performs Python static security analysis when Advanced Security is enabled. |
| `dependency-review.yml` | PRs to `main` | Reviews new dependencies when Advanced Security is enabled. |
| `pr-labeler.yml` | PRs to `main` | Labels PRs based on the files they change. |

Dependabot checks Python packages and GitHub Actions weekly.

## Held-out challenge tests

The `tests` branch owns `tests/test_pr.py`. The PR workflow checks out the PR,
then overlays only that file from `origin/tests`. Contributor changes therefore
cannot weaken the challenge tests, while the public tests on `main` remain in
place.

The workflow reads Issue references `#1` through `#4` from the PR title and
description. It combines those references with diagnostic source files changed
by the PR and runs the corresponding held-out tests. Changing diagnostic code
without referencing at least one diagnostic Issue fails with an actionable
message. PRs unrelated to diagnostics, including dependency and documentation
updates, pass without running intentionally failing challenge tests.

The PR policy runs through `pull_request_target`, so it reports even when GitHub
is waiting for approval before running code from a first-time contributor's
fork. It never checks out or executes contributor code. Human changes under
`.github/` or `tests/`, or to `pyproject.toml`, `uv.lock`, `dataset.py`,
`utils.py`, or `cli.py`, fail with a list of the protected files until a
maintainer applies the `infrastructure-approved` label. Dependabot is exempt so
its narrowly scoped dependency updates can proceed. Human changes to challenge
source code or `REPORT.md` must reference at least one diagnostic Issue.

The branch is public, so these tests are held out from contributor branches but
are not confidential.

## One-time repository setup

After both branches are pushed, configure a `main` branch ruleset in GitHub and
require these checks before merging:

- `Python CI / tests (3.9)`
- `Python CI / tests (3.11)`
- `PR Challenge Tests / challenge-tests`
- `PR Policy / policy`

This repository is private, so CodeQL and dependency review require GitHub
Advanced Security. They are configured but safely skipped by default. To enable
them, an organization administrator must enable Advanced Security and the
dependency graph under **Settings → Code security**, then create a repository
Actions variable named `ENABLE_ADVANCED_SECURITY` with value `true`. Only after
that should `Dependency Review / dependency-review` be made a required check.
