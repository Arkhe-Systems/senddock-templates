#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

REPO_BASE_URL = "https://raw.githubusercontent.com/Arkhe-Systems/senddock-templates/main"
ALLOWED_CATEGORIES = {"welcome", "newsletter", "announcement", "digest", "transactional"}
ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_THUMBNAIL_BYTES = 100 * 1024
MAX_NAME_CHARS = 40
MAX_DESCRIPTION_CHARS = 140
REQUIRED_FIELDS = {"id", "name", "category", "description", "thumbnail_url", "html_url", "variables"}
BUILTIN_VARIABLES = {"name", "email", "subscriber_id", "unsubscribe_url"}
SCRIPT_TAG = re.compile(r"<script[\s>]", re.IGNORECASE)


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "index.json"
    errors: list[str] = []

    try:
        manifest = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"ERROR: cannot parse index.json: {e}")
        sys.exit(1)

    if not isinstance(manifest, dict) or "version" not in manifest or "templates" not in manifest:
        errors.append("index.json: top-level must have `version` and `templates`")
    if not isinstance(manifest.get("templates"), list):
        errors.append("index.json: `templates` must be an array")

    seen_ids: set[str] = set()
    for i, entry in enumerate(manifest.get("templates", [])):
        prefix = f"templates[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: must be an object")
            continue

        missing = REQUIRED_FIELDS - set(entry.keys())
        if missing:
            errors.append(f"{prefix}: missing fields: {sorted(missing)}")
            continue

        eid = entry["id"]
        if not isinstance(eid, str) or not ID_PATTERN.match(eid):
            errors.append(f"{prefix}: id must be kebab-case (got {eid!r})")
            continue
        if eid in seen_ids:
            errors.append(f"{prefix}: duplicate id {eid!r}")
        seen_ids.add(eid)

        prefix = f"templates[{i}] ({eid})"

        name = entry["name"]
        if not isinstance(name, str) or not name or len(name) > MAX_NAME_CHARS:
            errors.append(f"{prefix}: name must be a non-empty string ≤ {MAX_NAME_CHARS} chars")

        if entry["category"] not in ALLOWED_CATEGORIES:
            errors.append(f"{prefix}: category must be one of {sorted(ALLOWED_CATEGORIES)}")

        description = entry["description"]
        if not isinstance(description, str) or not description or len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{prefix}: description must be a non-empty string ≤ {MAX_DESCRIPTION_CHARS} chars")

        expected_html = f"{REPO_BASE_URL}/templates/{eid}.html"
        expected_thumb = f"{REPO_BASE_URL}/templates/{eid}.png"
        if entry["html_url"] != expected_html:
            errors.append(f"{prefix}: html_url must be {expected_html}")
        if entry["thumbnail_url"] != expected_thumb:
            errors.append(f"{prefix}: thumbnail_url must be {expected_thumb}")

        variables = entry["variables"]
        if not isinstance(variables, list) or not all(isinstance(v, str) for v in variables):
            errors.append(f"{prefix}: variables must be an array of strings")
        else:
            for v in variables:
                if v in BUILTIN_VARIABLES:
                    errors.append(f"{prefix}: variable {v!r} is built-in, don't declare it")

        html_path = repo_root / "templates" / f"{eid}.html"
        thumb_path = repo_root / "templates" / f"{eid}.png"

        if not html_path.is_file():
            errors.append(f"{prefix}: missing file templates/{eid}.html")
        else:
            html = html_path.read_text(errors="replace")
            if SCRIPT_TAG.search(html):
                errors.append(f"{prefix}: html contains a <script> tag")

        if not thumb_path.is_file():
            errors.append(f"{prefix}: missing file templates/{eid}.png")
        elif thumb_path.stat().st_size > MAX_THUMBNAIL_BYTES:
            kb = thumb_path.stat().st_size // 1024
            errors.append(f"{prefix}: thumbnail is {kb}KB, max is {MAX_THUMBNAIL_BYTES // 1024}KB")

    templates_dir = repo_root / "templates"
    if templates_dir.is_dir():
        for file in templates_dir.iterdir():
            if file.suffix in {".html", ".png"} and file.stem not in seen_ids:
                errors.append(f"orphan file: templates/{file.name} has no entry in index.json")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print(f"OK — {len(seen_ids)} template(s) valid")


if __name__ == "__main__":
    main()
