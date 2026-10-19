# Atlas Knowledge 4.2: Assessment

## Question 1 (scenario)

**Competency:** #1, override the default SSO session timeout

**Question:** Your tenant has been live for two years. After upgrading to 4.2, users complain that they are asked to sign in far more often, and your security policy allows longer sessions. What should you do?

- A. Nothing. Existing tenants keep their old 8-hour default.
- B. Override the default under Settings > Security > Session.
- C. Turn off SSO so that sessions no longer expire.
- D. Change the setting under AI Answers > Display.

**Answer:** B

**Rationale:** In 4.2 the default SSO session timeout drops from 8 hours to 1 hour for new and existing tenants, and admins can override it under Settings > Security > Session.

## Question 2 (knowledge)

**Competency:** #2, explain the Search API v1 deprecation, the move to v2, and the new `locale` requirement

**Question:** Which statement best describes the Search API change in 4.2?

- A. `GET /v1/search` has been removed and now returns an error.
- B. `GET /v2/search` is deprecated, so integrations should keep using v1.
- C. `GET /v1/search` is deprecated, and `GET /v2/search` takes no extra parameters.
- D. `GET /v1/search` is deprecated, and `GET /v2/search` replaces it and requires a `locale` query parameter.

**Answer:** D

**Rationale:** The release notes say `GET /v1/search` is deprecated and that `GET /v2/search` requires a `locale` query parameter.

## Question 3 (scenario)

**Competency:** #3, enable citations for AI Answers on a portal

**Question:** The owner of your help portal wants AI Answers to show the source articles behind each answer, but nothing appears after the 4.2 upgrade. What do you do?

- A. Enable citations for that portal under AI Answers > Display > Show citations.
- B. Nothing. Citations are on by default, so clear the portal's cache.
- C. Enable citations once, and every portal switches on automatically.
- D. Change the default under Settings > Security > Session.

**Answer:** A

**Rationale:** Citations are off by default and are enabled per portal under AI Answers > Display > Show citations.

## Question 4 (scenario)

**Competency:** #4, confirm that integrations reading `article_id` are updated for payload v2

**Question:** Since the 4.2 release, an integration on your team that handles the `article.published` webhook can't find an article's ID, and nobody has changed its code. What most likely caused this?

- A. The webhook no longer sends article IDs at all.
- B. Payload v2 still sends `article_id`, but now as a string instead of an integer.
- C. Payload v2 replaces the integer field `article_id` with a string field.
- D. The webhook was deprecated and replaced by `GET /v2/search`.

**Answer:** C

**Rationale:** In 4.2, the `article.published` webhook sends payload v2, which replaces the integer field `article_id` with a string field, so integrations that parse `article_id` must be updated.

## Question 5 (scenario)

**Competency:** #2, explain the Search API v1 deprecation, the move to v2, and the new `locale` requirement

**Question:** A developer on your team asks what a search call must look like after moving to v2. What do you tell them?

- A. Keep calling `GET /v1/search` and add a `payload_version` value.
- B. Call `GET /v2/search` and include a `locale` value, for example `en-US`.
- C. Call `GET /v2/search` with no other changes.
- D. Replace `article_id` with a string field in the request.

**Answer:** B

**Rationale:** `GET /v2/search` requires a `locale` query parameter, so a v2 call must include one as well as use the new endpoint.
