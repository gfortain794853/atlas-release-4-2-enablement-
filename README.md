# Atlas Knowledge 4.2: release enablement

Take-home for the AI Engineer, Learning & Development role. It turns the 4.2 changelog into customer release notes, a 15-minute training module and an assessment, with a pipeline that regenerates the notes and assessment from `changelog.yaml`. All content is fictional.

## What is where

| # | Deliverable | File |
|---|---|---|
| 1 | Competency map | `competency_map.md` |
| 2 | Customer release notes | `output/release_notes.md` (generated) |
| 3 | 15-minute module | `training_module.md`, with an optional extension in `exercises/webhook_handler.py` |
| 4 | Assessment | `output/assessment.md` (AI-generated, then reviewed by me) |
| 5 | Regeneration pipeline | `generate.py` and `prompts/assessment_prompt.md` |
| 6 | AI log | `ai_log.md` |
| 7 | README | this file |

`samples/` and `changelog.yaml` are the starter files, unchanged except for formatting of C4 due to copy/paste from PDF. `drafts/` holds my hand-written release notes and assessment, which I used as the reference for what good looks like.

## Tools used

Claude Opus 5.5 (claude.ai chat) for explaining the brief, reviewing my drafts, and helping with the script and prompt. Python 3 with PyYAML, VS Code and Git. Details are in `ai_log.md`.

## How to run

From the repo's top folder:

```
pip install pyyaml
python generate.py
```

This writes `output/release_notes.md` and `output/assessment_prompt_filled.md`. To add a change, append an entry to `changelog.yaml` and run it again. A missing required field stops the script with a message naming the entry.

The assessment has an AI step:

- **With an API key:** set `ANTHROPIC_API_KEY` and `pip install anthropic`. The script sends the prompt, checks the reply, and saves it as `output/assessment.md`, or as `output/assessment_DRAFT.md` if the check fails.
- **Without a key (how I ran it):** paste `output/assessment_prompt_filled.md` into an AI tool, save the reply as `output/assessment.md`, then run `python generate.py --check`.

## How the pipeline works

- **Release notes:** plain Python, no AI, so the output is repeatable. Only entries with `visibility: external` are included, so a typo can never leak an internal change. Breaking changes come first. The action line comes from a "must" sentence in the description, or from a lookup by change type. Endpoints and field names get backticks.
- **Never states a release for removal or support.** The source conflicts on this (see below), so entries with `removal_release` say "a future release" and leave a review comment recording the conflict.
- **Assessment:** the script filters internal changes out of the prompt in code, fills in the changes and the competency map, and checks the reply: 5 questions, at least 2 scenarios, four options, an answer and a one-sentence rationale each, and no internal changes, flag names or release numbers.
- **YAML quirks handled:** an unquoted `off` loads as `False` (the "Norway problem"), and an unquoted date loads as a date object.

## Assumptions

- The competency map is written for the customer admin only, even for developer-facing changes. It has four competencies. C3 (Publish button) needs no admin action, so it appears in the notes only. C5 is internal and excluded everywhere.
- The pipeline also reads `competency_map.md`, because the changelog has no competencies.
- A type change from `article_id` to `article_uuid` breaks integrations that read the old field. The changelog only says they "must be updated."
- Learner-facing text refers to changes by title, never by ID (C1 to C6), since customers never see the IDs. I corrected places in the module that used IDs.
- The audience terms are not defined. "Partner" could be a non-technical reseller, so I wrote the module for a potentially less technical audience. The main exercise needs no code. The webhook script is an optional extension for developers.
- The samples are used exactly as given. The exercise follows the sample (`articleId`) and the answer key explains the mismatch.

## Unclear in the source material

- The brief says 4.2 ships "in two weeks," but the changelog date is later. I used the changelog date.
- The webhook sample spells the field `articleId`, but the changelog says `article_uuid`.
- The search sample uses `locale=enUS`, while the changelog gives `en-US` only as an example. I could not tell whether this is deliberate or whether the API accepts both, so I left the sample unchanged and flagged it.
- C1 gives removal in release 4.3 but also says v1 is "supported through release 4.4."
- C1 does not say how a customer can tell whether they still use v1, for example whether there is usage reporting.
- C1 is `breaking: true` although v1 keeps working. I followed the flag. C2 changes behavior immediately for existing tenants but is `breaking: false`, so the meaning of "breaking" needs confirming.
- C2 does not say whether tenants that already set a custom timeout keep it.
- C6 does not say whether the old payload stays available.
- C4's title and `type` ran together in the PDF, so I rebuilt the YAML. The indentation was also lost.
- "Prospect" is listed as a C4 audience, but prospects are not customers and may never see the notes.

## Limits

- The API path in `generate.py` was never run, because I had no key.
- The checker tests structure and rules only. It cannot judge whether a wrong option is plausible or a rationale is true, so a person has to read the questions.
- The generated notes are plainer than my hand-written ones in `drafts/`. Review flags that come from judgment, such as the C6 sample mismatch, cannot be generated.
- Sentences are split on full stops, so an abbreviation like "e.g." can confuse the "must" rule in an unusual description.
- The competency map is hand-written. A new change only appears in the assessment once a competency covering it is added to the map.

## With more time

- Add an AI rewriting step for the release notes, with its own checker, and tests for the generator.
- Compare field names in the sample files against the changelog, which would produce the C6 flag automatically.
- Add a prompt rule that wrong options include a near-miss from the same change.
- Confirm the open questions above ("Unclear in the source material") with the product team before publishing.
