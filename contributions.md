# Contributing to Project Event Horizon

Contributions are submitted through pull requests to `main`. Challenge fixes
must stay focused on the diagnostic issue they address and pass the repository's
public and held-out tests.

## Before you begin

1. Choose an open diagnostic issue.
2. Fork the repository and clone your fork.
3. Create a branch for the issue instead of working directly on `main`.
4. Install the project and development dependencies:

   ```bash
   uv sync
   ```

## Challenge scope

Use the diagnostic's primary files as your working scope:

| Issue | Diagnostic | Expected files |
|---|---|---|
| `#1` | Telemetry execution crash | `src/event_horizon/tensor_alignment.py` |
| `#2` | Dataset scaling instability | `src/event_horizon/batch_flux.py` |
| `#3` | Convergence phase desynchronization | `src/event_horizon/phase_desync.py` |
| `#4` | Neural pruning audit | `src/event_horizon/field_stress.py`, `REPORT.md` |

Keep the pull request limited to the issue being solved. If one pull request
intentionally addresses multiple issues, reference every applicable issue.

Candidates must not modify the following protected files:

- `.github/**`
- `tests/**`
- `pyproject.toml`
- `uv.lock`
- `src/event_horizon/dataset.py`
- `src/event_horizon/utils.py`
- `src/event_horizon/cli.py`

The policy check lists any protected files changed by a pull request. Restore
those files from `main` and push the correction. Infrastructure changes require
prior maintainer approval and the `infrastructure-approved` label.

## Test your solution

Run the public test suite before pushing:

```bash
uv run pytest tests/test_event_horizon.py -q
```

You may also run the complete local suite:

```bash
uv run pytest -q
```

Pull requests run public tests on Python 3.9 and 3.11. They also run the
issue-specific tests stored on the repository's `tests` branch. Those tests are
overlaid by CI, so changing tests in a contributor branch cannot weaken the
checks.

## Open the pull request

Open a pull request from your branch to this repository's `main` branch. Put an
issue-closing reference in the title or description, for example:

```text
Fixes #2
```

References such as `Fixes #2`, `Closes #2`, or `Resolves #2` are recognized
because they contain the exact issue number. A description without `#1`, `#2`,
`#3`, or `#4` does not satisfy the challenge policy.

Include the following in the description:

- What was wrong and what you changed
- The diagnostic issue number
- How you tested the change
- Relevant before-and-after evidence requested by the issue

Suggested description:

```markdown
Fixes #2

## What changed

Briefly explain the cause and the focused fix.

## Verification

- `uv run pytest tests/test_event_horizon.py -q`
- Add any issue-specific evidence here.
```

## Automated checks and review

Every challenge pull request is expected to pass:

- PR policy validation
- Held-out challenge tests for the referenced or affected diagnostics
- Public tests on Python 3.9
- Public tests on Python 3.11

GitHub also runs automatic labeling and configured security checks. A maintainer
review and approval may be required before merging.

If you add the issue reference after opening the pull request, edit its title or
description and save it. The policy and challenge workflows will run again. If
a check fails after a code change, fix the problem locally and push another
commit to the same branch; do not open a replacement pull request.

## Keep the pull request reviewable

- Avoid unrelated formatting, cleanup, generated files, or dependency updates.
- Do not include secrets, local environments, caches, or editor files.
- Keep commits understandable and use a clear pull request title.
- Respond to review comments and resolve conversations after addressing them.
- Do not force-push after review unless a maintainer asks you to rewrite history.
