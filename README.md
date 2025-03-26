# version_bumper
A pre-commit hook that enforces version.md patch bumps when code changes are made but no version update is done.

## Usage

1. Add this repo to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/13aksh/version_bumper
    rev: v1.0.2
    hooks:
      - id: version-bumper
