---
name: docs-development
description: >-
  Contribute to the Alchemyst-ai docs Mintlify documentation site. Add, update,
  or fix MDX documentation pages, manage docs.json navigation, run local
  preview and link validation, and understand auto-generation pipelines for
  API reference, community agents, and sitemap. Triggers on: "add a doc page",
  "update documentation", "fix a broken link in docs", "update the sidebar
  navigation", "regenerate API reference docs", "add an integration guide".
  Does not trigger on: questions about the Alchemyst platform API itself,
  generic Mintlify questions, or requests about the ignore/ example directory.
---

## Activation

When this skill is active, output:
`USING docs-development SKILL — [current action]`

## Scope and exclusions

**In scope:**
- Creating, updating, or fixing MDX documentation pages under `developer-docs/`
- Updating `developer-docs/docs.json` navigation to surface new or moved pages
- Maintaining the directory map in `developer-docs/README.md`
- Running local preview (`mint dev`) and link validation (`mint broken-links`)
- Following commit conventions (`docs(scope): summary`) and PR template
- Understanding which files are auto-generated and must not be hand-edited

**Out of scope:**
- Explaining the Alchemyst platform API, SDKs, or integrations (read the documentation content directly)
- Hand-editing auto-generated files (API reference endpoint MDX, sitemap.xml, community agent pages)
- Working with the `ignore/` directory (reference/example project, not part of the docs workflow)
- Deploying the docs site (handled automatically by Mintlify on push to main)

## Inputs

- The change request (new page, update, fix, navigation change)
- Target directory and file path within `developer-docs/`
- Whether the change affects navigation (new, moved, or renamed pages)

## Workflow

### 1. Understand the documentation structure

The docs site lives in `developer-docs/` with content in MDX files. Navigation is
defined in `developer-docs/docs.json` under `navigation.tabs[].groups[].pages[]`.

Key content directories:
- `getting-started/` — Getting started and quickstart guides
- `api-reference/` — API introduction plus auto-generated endpoint pages
- `integrations/` — SDK, third-party, data source, extension, and context proxy guides
- `advanced/` — Advanced usage, context arithmetic, usage patterns, troubleshooting
- `tutorials/` — Step-by-step tutorials (MCP setup, Chrome extension, n8n, agents)
- `mcps/` — MCP setup guides for Claude Desktop, Cursor, VS Code
- `changelog/` — Product and platform changelogs
- `example-projects/` — Team and community example projects
- `contribution/` — Contributing guide and awesome-saas repo link
- `self-hosting/` — Enterprise self-hosting guide

### 2. Create or modify an MDX page

Every MDX page requires frontmatter with at least `title` and `description`:

```yaml
---
title: "Page Title"
description: "Short description for SEO and search"
keywords: ['keyword1', 'keyword2']
---
```

Use Mintlify components for rich content:
- `<Card>` / `<CardGroup cols={2}>` — Navigation cards with `title`, `href`, `icon` or `img`
- `<Steps>` / `<Step title="...">` — Step-by-step guides
- `<Tabs>` / `<Tab title="...">` — Tabbed code examples
- `<CodeGroup>` — Grouped code blocks with language labels (e.g., ```bash npm, ```bash python)
- `<AccordionGroup>` / `<Accordion title="...">` — Collapsible sections
- `<Note>` / `<Warning>` / `<Info>` — Callout boxes
- `<Frame>` — Image frames with rounded corners
- `<Columns cols={2}>` — Multi-column layouts

For multi-language code samples (TypeScript/Python), use `<CodeGroup>` or `<Tabs>` with
consistent examples across both languages.

### 3. Update navigation in docs.json

When adding, moving, or renaming a page, update `developer-docs/docs.json`:
- Find the appropriate tab in `navigation.tabs[]` (e.g., "Guides", "Integrations", "API reference")
- Find or create the appropriate group in `groups[]`
- Add the page path (without `.mdx` extension, relative to `developer-docs/`) to `pages[]`
- Nested groups use objects with `group` and `pages` keys

Example page entry: `"getting-started/quickstart"` (no extension, relative to `developer-docs/`)

### 4. Update the directory map

When adding or removing files, update the directory map in `developer-docs/README.md`
under the "Directory map" section to reflect the current file structure.

### 5. Validate locally

Run the Mintlify dev server to preview:
```bash
cd developer-docs
mint dev
```
Open `http://localhost:3000` to verify the page renders, links work, and images load.

Validate links:
```bash
mint broken-links
```

Quality checks:
- Verify page renders without errors
- Check for broken links
- Verify heading hierarchy (one H1 per page, sentence case)
- Ensure code blocks have language fences
- Check internal links use relative paths
- Verify images include alt text

### 6. Commit and PR

- Branch naming: `docs/your-topic`
- Commit style: `docs(scope): short summary` (e.g., `docs(ai-context): add diagram`)
- Follow `.github/pull_request_template.md` checklist
- Include screenshots for visual changes
- Pull latest from `main` before pushing

## Auto-generation pipelines (do not hand-edit)

Three pipelines run automatically via GitHub Actions. Files they produce are
overwritten on the next run.

**API reference** — `.github/workflows/update-openapi.yaml`:
- `developer-docs/action.js` orchestrates: delete existing endpoint MDX, fetch
  latest OpenAPI spec from the platform backend via `developer-docs/ctx.js`,
  generate MDX files for paths containing "context", and update `docs.json`
- Key functions: `action.js:deleteAllAutogenFiles`, `action.js:generateMdx`,
  `action.js:createApiReferenceMdxFiles`, `action.js:generateNewDocsJson`
- Platform URLs: `ctx.js:PLATFORM_BASE_URLS` (staging vs main)
- Do not hand-edit files under `developer-docs/api-reference/endpoint/`
- To change generation behavior, modify `action.js` or `ctx.js`

**Community agents** — `.github/workflows/fetch-community-agents.yaml`:
- `fetch_agents.js` fetches README.md files from `alchemyst-ai/awesome-saas`
  under `agents/*/`, saves them as `.mdx` in
  `developer-docs/example-projects/community/`, and updates `docs.json`
- Do not hand-edit files under `developer-docs/example-projects/community/`

**Sitemap** — `.github/workflows/sitemap.yml`:
- `developer-docs/scripts/generate-sitemap-from-docsjson.mjs` reads `docs.json`,
  collects navigation routes, and generates `developer-docs/sitemap.xml`
- Do not hand-edit `developer-docs/sitemap.xml`

## Composition rules

This is a cross-cutting development companion. It is the sole skill for this
repository and triggers alone for all repository-artifact work. No task skills
co-trigger because API reference sync, community agent sync, and sitemap
generation are CI-automated maintenance pipelines whose procedures are documented
as conditional sections above.

For pure explanation or diagnosis of the Alchemyst platform API, no skill
activates—read the documentation content directly.

## Validation

- `mint dev` renders the page without errors at `http://localhost:3000`
- `mint broken-links` reports no broken links
- `docs.json` is valid JSON with the new page in the correct tab/group
- Frontmatter includes `title`, `description`, and `keywords`
- Commit message follows `docs(scope): summary` convention
- Directory map in `developer-docs/README.md` reflects added/removed files

## Failure handling

- If `mint dev` fails to start: ensure Node.js 18+ and `npm i -g mint` are installed
- If `mint broken-links` reports errors: fix the referenced links or add redirects in `docs.json` `redirects` array
- If a page does not appear in the sidebar: verify it is listed in `docs.json` navigation under the correct tab and group
- If the page renders but components are missing: check Mintlify component syntax (capitalized tags, self-closing where needed)
- If `mint dev` uses an unexpected port: port 3000 is default; Mintlify auto-increments if occupied

## Freshness triggers

This skill becomes stale when:
- The Mintlify CLI version or component syntax changes
- `docs.json` navigation structure is reorganized (new tabs, renamed groups)
- New auto-generation pipelines are added or existing ones are modified
- The `developer-docs/` directory structure is significantly reorganized
- The commit convention or PR template changes

## Source index

- `developer-docs/docs.json` — Mintlify configuration: navigation, theme, SEO, redirects, banner, fonts, logo, navbar, footer, integrations
- `developer-docs/README.md` — Contributor guide with directory map, setup, quality checks, commit and PR process
- `CONTRIBUTING.md` — High-level contribution process
- `.github/pull_request_template.md` — PR checklist with content, style, technical, and risk sections
- `developer-docs/contribution/contributing.mdx` — Detailed contributing guide with MDX tips, structure rules, validation, and troubleshooting
- `developer-docs/action.js` — API reference auto-generation: `deleteAllAutogenFiles`, `generateMdx`, `createApiReferenceMdxFiles`, `generateNewDocsJson`
- `developer-docs/ctx.js` — Platform API utilities: `fetchOpenApiJson`, `PLATFORM_BASE_URLS`
- `fetch_agents.js` — Community agent README sync from `alchemyst-ai/awesome-saas` repo
- `.github/workflows/update-openapi.yaml` — Daily cron and push-to-main OpenAPI sync
- `.github/workflows/fetch-community-agents.yaml` — Daily cron community agent sync
- `.github/workflows/sitemap.yml` — Push-to-main sitemap generation
- `developer-docs/scripts/generate-sitemap-from-docsjson.mjs` — Sitemap generator reading docs.json navigation
- `developer-docs/index.mdx` — Landing page with Mintlify component examples (Card, CardGroup, Steps, Tabs)
- `developer-docs/getting-started/quickstart.mdx` — Quickstart with CodeGroup, Tabs, AccordionGroup, Note patterns
