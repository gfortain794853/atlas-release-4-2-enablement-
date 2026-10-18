# Atlas Knowledge 4.2 Release Notes

Release date: 30 November 2026

## Breaking changes

### Search API v1 deprecated

**Who this affects:** Developers, partners

**What changed:** GET /v1/search is deprecated. Use GET /v2/search, which requires a locale query parameter (for example en-US). v1 remains supported through release 4.4.

**Action required:** Migrate to the replacement as soon as possible.

### Webhook payload v2 for article.published

**Who this affects:** Developers, partners

**What changed:** The article.published webhook now sends payload v2. The integer field article_id is replaced by the string field article_uuid. Integrations that parse article_id must be updated.

**Action required:** Update integrations that use this API.

## Other changes

### Default SSO session timeout reduced

**Who this affects:** Admins, partners

**What changed:** The default SSO session timeout changes from 8 hours to 1 hour for new and existing tenants. Admins can override it under Settings > Security > Session.

**Action required:** Review the new default and override it if it doesn't suit you.

### Publish button moved to top toolbar

**Who this affects:** Authors

**What changed:** In the Author Console, Publish moves from the article footer to the top toolbar. No behavior change.

**Action required:** No action required.

### Citations in AI Answers

**Who this affects:** Admins, partners, prospects

**What changed:** AI Answers can show the source articles behind each answer. Enable it per portal under AI Answers > Display > Show citations.

**Action required:** No action required. This feature is optional.
