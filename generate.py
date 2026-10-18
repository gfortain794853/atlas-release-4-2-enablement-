"""Generate customer release notes from changelog.yaml.

Usage:  python generate.py [path/to/changelog.yaml]
"""
import sys
from pathlib import Path

import yaml

# Every entry must have these fields, or the script stops with a clear message.
REQUIRED = ["id", "title", "type", "breaking", "audience", "visibility", "description"]

# What the customer should do, by change type.
# A type that isn't listed here falls back to DEFAULT_ACTION.
ACTIONS = {
    "api_deprecation": "Migrate to the replacement as soon as possible.",
    "api_change": "Update any integration affected by this change.",
    "config_change": "No action required. Review the new default and override it if it doesn't suit your organization.",
    "ui_change": "None.",
    "feature": "No action required. Enable the feature if you want it.",
}
DEFAULT_ACTION = "Review this change and decide whether it affects you."


def load_changelog(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for change in data["changes"]:
        missing = [key for key in REQUIRED if key not in change]
        if missing:
            sys.exit(f"Entry {change.get('id', '?')} is missing: {', '.join(missing)}")
    return data


def audience_text(audience):
    text = ", ".join(f"{a}s" for a in audience)  # [developer, partner] -> "developers, partners"
    return text[0].upper() + text[1:]


def render_entry(change):
    what = " ".join(change["description"].split())  # tidy the line breaks
    if change.get("default") in (False, "off"):      # YAML reads unquoted "off" as False
        what += " It is off by default."
    action = ACTIONS.get(change["type"], DEFAULT_ACTION)
    lines = [
        f"### {change['title']}",
        "",
        f"**Who this affects:** {audience_text(change['audience'])}",
        "",
        f"**What changed:** {what}",
        "",
        f"**Action required:** {action}",
        "",
    ]
    if "removal_release" in change:
        lines += [
            f"<!-- REVIEW BEFORE PUBLISHING: {change['id']} gives removal_release "
            f"{change['removal_release']}. Check it against the description before "
            f"stating a release number. -->",
            "",
        ]
    return "\n".join(lines)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "changelog.yaml"
    data = load_changelog(path)

    external = [c for c in data["changes"] if c["visibility"] == "external"]
    breaking = [c for c in external if c["breaking"]]
    other = [c for c in external if not c["breaking"]]

    d = data["release_date"]  # YAML turns an unquoted date into a date object
    date_text = d if isinstance(d, str) else f"{d.day} {d:%B %Y}"

    parts = [f"# {data['product']} {data['release']} Release Notes", "", f"Release date: {date_text}", ""]
    if breaking:
        parts += ["## Breaking changes", ""] + [render_entry(c) for c in breaking]
    if other:
        parts += ["## Other changes", ""] + [render_entry(c) for c in other]

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)
    (out_dir / "release_notes.md").write_text("\n".join(parts), encoding="utf-8")

    skipped = len(data["changes"]) - len(external)
    print(f"Wrote output/release_notes.md: {len(breaking)} breaking, {len(other)} other, {skipped} internal skipped.")


if __name__ == "__main__":
    main()