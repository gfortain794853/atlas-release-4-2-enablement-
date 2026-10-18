# 15-minute module: Getting ready for Atlas Knowledge 4.2

**Audience:** customer admins, plus developers and authors on their teams.
**Format:** live or recorded walkthrough with a short hands-on exercise.
**Prep:** Python 3 installed; the repo open; `output/release_notes.md` open in a second window.

## Learning objectives
By the end, an admin can:
1. Name the breaking changes in 4.2 and the action each needs (COMP-1)
2. Describe how to move a search call from v1 to v2 (COMP-2)
3. Find and fix a webhook handler broken by payload v2 (COMP-3)
4. Decide whether to keep or override the new SSO session timeout (COMP-4)
5. Say whether Citations is on, and where an admin turns it on; tell authors where Publish moved (COMP-5)

## Timing
| Time | Segment | Competency |
|---|---|---|
| 0:00 – 1:30 | Opening: three buckets | COMP-1 |
| 1:30 – 4:30 | Breaking change: Search API v1 deprecated (C1) | COMP-2 |
| 4:30 – 6:30 | Breaking change: webhook payload v2 (C6) | COMP-3 |
| 6:30 – 8:00 | Behavior change: SSO session timeout (C2) | COMP-4 |
| 8:00 – 9:00 | New: Citations (C4) and Publish button (C3) | COMP-5 |
| 9:00 – 14:00 | Hands-on exercise (A and B) | COMP-2, COMP-3 |
| 14:00 – 15:00 | Wrap-up and the 5-question check | all |

## Script

**Opening (0:00 – 1:30)**
"Release 4.2 ships on 2026-11-30. Six things changed; one is internal, so you will hear about five. Sort them into three buckets. *Breaking*: your integrations can fail, so you must act. That is C1 and C6. *Review*: not breaking, but your users will notice, so you must decide. That is C2. *New*: nothing to do unless you want it. That is C3 and C4. The release notes follow these same three buckets."

**Search API v1 deprecated, C1 (1:30 – 4:30)**
- "GET /v1/search is deprecated. *Deprecated* means it still works today but has an end date. Do not read it as 'already broken' or as 'safe to ignore'."
- "The replacement is GET /v2/search. The one new rule: v2 **requires a `locale` parameter**, written like `en-US`."
- "Plan to finish before release 4.3." (Show the sample request in `samples/search_v2_request.json` and point at the path and the locale.)
- Ask the room: "Who owns the code that calls search? That person needs this slide."

**Webhook payload v2, C6 (4:30 – 6:30)**
- "The `article.published` webhook now sends payload v2. The ID changed from an integer called `article_id` to a string called `article_uuid`."
- "Any code that reads `article_id` will fail. The failure looks like a parsing error in code nobody touched. If you see that after the release, check this change first."
- Show `samples/webhook_article_published_v2.json`: `payload_version` is 2.

**SSO session timeout, C2 (6:30 – 8:00)**
- "The default session timeout drops from 8 hours to 1 hour. It applies to **new and existing tenants**, so your users will be signed out sooner without you doing anything."
- "You can override it under Settings > Security > Session. Decide on purpose: keep 1 hour, or set your own value that matches your security policy."

**Citations and Publish button, C4 and C3 (8:00 – 9:00)**
- "Citations lets AI Answers show the source articles behind an answer. It is **off by default** (flag `ai_answers_citations`). To turn it on for a portal: AI Answers > Display > Show citations."
- "Authors: Publish moved from the article footer to the top toolbar in the Author Console. Same behavior, new place."

## Hands-on exercise (9:00 – 14:00, about 5 minutes)
You will fix two things the way you would after a real release. Copy the sample first so the original stays intact:
`cp samples/search_v2_request.json exercises/my_request.json`

**A. Check a v2 search request (about 2 min)**
1. Run `python exercises/check_search_request.py exercises/my_request.json`
2. Read what it reports. Open `exercises/my_request.json` and fix the problem.
3. Run the check again until it says `OK`.

**B. Fix a webhook handler (about 3 min)**
1. Run `python exercises/webhook_handler.py samples/webhook_article_published_v2.json`
2. It fails. Read the message: which field does it say is missing, and which fields does the payload actually have?
3. Edit `get_article_id()` in `exercises/webhook_handler.py` so it returns the ID from the v2 payload. In v2 the ID is text, not a number, so remove `int(...)`.
4. Run it again until it says `OK`.

**Answers (facilitator)**
- A: the sample has `locale=enUS`; change it to `locale=en-US`.
- B: the sample's ID field is spelled `articleId`, so `return payload["articleId"]` passes the check.

## Wrap-up (14:00 – 15:00)
"Three things to take away: act on C1 and C6, decide on C2, and enable C4 only when you are ready. Take the 5-question check in `output/assessment.md`; it covers all five skills."

## Facilitator notes: resolve before delivering
- **Field name conflict.** The changelog (C6) says the new field is `article_uuid`. The webhook sample uses `articleId`. The exercise is written to work with the sample as given, but learners will notice. Confirm the real field name with the product owner and fix the sample or the changelog.
- **Locale in the sample.** The changelog example is `en-US`; the sample request uses `enUS`. Exercise A treats this as the bug to fix. If `enUS` is actually accepted by the API, replace Exercise A with a different check.
- **Removal date.** C1 says removal in 4.3 but also "supported through release 4.4". The script says "before 4.3" (the cautious reading). Confirm which is right.
- **Timing is tight.** If you run long, move Exercise B to homework and cut the C3/C4 segment to 30 seconds.
