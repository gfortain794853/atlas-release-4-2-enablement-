# AI log

**Tools:** Claude Opus 5.5 (claude.ai chat) to explain the brief, review my drafts, `generate.py`, and structure the assessment prompt. VS Code and Git for the repo. I wrote the competency rows, release-note entries and module sections myself first, then had Claude review them.

## Main prompts


1. "How's this?" on each draft (competencies, notes, module sections, questions).
2. Script prompt: "Write a Python 3 script that reads changelog.yaml and writes customer release notes to output/release_notes.md ... Do not include any changes with visibility: internal ... keep it brief and pythonic. leave lots of comments." The script was reviewed and minor edits made.
3. Small fixes: "Fix the spacing on this yaml" and "Check my indentation on lines 22-45", etc.
4. Ran the filled prompt (`output/assessment_prompt_filled.md`) through Claude to produce the questions.
5. Finding gaps in the assessment rules to improve assessment quality

## Where I changed or questioned AI output

**1. C1 competency.** Claude suggested "identify which integrations still call v1." I asked how an admin would do that. The changelog mentions no usage report, so the wording assumed a feature that is not in the source. I reworded it to explaining the deprecation and listed the gap in the README.

**2. "Including".** Claude's wording said "including the new `locale` requirement," which implied other changes. I pointed out the source lists only one and switched to a closed list.

**3. Too specific.** The competency rows had grown to repeat menu paths and field names. I said they were no shorter than the YAML and cut them to a verb and an object.

**4. Audience.** Claude rephrased "deprecated" in the notes. I checked whether partners would understand it. Because "partner" is undefined, I kept the term and added a plain explanation.

**5. Webhook exercise.** Claude suggested a script as the module's exercise. The audience includes less technical partners, so I made the main exercise code-free and kept the script as an extension.

**6. IDs vs titles.** Part of the module referred to changes by ID, which customers never see. I switched to titles.

**7. Release notes, C1.** The generated text copied "supported through release 4.4," which conflicts with `removal_release: 4.3`. I chose to state neither. The script now says "a future release" and leaves a review comment.

**8. Sample mismatch.** The sample says `articleId`, the changelog says `article_uuid`. I left the sample alone and put the explanation in the answer key.

**9. Generated assessment.** The checker passes.

**10. Pipeline testing.** Testing with invented entries showed a feature with `default: on` being told "Enable the feature if you want it." It was fixed.

## Not trusted without checking

I compared the generated notes with my hand-written ones in `drafts/`. A person still has to read the generated questions. The API path in `generate.py` was never run.




