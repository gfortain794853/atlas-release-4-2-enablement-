# Atlas Knowledge 4.2: Assessment

## Question 1 (scenario)

**Competency:** #1, override the default SSO session timeout
<!-- Change C2 -->

**Question:** After the 4.2 upgrade, users on your tenant are asked to sign in again after about an hour. Your organization's security policy allows longer sessions. What should you do?

- A. Nothing. The session timeout can't be changed.
- B. Override the default under Settings > Security > Session.
- C. Turn off SSO for the tenant.
- D. Wait for the next release to restore the old default.

**Answer:** B

**Rationale:** 4.2 lowers the default SSO session timeout from 8 hours to 1 hour, and admins can override it under Settings > Security > Session.

## Question 2 (knowledge)

**Competency:** #2, explain the Search API v1 deprecation, the move to v2, and the new `locale` requirement
<!-- Change C1 -->

**Question:** A developer on your team is moving a search call from `GET /v1/search` to `GET /v2/search`. According to the release notes, which value must the new request include?

- A. A `payload_version` value
- B. A `portal` value
- C. An `article_id` value
- D. A `locale` value

**Answer:** D

**Rationale:** The release notes say `GET /v2/search` requires a `locale` query parameter, for example `en-US`.

## Question 3 (scenario)

**Competency:** #3, enable citations for AI Answers on a portal
<!-- Change C4 -->

**Question:** A portal owner asks why answers on their portal don't show source articles after release 4.2. The release notes say citations are off by default. What do you tell them?

- A. An admin must turn citations on for that portal under AI Answers > Display > Show citations.
- B. It's a bug. Citations should be on for every portal automatically.
- C. Citations switch on by themselves 30 days after the release.
- D. Only Atlas staff can turn citations on.

**Answer:** A

**Rationale:** Citations are off by default and are enabled per portal under AI Answers > Display > Show citations.

## Question 4 (scenario)

**Competency:** #4, confirm integrations that read `article_id` are updated for payload v2
<!-- Change C6 -->

**Question:** Your team has an integration that reads `article_id` from the `article.published` webhook. What do the 4.2 release notes say about it?

- A. Nothing needs to change, because the webhook is unchanged.
- B. It's fine as long as it also sends a `locale` value.
- C. It must be updated, because payload v2 replaces the integer field `article_id` with a string field.
- D. It must be updated, but only if the SSO session timeout is changed.

**Answer:** C

**Rationale:** The release notes say payload v2 replaces the integer field `article_id` with a string field, so integrations that parse `article_id` must be updated.

## Question 5 (scenario)

**Competency:** #4, confirm integrations that read `article_id` are updated for payload v2
<!-- Change C6 -->

**Question:** Since the 4.2 release, an integration on your team that handles the `article.published` webhook reports that it can't find an article's ID. Nobody has changed the integration's code. What is the most likely cause?

- A. The default SSO session timeout dropped to 1 hour.
- B. Payload v2 replaced the integer field `article_id`, which the integration reads, with a string field.
- C. Citations in AI Answers are off by default.
- D. `GET /v1/search` was deprecated.

**Answer:** B

**Rationale:** In 4.2, the `article.published` webhook sends payload v2, which replaces the integer field `article_id` with a string field, so integrations that parse `article_id` must be updated.