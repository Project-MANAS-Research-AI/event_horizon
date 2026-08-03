# GitHub Automation

Project Event Horizon uses GitHub Actions for visible smoke tests, held-out
diagnostic tests, dependency checks, security scanning, and pull-request
labeling.

## Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `regular-tests.yml` | Pushes and PRs to `main` | Runs the public test suite on Python 3.9 and 3.11. |
| `pr-tests.yml` | PRs to `main` | Fetches `tests/test_pr.py` from the `tests` branch and runs the complete challenge suite. |
| `codeql.yml` | Pushes and PRs to `main`, weekly | Performs Python static security analysis. |
| `dependency-review.yml` | PRs to `main` | Reviews newly introduced dependencies for known vulnerabilities. |
| `pr-labeler.yml` | PRs to `main` | Labels PRs based on the files they change. |

Dependabot checks Python packages and GitHub Actions weekly.

## Held-out challenge tests

The `tests` branch owns `tests/test_pr.py`. The PR workflow checks out the PR,
then overlays only that file from `origin/tests`. Contributor changes therefore
cannot weaken the challenge tests, while the public tests on `main` remain in
place.

The branch is public, so these tests are held out from contributor branches but
are not confidential.

## One-time repository setup

After both branches are pushed, configure a `main` branch ruleset in GitHub and
require these checks before merging:

- `Python CI / tests (3.9)`
- `Python CI / tests (3.11)`
- `PR Challenge Tests / challenge-tests`
- `Dependency Review / dependency-review`

Enable code scanning under **Settings → Code security** so CodeQL results appear
in the Security tab.

