#!/usr/bin/env python3
"""Verify every public HTML page includes the Google Analytics tag.

Pages can opt out by including the marker `<!-- ga-exempt:` (with an optional
reason) anywhere in the file. Print templates and other internal tools should
use this marker rather than being added to the path exclusion list below.
"""
from __future__ import annotations

import argparse
import fnmatch
import sys
from pathlib import Path

GA_ID = "G-WXEF9TG8WK"
EXEMPT_MARKER = "<!-- ga-exempt:"

# Paths (glob patterns, relative to repo root) that are not public pages.
PATH_EXCLUDES = [
    "just-do-ai/b-cards/*.html",
    "images/social-preview-generator.html",
    "**/heic_converter/**",
]


def is_path_excluded(path: Path) -> bool:
    posix = path.as_posix()
    return any(fnmatch.fnmatch(posix, pat) for pat in PATH_EXCLUDES)


def check_file(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"could not read: {e}"
    if EXEMPT_MARKER in content:
        return None
    if GA_ID not in content:
        return f"missing GA tag ({GA_ID}) and no '{EXEMPT_MARKER} ...' marker"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="HTML files to check (from pre-commit)")
    args = parser.parse_args()

    failures: list[tuple[Path, str]] = []
    for f in args.files:
        path = Path(f)
        if path.suffix.lower() != ".html":
            continue
        if is_path_excluded(path):
            continue
        if not path.exists():
            continue
        problem = check_file(path)
        if problem:
            failures.append((path, problem))

    if failures:
        print("Google Analytics check failed:", file=sys.stderr)
        for path, problem in failures:
            print(f"  {path}: {problem}", file=sys.stderr)
        print(
            f"\nAdd the gtag snippet for {GA_ID}, or mark the page exempt with an\n"
            f"HTML comment like: {EXEMPT_MARKER} internal print template -->",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
