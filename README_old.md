<div align="center">
  <h1>Alchemyst-ai Docs</h1>
  <p><strong>The central hub for all Alchemyst-ai documentation.</strong></p>

  <p>
    <a href="https://github.com/Alchemyst-ai/docs/stargazers"><img src="https://img.shields.io/github/stars/Alchemyst-ai/docs?style=social" alt="GitHub stars"></a>
    <a href="https://github.com/Alchemyst-ai/docs/network"><img src="https://img.shields.io/github/forks/Alchemyst-ai/docs?style=social" alt="GitHub forks"></a>
    <a href="https://github.com/Alchemyst-ai/docs/graphs/contributors"><img src="https://img.shields.io/github/contributors/Alchemyst-ai/docs" alt="Contributors"></a>

  </p>
</div>

---

## 📜 Table of Contents

* [✅ Project Overview](#-project-overview)
* [🚀 Features](#-features)
* [📦 Tech Stack](#-tech-stack)
* [📁 Folder Structure](#-folder-structure)
* [🛠️ Getting Started](#️-getting-started)
* [🧑‍💻 Contributing](#-contributing)
* [📄 License](#-license)

---

## ✅ Project Overview

Welcome to the official documentation repository for `Alchemyst-ai`! This monorepo is the single source of truth for all documentation related to our projects, APIs, and tools. We believe in the power of clear, concise, and accessible information, and this repository is our commitment to empowering our users and developers.

Our documentation is primarily written in **MDX**, allowing us to combine the readability of Markdown with the power and interactivity of JSX components, creating a rich and engaging learning experience.

---

## 📦 Tech Stack

This documentation site is built with modern, developer-friendly technologies:

* **[MDX](https://mdxjs.com/):** For writing content that combines Markdown and JSX.
* **[Node.js](https://nodejs.org/):** For the development environment and server-side logic.
* **[Mintlify CLI](https://www.npmjs.com/package/mint)**

---

## 📁 Folder Structure

Here is a basic overview of the directory layout in this monorepo:

```bash
├── .github/              # Community health files (e.g., CODE_OF_CONDUCT.md)
├── developer-docs/
├─ README.md
├─ docs.json
├─ index.mdx
├─ quickstart.mdx
├─ development.mdx
├─ api-reference/
│  ├─ introduction.mdx
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

---

## 🛠️ Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

* Node.js (v18 or higher recommended)
* npm or yarn

### Installation

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

---

## 🧑‍💻 Contributing

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

</br>
 
 Note: Before pushing or opening a PR, pull the latest changes from `main`.

---

## 📄 License

Distributed under the CC BY-SA 4.0 License. See `LICENSE` for more information.

---
