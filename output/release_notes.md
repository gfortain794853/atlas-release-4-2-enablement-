# Atlas Knowledge 4.2 Release Notes

Release date: 30 November 2026

## Breaking changes

### Search API v1 deprecated

**Who this affects:** Developers, partners

**What changed:** `GET /v1/search` is deprecated. Use `GET /v2/search`, which requires a `locale` query parameter (for example `en-US`). It will be removed in a future release.

**Action required:** Migrate to the replacement named above as soon as possible.

<!-- REVIEW BEFORE PUBLISHING: C1 gives removal_release 4.3. The description also said: "v1 remains supported through release 4.4." The notes say only 'a future release' until the product team confirms which. -->

### Webhook payload v2 for article.published

**Who this affects:** Developers, partners

**What changed:** The `article.published` webhook now sends payload v2. The integer field `article_id` is replaced by the string field `article_uuid`.

**Action required:** Integrations that parse `article_id` must be updated.

## Other changes

### Default SSO session timeout reduced

**Who this affects:** Admins, partners

**What changed:** The default SSO session timeout changes from 8 hours to 1 hour for new and existing tenants. Admins can override it under Settings > Security > Session.

**Action required:** No action required. Review the new default and override it if it doesn't suit your organization.

### Publish button moved to top toolbar

**Who this affects:** Authors

**What changed:** In the Author Console, Publish moves from the article footer to the top toolbar. No behavior change.

**Action required:** None.

### Citations in AI Answers

**Who this affects:** Admins, partners, prospects

**What changed:** AI Answers can show the source articles behind each answer. Enable it per portal under AI Answers > Display > Show citations. It is off by default.

**Action required:** No action required. Enable the feature if you want it.
