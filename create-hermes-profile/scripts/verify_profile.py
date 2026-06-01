#!/usr/bin/env python3
"""Run all post-setup verification checks for a Hermes profile in one pass.

Replaces the seven manual `hermes ...` commands at the end of the create flow so
no check is silently skipped. Each check is run via subprocess; output is printed
under a clear header and a final PASS/WARN/FAIL summary is shown.

Usage:
  python verify_profile.py NAME
  python verify_profile.py NAME --since 10m -n 100

This script does NOT redact secrets — gateway logs may contain tokens. The agent
must redact before relaying any output to the user (see SKILL.md rule #4).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys

# (label, args-after-`hermes`, fail_is_hard)
def build_checks(name: str, since: str, lines: str):
    return [
        ("profile show", ["profile", "show", name], True),
        ("config check", ["--profile", name, "config", "check"], True),
        ("tools list", ["--profile", name, "tools", "list"], False),
        ("gateway status", ["--profile", name, "gateway", "status"], False),
        ("gateway logs", ["--profile", name, "logs", "gateway",
                          "--since", since, "-n", lines], False),
    ]


def run_check(hermes: str, argv: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            [hermes, *argv],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return 124, "(timed out after 60s)"
    except FileNotFoundError:
        return 127, f"(command not found: {hermes})"
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Profile name to verify.")
    parser.add_argument("--since", default="10m", help="Log window (default 10m).")
    parser.add_argument("-n", dest="lines", default="100",
                        help="Log line count (default 100).")
    parser.add_argument("--hermes", default="hermes",
                        help="Path to the hermes CLI (default: 'hermes' on PATH).")
    args = parser.parse_args()

    hermes = shutil.which(args.hermes) or args.hermes

    results = []
    for label, argv, hard in build_checks(args.name, args.since, args.lines):
        print(f"\n===== {label}: hermes {' '.join(argv)} =====")
        code, out = run_check(hermes, argv)
        print(out if out else "(no output)")
        if code == 0:
            status = "PASS"
        elif hard:
            status = "FAIL"
        else:
            status = "WARN"
        results.append((label, status, code))

    print("\n===== SUMMARY =====")
    worst = "PASS"
    for label, status, code in results:
        print(f"  [{status}] {label} (exit {code})")
        if status == "FAIL":
            worst = "FAIL"
        elif status == "WARN" and worst != "FAIL":
            worst = "WARN"

    print(f"\nOverall: {worst}")
    print("NOTE: redact any tokens/secrets from gateway logs before relaying.")
    return 1 if worst == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
