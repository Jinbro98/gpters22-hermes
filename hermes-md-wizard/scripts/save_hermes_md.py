#!/usr/bin/env python3
"""Deterministically save a SOUL.md or HERMES.md into the correct Hermes root.

This helper exists so the wizard never loses data: root resolution, directory
creation, and timestamped backup happen atomically in code instead of being
re-derived by the model on every run.

Resolution order for the root folder:
  1. --root PATH                      (explicit override; used as-is)
  2. --profile NAME                   -> {hermes-home}/profiles/{NAME}
  3. exactly one folder under         -> that profile folder
     {hermes-home}/profiles/
  4. otherwise                        -> {hermes-home}

If {hermes-home}/profiles/ contains MORE than one profile and neither --root
nor --profile is given, the script refuses and asks the caller to disambiguate
(matches the wizard rule: "프로필이 여러 개라 모호하면 어느 프로필에 저장할지 물어보세요").

Content is read from --content-file, or from stdin when that flag is omitted.

Usage:
  python save_hermes_md.py --file SOUL.md --content-file /tmp/soul.md
  python save_hermes_md.py --file HERMES.md --profile myagent < content.md
  python save_hermes_md.py --file SOUL.md --root /custom/path --content-file c.md

On success prints a JSON summary to stdout:
  {"root": "...", "saved": "...", "backup": "..."|null, "created_dir": true|false}
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ALLOWED_FILES = {"SOUL.md", "HERMES.md", ".hermes.md"}


def resolve_root(hermes_home: Path, profile: str | None, root: str | None) -> Path:
    if root:
        return Path(root).expanduser()
    if profile:
        return hermes_home / "profiles" / profile

    profiles_dir = hermes_home / "profiles"
    profile_dirs = (
        sorted(p for p in profiles_dir.iterdir() if p.is_dir())
        if profiles_dir.is_dir()
        else []
    )
    if len(profile_dirs) == 1:
        return profile_dirs[0]
    if len(profile_dirs) > 1:
        names = ", ".join(p.name for p in profile_dirs)
        raise SystemExit(
            f"ERROR: multiple profiles found ({names}). "
            f"Re-run with --profile NAME or --root PATH to choose one."
        )
    return hermes_home


def backup_existing(target: Path) -> Path | None:
    if not target.exists():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    backup = target.with_name(f"{target.stem}.backup-{stamp}{target.suffix}")
    # Avoid clobbering a backup made in the same minute.
    counter = 1
    while backup.exists():
        backup = target.with_name(
            f"{target.stem}.backup-{stamp}-{counter}{target.suffix}"
        )
        counter += 1
    backup.write_bytes(target.read_bytes())
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, choices=sorted(ALLOWED_FILES),
                        help="Which file to write.")
    parser.add_argument("--content-file",
                        help="Path to a file holding the assembled markdown. "
                             "If omitted, content is read from stdin.")
    parser.add_argument("--profile", default=None,
                        help="Target profile name under {hermes-home}/profiles/.")
    parser.add_argument("--root", default=None,
                        help="Explicit root folder (overrides profile detection).")
    parser.add_argument("--hermes-home", default="~/.hermes",
                        help="Hermes home dir (default: ~/.hermes).")
    args = parser.parse_args()

    hermes_home = Path(args.hermes_home).expanduser()

    if args.content_file:
        content = Path(args.content_file).expanduser().read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()
    if not content.strip():
        raise SystemExit("ERROR: refusing to save empty content.")

    root = resolve_root(hermes_home, args.profile, args.root)
    created_dir = not root.exists()
    root.mkdir(parents=True, exist_ok=True)

    target = root / args.file
    backup = backup_existing(target)
    target.write_text(content, encoding="utf-8")

    print(json.dumps({
        "root": str(root),
        "saved": str(target),
        "backup": str(backup) if backup else None,
        "created_dir": created_dir,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
