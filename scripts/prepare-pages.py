#!/usr/bin/env python3
"""Safely mirror dist/ into docs/ for GitHub Pages branch publication.

Only standard-library modules are required. Run from any working directory.
The manifest protects manual changes in generated docs/ from being overwritten.
"""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DOCS = ROOT / "docs"
MANIFEST = ROOT / "scripts" / ".pages-manifest.json"


def inside_root(path):
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise SystemExit(f"Unsafe path outside project or symbolic link: {path}")


def files_under(folder):
    inside_root(folder)
    result = {}
    for path in sorted(folder.rglob("*")):
        inside_root(path)
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise SystemExit(f"Unsupported file type: {path}")
    return result


def main():
    for path in (DIST, DOCS, MANIFEST, MANIFEST.parent):
        inside_root(path)
    if not DIST.is_dir() or not (DIST / "index.html").is_file():
        raise SystemExit("dist/index.html is required; build content before publishing.")
    expected = files_under(DIST)
    expected[".nojekyll"] = sha256(b"\n").hexdigest()
    if DOCS.exists():
        if not DOCS.is_dir() or not MANIFEST.is_file():
            raise SystemExit("Existing docs/ is not managed by this script; move it aside first.")
        previous = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if files_under(DOCS) != previous:
            raise SystemExit("docs/ contains manual changes. Keep edits in dist/; preserve or revert docs/ before syncing.")
    stage = Path(tempfile.mkdtemp(prefix=".pages-build-", dir=ROOT))
    backup = None
    try:
        shutil.copytree(DIST, stage, dirs_exist_ok=True)
        (stage / ".nojekyll").write_bytes(b"\n")
        if files_under(stage) != expected:
            raise SystemExit("Staged files differ from dist/; no published files were replaced.")
        if DOCS.exists():
            backup = Path(tempfile.mkdtemp(prefix=".pages-previous-", dir=ROOT))
            backup.rmdir()
            DOCS.rename(backup)
        try:
            stage.rename(DOCS)
            MANIFEST.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except BaseException:
            if DOCS.exists():
                shutil.rmtree(DOCS)
            if backup is not None:
                backup.rename(DOCS)
                backup = None
            raise
        if backup is not None:
            shutil.rmtree(backup)
            backup = None
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print(f"GitHub Pages ready: docs/ contains {len(expected)} files, including .nojekyll.")


if __name__ == "__main__":
    main()
