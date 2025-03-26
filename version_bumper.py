#!/usr/bin/env python3

import subprocess
import sys
import re
from pathlib import Path

VERSION_FILE = "version.md"

def main():
    # 1) Check if version.md has any staged changes
    #    Return code == 0 => no changes, Return code != 0 => there's a diff
    diff_result = subprocess.run(
        ["git", "diff", "--cached", "--exit-code", VERSION_FILE],
        capture_output=True
    )

    if diff_result.returncode == 0:
        # Means version.md was NOT changed in the staged commit
        print(f"{VERSION_FILE} was not changed. Auto-incrementing patch version...")

        path = Path(VERSION_FILE)
        if not path.exists():
            print(f"Error: {VERSION_FILE} does not exist.", file=sys.stderr)
            sys.exit(1)

        version_str = path.read_text().strip()
        # Expect a line like X.Y.Z (semantic version)
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str)
        if not match:
            print(
                f"Error: {VERSION_FILE} must contain a valid semver 'X.Y.Z', found '{version_str}'",
                file=sys.stderr
            )
            sys.exit(1)

        major, minor, patch = match.groups()
        major = int(major)
        minor = int(minor)
        patch = int(patch) + 1  # increment patch
        new_version = f"{major}.{minor}.{patch}"

        # Overwrite version.md
        path.write_text(new_version + "\n")
        # Stage the updated version.md
        subprocess.run(["git", "add", VERSION_FILE], check=True)

        print(f"Updated {VERSION_FILE} from {version_str} to {new_version}.")
        print("Please commit again with the new version.")
        # Fail => user must re-commit
        sys.exit(1)
    else:
        # version.md was changed => pass
        print(f"{VERSION_FILE} is already updated, continuing commit...")
        sys.exit(0)

if __name__ == "__main__":
    main()
