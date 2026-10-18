# Atlas Knowledge 4.2: Admin Training Module (15 min)

## 1. Welcome and overview (1 min)

## 2. SSO session timeout (3 min)

**Competency practised:** #1, override the default SSO session timeout
<!-- Competency 1, change C2 -->

**Say:** In 4.2, the default SSO session timeout drops from 8 hours to 1 hour. That applies to new and existing tenants. If 1 hour doesn't suit your organization, an admin can override it under Settings > Security > Session. 

**Show:** The "Default SSO session timeout reduced" entry from the release notes. Then a slide with the path: Settings > Security > Session.

**Check:** How can the default SSO session timeout be changed? 

**Answer:** Go to Settings > Security > Session

## 3. Citations in AI Answers (2 min)

**Competency practised:** #3, enable citations for AI Answers in a portal 
<!-- Competency 3, change C4 -->

**Say:** In 4.2, AI Answers can show the source articles behind each answer. It is, by default, off. It can be enabled per portal under AI Answers > Display > Show citations.

**Show:** The "Citations in AI Answers" entry from the release notes. Then a slide with the path: AI Answers > Display > Show citations.

**Check:** An author wants to know why answers in their portal don't show source articles after the update. What do you tell them?

**Answer:** Citations in AI Answers is off by default in 4.2. To turn them on, enable them (per portal) via AI Answers > Display > Show citations.


## 4. Search API v1 to v2 (3 min)

**Competency Practiced:** explain Search API v1 deprecation, move to v2, added `locale` value requirement
<!-- Competency 2, change C1 -->

**Say:** In 4.2, `GET /v1/search` is deprecated. It still works for now, but it will be removed in a future release. The replacement is `GET /v2/search`, which needs a `locale` value in the query (for example, `en-US`).

***Show:** The "Search API v1 deprecated" entry from the release notes. Then a slide with the two endpoints side by side: `GET /v1/search` (deprecated) and `GET /v2/search` (requires `locale`).

**Check:** A developer on your team asks what the 4.2 change means for their integration. What do you tell them?

**Answer:** `GET /v1/search` is deprecated. They should move to `GET /v2/search` and add a `locale` value to the query.

<!-- TRAINER NOTE: the changelog gives removal_release 4.3 but says v1 is supported through release 4.4, so no removal release is stated here. The sample request uses locale=enUS, while the changelog's example is en-US. Confirm both with the product team. -->
<!-- Note: The changelog's removal release (4.3) directly conflicts with the description's (4.4). -->

## 5. Hands-on exercise: Is our integration ready for payload v2? (5 min)

**Competency practised:** #4, confirm integrations that read `article_id` are updated for payload v2
<!-- Competency 4, change C6 -->

**Scenario:** Your team has an integration that reads the `article.published` webhook and records each article's ID. It was written for payload v1. Before 4.2 ships, you've been asked to confirm that it will cope with payload v2.

**Material:** `samples/webhook_article_published_v2.json` and the "Webhook payload v2 for article.published" entry in the release notes

**Task:**
1. Open the sample payload and find the field that holds the article's ID.
2. Say whether its value is a number or text.
3. The integration reads a field called `article_id`. Say what it will find in this payload.
4. Write one sentence telling your developer what must change.

**Answer key:**
1. The field is `articleId`. (The release notes call the new field `article_uuid`, but the provided sample uses `articleId`. Use the name in the sample.)
2. Text. It's a string like `a7c9e2f4-...`, not a number.
3. Nothing. The payload has no `article_id` field, so the integration won't find an ID.
4. "Read the new string ID field (`articleId` in the sample) instead of `article_id`."

**Common mistakes:**
- Assuming the ID is still a number.
- Expecting the old field name to still be in the payload.

**Debrief (1 minute):** the integration was written for v1, so it looks for a field that v2 no longer sends. Checking a v2 sample against what your code reads is a quick way to confirm readiness before release.

### Extension (optional, not part of the 15 minutes): prove it by running it

For learners who want to test the fix, or for a developer on the team. Do this after the main exercise.

**Material:** `exercises/webhook_handler.py`

**Task:**
1. Run the handler against the v2 sample:

   ```
   python exercises/webhook_handler.py samples/webhook_article_published_v2.json
   ```

   It fails and lists the fields the payload does have.
2. Edit `get_article_id()` so it returns the ID from the v2 payload. Run the command again until you see `OK`.

**Hint:** the field has a different name in v2, and its value is no longer a number.

**Answer key:** the corrected function is:

```python
def get_article_id(payload):
    return payload["articleId"]
```

Keeping `int(...)` causes a conversion error, because the ID is text. Reading `article_uuid` (the release notes' name) causes the "no field" message again, because the sample doesn't contain it.

<!-- TRAINER NOTE: the release notes name the new field article_uuid, but the provided sample uses articleId. The exercise follows the sample as given. Confirm the real field name with the product team before delivering. -->

## 6. Recap (1 min)