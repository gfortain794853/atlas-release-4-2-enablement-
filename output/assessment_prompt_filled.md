You are an instructional designer writing a short multiple-choice assessment for customer admins on a software release.

## Release

Atlas Knowledge 4.2, releasing 30 November 2026

## Competencies (every question must be tied to one of these)

**The admin can...**

| # | Competency | Changes covered | Level |
|---|------------|-----------------|-------|
| 1 | override new default SSO session timeout | C2 | Apply |
| 2 | explain Search API v1 deprecation, move to v2, added `locale` value requirement | C1 | Know |
| 3 | enable citations for AI Answers in a portal | C4 | Apply |
| 4 | confirm integrations that read `article_id` are updated for payload v2 | C6 | Apply |

## Changes you may use

These are the only facts you may use. Do not add details from your own knowledge of similar products.

- Title: Search API v1 deprecated
  Breaking: yes
  Audience: developer, partner
  Description: GET /v1/search is deprecated. Use GET /v2/search, which requires a locale query parameter (for example en-US). v1 remains supported through release 4.4.

- Title: Default SSO session timeout reduced
  Breaking: no
  Audience: admin, partner
  Description: The default SSO session timeout changes from 8 hours to 1 hour for new and existing tenants. Admins can override it under Settings > Security > Session.

- Title: Publish button moved to top toolbar
  Breaking: no
  Audience: author
  Description: In the Author Console, Publish moves from the article footer to the top toolbar. No behavior change.

- Title: Citations in AI Answers
  Breaking: no
  Audience: admin, partner, prospect
  Description: AI Answers can show the source articles behind each answer. Enable it per portal under AI Answers > Display > Show citations.
  Off by default: yes

- Title: Webhook payload v2 for article.published
  Breaking: yes
  Audience: developer, partner
  Description: The article.published webhook now sends payload v2. The integer field article_id is replaced by the string field article_uuid. Integrations that parse article_id must be updated.

## Rules

1. Write exactly 5 questions. Every question is tied to one competency by its number.
2. At least 2 questions must be scenarios (a short situation, then "what should you do?" or "what is the most likely cause?"). Label each question "(scenario)" or "(knowledge)".
3. Match the level of the competency: "Know" competencies ask the learner to explain; "Apply" competencies ask what to do; "Troubleshoot" competencies start from a symptom.
4. Each question has 4 options (A to D) and exactly one correct answer. Wrong options must be plausible to someone who half-remembers the release, for example using details from a different change. No "all of the above" or "none of the above".
5. Spread the correct answers across A, B, C and D. Do not put the correct answer in the same position more than twice.
6. The rationale is ONE sentence and must be supported by the change descriptions above.
7. Never state which release removes a deprecated feature, or until which release it is supported. The source is unclear on this.
8. Never mention internal flag names, change IDs (like C1) or engineering details. Customers do not see them.
9. Refer to a replaced field by the names given in the change descriptions, and never make a question depend on how a field name is spelled.
10. Use the product's own terms exactly as written in the descriptions (for example "AI Answers", "Show citations"). Put field names, endpoints and parameters in backticks.
11. If something is unclear or missing in the descriptions, do not guess. Leave it out of the questions.
12. Copy the competency text exactly as written in the table.
13. No two questions may test the same fact.
14. At least one wrong option per question must be a near-miss from the same change, not a detail from an unrelated change.

## Output format

Output only Markdown, in exactly this shape, with a blank line between every field:

# Atlas Knowledge 4.2: Assessment

## Question 1 (scenario)

**Competency:** #[NUMBER], [competency text]

**Question:** [the question]

- A. [option]
- B. [option]
- C. [option]
- D. [option]

**Answer:** [letter]

**Rationale:** [one sentence]

Repeat for questions 2 to 5. Add no other text before or after.