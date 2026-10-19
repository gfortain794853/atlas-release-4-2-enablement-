# Atlas Knowledge 4.2: Assessment

## Question 1 (scenario)

**Competency:** #1, override new default SSO session timeout

**Question:** After the 4.2 release, your support agents are signed out after one hour. Before the release they stayed signed in for eight hours, and your team wants to keep eight hours. What should you do?

- A. Nothing, because the new one-hour default applies only to new tenants, so your existing tenant is not affected.
- B. Override the default session timeout under Settings > Security > Session.
- C. Turn the setting on per portal under Settings > Display > AI Answers.
- D. Wait for the next release, when the default goes back to eight hours.

**Answer:** B

**Rationale:** The default SSO session timeout drops from 8 hours to 1 hour for new and existing tenants, and admins can override it under Settings > Security > Session.

## Question 2 (knowledge)

**Competency:** #2, explain Search API v1 deprecation, move to v2, added `locale` value requirement

**Question:** A partner developer asks what they need to change when they move from Search API v1 to v2. What should you tell them?

- A. Replace the integer `article_id` with the string `article_uuid` in search requests.
- B. Call `GET /v2/search` with the same parameters as before. Nothing else changes.
- C. Keep calling `GET /v1/search`, but add a `locale` query parameter.
- D. Call `GET /v2/search` and include a `locale` query parameter, for example `en-US`.

**Answer:** D

**Rationale:** `GET /v1/search` is deprecated, and its replacement `GET /v2/search` requires a `locale` query parameter such as `en-US`.

## Question 3 (scenario)

**Competency:** #3, enable citations for AI Answers in a portal

**Question:** A customer wants AI Answers in their help portal to show the source articles behind each answer. They upgraded to 4.2, but no sources appear. What should you do?

- A. Turn on Show citations for that portal under AI Answers > Display > Show citations.
- B. Nothing. Citations appear automatically in every portal after the upgrade.
- C. Turn on Show citations once to apply it to every portal in the tenant.
- D. Ask authors to republish their articles using Publish in the top toolbar.

**Answer:** A

**Rationale:** Citations in AI Answers are off by default and are enabled per portal under AI Answers > Display > Show citations.

## Question 4 (scenario)

**Competency:** #4, confirm integrations that read `article_id` are updated for payload v2

**Question:** Before the 4.2 release, you review your integrations. One of them listens for the `article.published` webhook and reads `article_id`. What should you do?

- A. Nothing, because the 4.2 publishing change only moves the Publish button and does not change behavior.
- B. Confirm the integration now gets `article_id` from `GET /v2/search` instead of the webhook.
- C. Confirm the integration is updated for payload v2, where the integer `article_id` is replaced by the string `article_uuid`.
- D. Confirm the integration now reads `article_id` as a string instead of an integer.

**Answer:** C

**Rationale:** The `article.published` webhook now sends payload v2, which replaces the integer `article_id` with the string `article_uuid`, so integrations that parse `article_id` must be updated.

## Question 5 (knowledge)

**Competency:** #2, explain Search API v1 deprecation, move to v2, added `locale` value requirement

**Question:** A customer admin asks what the Search API v1 deprecation means for integrations that still call `GET /v1/search`. Which explanation is correct?

- A. `GET /v1/search` has stopped working, so those integrations can no longer search until they switch.
- B. `GET /v1/search` is deprecated but still supported, and integrations should move to `GET /v2/search`.
- C. `GET /v1/search` requires a `locale` query parameter that is not necessary after the update.
- D. The change is not breaking, so no integration needs to move to `GET /v2/search`.

**Answer:** B

**Rationale:** `GET /v1/search` is deprecated but remains supported, and integrations should move to `GET /v2/search`.
