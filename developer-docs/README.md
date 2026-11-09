# Alchemyst Developer Documentation

This directory contains the Alchemyst developer docs built with Mintlify.

## Prerequisites

- Node.js 18+ recommended
- [Mintlify CLI](https://www.npmjs.com/package/mint)

Install the CLI globally:

```
npm i -g mint
```

## Local development

Run the dev server :

```
cd developer-docs
```

```
mint dev
```

Then open `http://localhost:3000`.

### Directory map

```
developer-docs/
├─ README.md
├─ docs.json
├─ index.mdx
├─ quickstart.mdx
├─ development.mdx
├─ api-reference/
│  ├─ introduction.mdx
│  ├─ chat-completions.mdx
│  ├─ models/
│  │  └─ index.mdx
│  ├─ openapi.json
│  └─ endpoint/api/v1/
│     └─ context/
│        ├─ add/post.mdx
│        ├─ delete/post.mdx
│        ├─ search/post.mdx
│        ├─ traces/{traceId}/delete/delete.mdx
│        └─ view/
│           ├─ get.mdx
│           └─ docs/get.mdx
├─ ai-context/
│  ├─ what-is-ai-context.mdx
│  ├─ why-you-need-ai-context.mdx
│  └─ how-alchemyst-works.mdx
├─ essentials/
│  ├─ code.mdx
│  ├─ images.mdx
│  ├─ markdown.mdx
│  ├─ navigation.mdx
│  ├─ reusable-snippets.mdx
│  └─ settings.mdx
├─ integrations/
│  ├─ introduction.mdx
│  ├─ sdk/
│  │  ├─ typescript-sdk.mdx
│  │  └─ python-sdk.mdx
│  └─ third-party/
│     ├─ agnoagi/python.mdx
│     ├─ aisdk/js.mdx
│     ├─ langchain/{js,python}.mdx
│     └─ llamaindex/{js,python}.mdx
├─ example-projects/
│  ├─ introduction.mdx
│  └─ team/
│     ├─ syllabai.mdx
│     └─ zendocs.mdx
├─ mcps/
│  ├─ introduction.mdx
│  ├─ mcps.mdx
│  ├─ cursor.mdx
│  ├─ claude-desktop.mdx
│  └─ visual-studio-code.mdx
├─ snippets/
│  └─ snippet-intro.mdx
├─ images/
│  └─ ...
├─ logo/
│  └─ ...
├─ action.js
└─ ctx.js
```

## Contributors guide

### 1) Setup

- Fork and clone the repo
- Create a feature branch from `main`: `git checkout -b docs/your-topic`
- Install Mintlify CLI (see prerequisites) and run locally with `mint dev`

### 2) MDX quick tips

- Check how mdx works you can see some examples in `/essentials`

### 3) Structure and navigation

- Place new pages in the most relevant directory (e.g., `ai-context/`, `integrations/`).
- For API docs, follow `api-reference/endpoint/api/v1/...` folder conventions.
- Update `docs.json` to surface new sections/pages in the sidebar navigation.

### 4) Quality checks

- Run: `mint dev` and verify the page renders, links work, and images load
- Lint/content sanity: check for broken links, heading hierarchy, and typos
- Keep line length readable; wrap long lines and avoid trailing spaces

### 5) Commit and PR

- Commit style: `docs(scope): short summary` (e.g., `docs(ai-context): add diagram`)
- When adding files, update the Directory map in this README (`developer-docs/README.md`).
- Push your branch and open a PR to `main`
- In the PR description: include screenshots of visual changes and a brief summary
- Request review from a maintainer; address feedback promptly

### 6) After merge

- If everything goes well and your PR is merged to `main`, you will see it at `https://docs.getalchemystai.com/`.
- If issues arise, submit a follow-up PR with focused fixes

<br />

 Note: Before pushing or opening a PR, pull the latest changes from `main`.

## Resources

- Mintlify docs: https://mintlify.com/docs
- Mintlify community: https://mintlify.com/community
