#!/usr/bin/env python3
"""Sync PatrickJS awesome-cursorrules README into tarshub.json files and _index.json."""
from __future__ import annotations

import json
import re
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

README_URL = (
    "https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/README.md"
)
TREE_API = (
    "https://api.github.com/repos/PatrickJS/awesome-cursorrules/git/trees/main"
    "?recursive=1"
)

EXCLUDED_FOLDERS = {
    "angular-novo-elements-cursorrules-prompt-file",
    "angular-typescript-cursorrules-prompt-file",
    "astro-typescript-cursorrules-prompt-file",
    "beefreeSDK-nocode-content-editor-cursorrules-prompt-file",
    "cursor-ai-react-typescript-shadcn-ui-cursorrules-p",
}

# README link typos vs actual folder names under rules/ (upstream README issue).
README_FOLDER_REMAP = {
    "drupal-11-cursorrules-promt-file": "drupal-11-cursorrules-prompt-file",
}

KEYWORDS = [
    "awesome",
    "awesome-list",
    "cursor",
    "cursor-ai-editor",
    "cursorrules",
]

REGISTRY_ROOT = Path(__file__).resolve().parents[1]
PACKAGES_RULES = REGISTRY_ROOT / "packages" / "PatrickJS" / "awesome-cursorrules" / "rules"
INDEX_PATH = REGISTRY_ROOT / "_index.json"


def fetch_text(url: str) -> str:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "tarshub-registry-sync"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
        return r.read().decode("utf-8")


def fetch_json(url: str):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "tarshub-registry-sync"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_readme_rules(readme: str) -> list[tuple[str, str]]:
    line_re = re.compile(
        r"^\s*-\s*\[([^\]]*)\]\(\./rules/([^)]+)\)\s*-\s*(.+)\s*$"
    )
    out: list[tuple[str, str]] = []
    for line in readme.splitlines():
        m = line_re.match(line)
        if not m:
            continue
        link_path = m.group(2).strip()
        desc = m.group(3).strip()
        folder = link_path.split("/")[0]
        out.append((folder, desc))
    return out


def build_tree_files_by_folder(tree: dict) -> dict[str, list[str]]:
    by_folder: dict[str, list[str]] = {}
    for item in tree.get("tree", []):
        if item.get("type") != "blob":
            continue
        path = item.get("path", "")
        if not path.startswith("rules/"):
            continue
        parts = path.split("/")
        if len(parts) < 3:
            continue
        folder = parts[1]
        rel = "/".join(parts[2:])
        by_folder.setdefault(folder, []).append(rel)
    return by_folder


def sort_files_for_tarshub(files: list[str]) -> list[str]:
    def key(f: str) -> tuple:
        if f == ".cursorrules":
            return (0, f)
        if f == "README.md":
            return (1, f)
        return (2, f.lower())

    return sorted(files, key=key)


def main() -> None:
    readme = fetch_text(README_URL)
    rows = parse_readme_rules(readme)

    seen: set[str] = set()
    ordered_folders: list[str] = []
    folder_desc: dict[str, str] = {}
    for folder, desc in rows:
        folder = README_FOLDER_REMAP.get(folder, folder)
        if folder in seen:
            continue
        seen.add(folder)
        ordered_folders.append(folder)
        folder_desc[folder] = desc

    tree_data = fetch_json(TREE_API)
    if tree_data.get("truncated"):
        raise SystemExit("Git tree truncated")

    files_by_folder = build_tree_files_by_folder(tree_data)

    to_generate = [f for f in ordered_folders if f not in EXCLUDED_FOLDERS]

    for folder in to_generate:
        files = files_by_folder.get(folder)
        if not files:
            print(f"WARN: no files in tree for folder {folder}, skipping")
            continue

        pkg_dir = PACKAGES_RULES / folder
        pkg_dir.mkdir(parents=True, exist_ok=True)

        tarshub = {
            "name": folder,
            "description": folder_desc.get(folder, ""),
            "keywords": KEYWORDS.copy(),
            "version": "1.0.0",
            "repo": f"PatrickJS/awesome-cursorrules/rules/{folder}",
            "files": sort_files_for_tarshub(files),
            "contentType": "cursor-rules",
        }
        (pkg_dir / "tarshub.json").write_text(
            json.dumps(tarshub, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    index_raw = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    non_patrick = [
        p
        for p in index_raw.get("packages", [])
        if not p.get("id", "").startswith("PatrickJS/awesome-cursorrules/")
    ]

    patrick_packages = []
    for folder in ordered_folders:
        files = files_by_folder.get(folder)
        if not files:
            print(f"WARN: index skip missing tree folder {folder}")
            continue
        patrick_packages.append(
            {
                "id": f"PatrickJS/awesome-cursorrules/rules/{folder}",
                "name": folder,
                "author": "PatrickJS",
                "avatar": "https://avatars.githubusercontent.com/PatrickJS",
                "repo": f"PatrickJS/awesome-cursorrules/rules/{folder}",
                "description": folder_desc[folder],
                "keywords": KEYWORDS.copy(),
                "files": len(files),
                "version": "1.0.0",
                "contentType": "cursor-rules",
            }
        )

    index_raw["updated"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )
    index_raw["packages"] = patrick_packages + non_patrick

    INDEX_PATH.write_text(
        json.dumps(index_raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"tarshub written: {len(to_generate)} (excluded {len(EXCLUDED_FOLDERS)})")
    print(f"index PatrickJS: {len(patrick_packages)}, other: {len(non_patrick)}")


if __name__ == "__main__":
    main()
