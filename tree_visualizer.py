#!/usr/bin/env python3
"""Recursively render a directory tree.

This script prints a visual tree of a directory structure similar to the Unix
``tree`` command. It is intentionally lightweight so it can run anywhere Python
is available, including on macOS and within the iOS/iPadOS Files app via
Python-capable tools like Pyto or Pythonista.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional
import argparse
import sys


@dataclass
class TreeOptions:
    """Configuration controlling how the tree is rendered."""

    include_hidden: bool
    max_depth: Optional[int]
    follow_symlinks: bool


@dataclass
class TreeStats:
    """Metadata describing how many items were rendered."""

    directories: int = 0
    files: int = 0

    def bump_dir(self) -> None:
        self.directories += 1

    def bump_file(self) -> None:
        self.files += 1


def iter_entries(path: Path, options: TreeOptions) -> Iterable[Path]:
    """Yield sorted child paths for ``path`` respecting the options provided."""

    try:
        entries = list(path.iterdir())
    except PermissionError:
        print(f"Skipping {path} (permission denied)", file=sys.stderr)
        return []

    if not options.include_hidden:
        entries = [entry for entry in entries if not entry.name.startswith('.')]

    # Sort directories first, then files, alphabetically.
    return sorted(entries, key=lambda p: (p.is_file(), p.name.lower()))


def render_tree(
    path: Path,
    *,
    prefix: str = "",
    is_last: bool = True,
    depth: int = 0,
    options: TreeOptions,
    stats: TreeStats,
    lines: Optional[List[str]] = None,
) -> List[str]:
    """Recursively walk ``path`` and collect formatted tree lines."""

    if lines is None:
        lines = []

    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{path.name}")

    if path.is_dir():
        stats.bump_dir()
    else:
        stats.bump_file()
        return lines

    # Stop if depth limit reached.
    if options.max_depth is not None and depth >= options.max_depth:
        return lines

    entries = iter_entries(path, options)
    entries = [e for e in entries if options.follow_symlinks or not e.is_symlink()]

    if not entries:
        return lines

    new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
    for index, child in enumerate(entries):
        child_is_last = index == len(entries) - 1
        render_tree(
            child,
            prefix=new_prefix,
            is_last=child_is_last,
            depth=depth + 1,
            options=options,
            stats=stats,
            lines=lines,
        )

    return lines


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a visual directory tree with optional depth and hidden-file control.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Directory to inspect (defaults to the current working directory).",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Limit recursion to this depth (0 shows only the top directory).",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories (those starting with a dot).",
    )
    parser.add_argument(
        "--follow-symlinks",
        action="store_true",
        help="Follow symlinked directories when traversing.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    target_path = args.path.expanduser().resolve()

    if not target_path.exists():
        print(f"Path does not exist: {target_path}", file=sys.stderr)
        return 1

    options = TreeOptions(
        include_hidden=args.include_hidden,
        max_depth=args.max_depth,
        follow_symlinks=args.follow_symlinks,
    )

    stats = TreeStats()
    lines: List[str] = []
    render_tree(target_path, prefix="", is_last=True, depth=0, options=options, stats=stats, lines=lines)

    # Root entry has no leading lines; print as-is.
    print('\n'.join(lines))
    print(f"\n{stats.directories} directories, {stats.files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
