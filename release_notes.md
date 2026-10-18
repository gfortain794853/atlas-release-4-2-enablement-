# Atlas Knowledge 4.2 Release Notes
Release date: 30 November 2026

## Breaking changes

### Search API v1 deprecated

**Who this affects:** Developers, partners

**What changed:** `GET /v1/search` is deprecated. Use `GET /v2/search`, which requires a `locale` value in the query (for example: en-US). `GET /v1/search` will be removed in a future release. 

**Action required:** Migrate to v2 as soon as possible.

<!-- REVIEW BEFORE PUBLISHING: C1 source conflict. The changelog gives removal_release 4.3, but its description says v1 stays supported through release 4.4. Specific release number removed from the notes to avoid conflict. Confirm with the product team, then add the removal release number. -->


### Webhook payload v2 for article.published

**Who this affects:** Developers, partners

**What changed:** The `article.published` webhook now sends payload v2. The integer field
`article_id` has been replaced by the string field `article_uuid`.

**Action required:** Update integrations that parse `article_id` to read `article_uuid`.

<!-- REVIEW BEFORE PUBLISHING: the sample webhook file spells the field articleId, but the changelog says article_uuid. Notes reflect information in the changelog. The changelog also doesn't describe the availability of the old payload -->

## Other changes

### Default SSO session timeout reduced

**Who this affects:** Admins, partners

**What changed:** The default SSO session timeout changes from 8 hours to 1 hour for
new and existing tenants.

**Action required:** No action required. The default SSO session timeout can be changed in Settings > Security > Session. 

<!-- REVIEW BEFORE PUBLISHING: the changelog doesn't say if tenants that already set a custom timeout keep it. -->

### Publish button moved to top toolbar

**Who this affects:** Authors

**What changed:** In the Author Console, Publish moves from the article footer to the top toolbar. Behavior is unchanged.

**Action required:** None.

### Citations in AI Answers

**Who this affects:** Admins, partners, prospects

**What changed:** AI Answers can show the source articles behind each answer. Citations in AI Answers are off by default.

**Action required:** No action required. This functionality can be enabled per portal under AI Answers > Display > Show citations.