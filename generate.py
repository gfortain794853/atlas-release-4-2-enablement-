"""Regenerate the Atlas release notes and assessment from changelog.yaml.

Usage:
    python generate.py [path/to/changelog.yaml]
    python generate.py --check path/to/assessment.md     (validate an assessment only)

What it does:
  1. Writes output/release_notes.md (plain Python, no AI).
  2. Fills prompts/assessment_prompt.md with the external changes and the
     competency map, and saves it as output/assessment_prompt_filled.md.
  3. If ANTHROPIC_API_KEY is set, sends that prompt to the model and saves the
     reply. Otherwise you paste the filled prompt into any AI tool and save the
     reply as output/assessment.md.
  4. Checks the assessment against the rules and reports any problems.
"""
import os
import re
import sys
from pathlib import Path

import yaml

MODEL = "claude-opus-5-5"
OUT_DIR = Path("output")
PROMPT_TEMPLATE = Path("prompts/assessment_prompt.md")
COMPETENCY_MAP = Path("competency_map.md")
ASSESSMENT_SOURCE = OUT_DIR / "assessment_source.md"   # the prompt the current assessment was made from

# Every entry must have these fields, or the script stops with a clear message.
REQUIRED = ["id", "title", "type", "breaking", "audience", "visibility", "description"]

# What the customer should do, by change type.
# A type that isn't listed here falls back to DEFAULT_ACTION.
ACTIONS = {
    "api_deprecation": "Migrate to the replacement named above as soon as possible.",
    "api_change": "Update any integration affected by this change.",
        "config_change": "Review the new default before the release date, and override it if it doesn't suit your organization.",
    "ui_change": "None.",
    "feature": "No action required. Enable the feature if you want it.",
}
DEFAULT_ACTION = "Review this change and decide whether it affects you."


# ---------- reading the changelog ----------

def load_changelog(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for change in data["changes"]:
        missing = [key for key in REQUIRED if key not in change]
        if missing:
            sys.exit(f"Entry {change.get('id', '?')} is missing: {', '.join(missing)}")
        if change["visibility"] not in ("external", "internal"):
            sys.exit(f"Entry {change['id']} has visibility '{change['visibility']}'. Use external or internal.")
    return data


def is_external(change):
    # Only entries explicitly marked external are customer-facing.
    return change["visibility"] == "external"


def audience_text(audience):
    text = ", ".join(f"{a}s" for a in audience)  # [developer, partner] -> "developers, partners"
    return text[0].upper() + text[1:]


def date_text(d):
    # YAML turns an unquoted date into a date object, so format it ourselves.
    return d if isinstance(d, str) else f"{d.day} {d:%B %Y}"


# ---------- release notes ----------

# Things that should look like code: endpoints, snake_case names, dotted names, locale codes.
CODE_RE = re.compile("|".join(f"(?:{p})" for p in [
    r"\b(?:GET|POST|PUT|PATCH|DELETE) /[\w/{}.-]*\w",   # GET /v2/search
    r"\b[a-z]+(?:_[a-z0-9]+)+\b",                       # article_id
    r"\b[a-z]{3,}\.[a-z]{3,}\b",                        # article.published
    r"\b[a-z]{2}-[A-Z]{2}\b",                           # en-US
]))
NOT_A_PARAMETER = {"a", "an", "the", "any", "each", "one", "this", "that", "no"}
RELEASE_MENTION = re.compile(r"\brelease\s+\d+(?:\.\d+)*", re.I)


def code_format(text):
    """Put backticks around endpoints, field names and parameters."""
    text = CODE_RE.sub(lambda m: f"`{m.group(0)}`", text)
    # "requires a locale query parameter" -> "requires a `locale` query parameter"
    def wrap_parameter(m):
        word = m.group(1)
        return word if word.lower() in NOT_A_PARAMETER else f"`{word}`"
    return re.sub(r"(?<![`\w])(\w+)(?= query parameter)", wrap_parameter, text)


def split_sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if s]


def prepare_entry(change):
    """Work out the 'What changed' text, the action line, and any sentences we dropped."""
    has_removal = "removal_release" in change
    kept, dropped, obligation = [], [], None
    for sentence in split_sentences(change["description"]):
        if has_removal and RELEASE_MENTION.search(sentence):
            dropped.append(sentence)   # never state a removal or support release
        elif obligation is None and re.search(r"\bmust\b", sentence):
            obligation = sentence      # an obligation becomes the action line
        else:
            kept.append(sentence)
    if not kept and obligation:
        kept.append(obligation)        # don't leave "What changed" empty
    if has_removal:
        kept.append("It will be removed in a future release.")
    what = " ".join(kept)
    default = change.get("default")
    default_on = default in (True, "on")             # YAML reads unquoted on/off as True/False
    if default in (False, "off"):
        what += " It is off by default."
    elif default_on:
        what += " It is on by default."
    action = obligation or ACTIONS.get(change["type"], DEFAULT_ACTION)
    if not obligation and default_on and change["type"] == "feature":
        action = "No action required."              # don't tell people to enable what is already on
    return code_format(what), code_format(action), dropped


def render_entry(change):
    what, action, dropped = prepare_entry(change)
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
        note = f"{change['id']} gives removal_release {change['removal_release']}."
        if dropped:
            note += f" The description also said: \"{' '.join(dropped)}\""
        note += " The notes say only 'a future release' until the product team confirms which."
        lines += [f"<!-- REVIEW BEFORE PUBLISHING: {note} -->", ""]
    return "\n".join(lines)


def write_release_notes(data):
    external = [c for c in data["changes"] if is_external(c)]
    breaking = [c for c in external if c["breaking"]]
    other = [c for c in external if not c["breaking"]]

    parts = [
        f"# {data['product']} {data['release']} Release Notes",
        "",
        f"Release date: {date_text(data['release_date'])}",
        "",
    ]
    if breaking:
        parts += ["## Breaking changes", ""] + [render_entry(c) for c in breaking]
    if other:
        parts += ["## Other changes", ""] + [render_entry(c) for c in other]

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "release_notes.md").write_text("\n".join(parts), encoding="utf-8")
    skipped = len(data["changes"]) - len(external)
    print(f"Wrote output/release_notes.md: {len(breaking)} breaking, {len(other)} other, {skipped} internal skipped.")


# ---------- assessment prompt ----------

def changes_for_prompt(data):
    """Describe the external changes for the AI. Internal ones never get here."""
    blocks = []
    for c in data["changes"]:
        if not is_external(c):
            continue
        lines = [
            f"- Title: {c['title']}",
            f"  Breaking: {'yes' if c['breaking'] else 'no'}",
            f"  Audience: {', '.join(c['audience'])}",
            f"  Description: {' '.join(c['description'].split())}",
        ]
        if c.get("default") in (False, "off"):
            lines.append("  Off by default: yes")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def competency_numbers(map_text):
    # Table rows look like: | 1 | override ... | C2 | Apply |
    return {int(n) for n in re.findall(r"(?m)^\|\s*(\d+)\s*\|", map_text)}


def build_prompt(data):
    for needed in (PROMPT_TEMPLATE, COMPETENCY_MAP):
        if not needed.exists():
            sys.exit(f"Missing {needed}. Run the script from the repo's top folder.")
    prompt = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    values = {
        "{{RELEASE}}": f"{data['product']} {data['release']}, releasing {date_text(data['release_date'])}",
        "{{PRODUCT}}": data["product"],
        "{{VERSION}}": str(data["release"]),
        "{{COMPETENCIES}}": COMPETENCY_MAP.read_text(encoding="utf-8").strip(),
        "{{CHANGES}}": changes_for_prompt(data),
    }
    for placeholder, text in values.items():
        prompt = prompt.replace(placeholder, text)
    return prompt


def call_model(prompt):
    """Return the model's reply, or None if no API key / SDK is available."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
    except ImportError:
        print("ANTHROPIC_API_KEY is set but the 'anthropic' package is missing: pip install anthropic")
        return None
    client = anthropic.Anthropic()
    reply = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    return reply.content[0].text


# ---------- checking the assessment ----------

def validate_assessment(text, data):
    """Return a list of problems. An empty list means the assessment passes."""
    problems = []
    map_numbers = competency_numbers(COMPETENCY_MAP.read_text(encoding="utf-8")) if COMPETENCY_MAP.exists() else set()
    blocks = re.split(r"(?m)^## Question ", text)[1:]

    if len(blocks) != 5:
        problems.append(f"Expected 5 questions, found {len(blocks)}.")

    scenarios = 0
    for block in blocks:
        head = block.splitlines()[0]
        m = re.match(r"(\d+) \((scenario|knowledge)\)", head)
        if not m:
            problems.append(f"Question heading '{head}' should look like '1 (scenario)'.")
            continue
        label, kind = f"Question {m.group(1)}", m.group(2)
        scenarios += kind == "scenario"

        comp = re.search(r"\*\*Competency:\*\* #(\d+)", block)
        if not comp:
            problems.append(f"{label}: missing '**Competency:** #N'.")
        elif map_numbers and int(comp.group(1)) not in map_numbers:
            problems.append(f"{label}: competency #{comp.group(1)} is not in the competency map.")

        options = re.findall(r"(?m)^- ([A-D])\. ", block)
        if options != ["A", "B", "C", "D"]:
            problems.append(f"{label}: needs four options '- A.' to '- D.' as a list.")
        answer = re.search(r"\*\*Answer:\*\* ([A-D])\b", block)
        if not answer:
            problems.append(f"{label}: missing '**Answer:** <letter>'.")
        rationale = re.search(r"\*\*Rationale:\*\* (.+)", block)
        if not rationale:
            problems.append(f"{label}: missing '**Rationale:**' with a colon.")
        elif len(re.findall(r"[.!?](\s|$)", rationale.group(1).strip())) > 1:
            problems.append(f"{label}: rationale should be one sentence.")

    if blocks and scenarios < 2:
        problems.append(f"Need at least 2 scenario questions, found {scenarios}.")

    # Things customers must never see.
    lowered = text.lower()
    for c in data["changes"]:
        if re.search(rf"\b{re.escape(c['id'])}\b", text):
            problems.append(f"Mentions change ID {c['id']}; customers never see IDs.")
        if not is_external(c):
            if c["title"].lower() in lowered or re.search(rf"\b{re.escape(c['id'])}\b", text):
                problems.append(f"Mentions internal change {c['id']} ({c['title']}).")
        elif c.get("feature_flag") and c["feature_flag"] in text:
            problems.append(f"Shows the internal flag name {c['feature_flag']}.")
        if c.get("removal_release") and re.search(rf"release {re.escape(str(c['removal_release']))}\b", text, re.I):
            problems.append(f"States removal release {c['removal_release']}; the source is unclear on it.")
    # Also catch phrases like "supported through release 4.4" or "removed in release 4.3".
    for hit in re.findall(r"(?:through|until|removed in|removal in)\s+(?:release\s+)?\d+\.\d+", text, re.I):
        problems.append(f"States a release for removal/support ('{hit}'); the source is unclear on it.")
    return problems


def report(problems):
    if problems:
        print("Assessment check: FAILED")
        for p in problems:
            print("  -", p)
    else:
        print("Assessment check: OK (5 questions, scenarios, options, answers, rationales, no internal details).")


# ---------- main ----------

def main():
    args = sys.argv[1:]
    if args and args[0] == "--check":
        path = args[1] if len(args) > 1 else str(OUT_DIR / "assessment.md")
        data = load_changelog("changelog.yaml")
        problems = validate_assessment(Path(path).read_text(encoding="utf-8"), data)
        report(problems)
        if not problems:
           ASSESSMENT_SOURCE.write_text(build_prompt(data), encoding="utf-8")
        return

    data = load_changelog(args[0] if args else "changelog.yaml")
    write_release_notes(data)

    OUT_DIR.mkdir(exist_ok=True)
    prompt = build_prompt(data)
    (OUT_DIR / "assessment_prompt_filled.md").write_text(prompt, encoding="utf-8")
    print("Wrote output/assessment_prompt_filled.md")

    reply = call_model(prompt)
    if reply is not None:
        problems = validate_assessment(reply, data)
        target = OUT_DIR / ("assessment.md" if not problems else "assessment_DRAFT.md")
        target.write_text(reply, encoding="utf-8")
        if not problems:
            ASSESSMENT_SOURCE.write_text(prompt, encoding="utf-8")
        print(f"Wrote {target}")
        report(problems)
        return

    existing = OUT_DIR / "assessment.md"
    if existing.exists():
        if not ASSESSMENT_SOURCE.exists() or ASSESSMENT_SOURCE.read_text(encoding="utf-8") != prompt:
            print("WARNING: changelog.yaml or competency_map.md changed since this assessment was made. Regenerate it.")
        print("No API key set, so the existing assessment was not regenerated. Checking it instead:")
        report(validate_assessment(existing.read_text(encoding="utf-8"), data))
    else:
        print("No API key set. Paste output/assessment_prompt_filled.md into an AI tool,")
        print("save the reply as output/assessment.md, then run: python generate.py --check")


if __name__ == "__main__":
    main()