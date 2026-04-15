# TarsHub Registry

The community registry for [TarsHub](https://tarshub.com) — agent context packages that make any AI coding tool smarter about your stack.

## What is a TarsHub package?

A TarsHub package is a collection of plain-text context files (`AGENTS.md`, `.cursor/rules/`, task prompts) bundled for a specific tech stack. Install one, and your AI coding agent instantly knows your conventions, patterns, and workflows.

Packages work with **any agent** — Cursor, Claude Code, Windsurf, and more.

## Install a package

```bash
npx tarshub install @johndoe/nextjs-supabase-saas
```

Or browse and download from [tarshub.com](https://tarshub.com).

## Publish a package

### 1. Create a public repo with your context files

Your repo must have a `tarshub.json` at the root:

```json
{
  "name": "my-package-name",
  "description": "Short description of what this context package is for",
  "keywords": ["nextjs", "supabase", "saas"],
  "version": "1.0.0",
  "files": [
    "AGENTS.md",
    ".cursor/rules/general.mdc",
    "tasks/add-feature.md"
  ]
}
```

**Allowed file types:** `.md`, `.mdc`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`
**Max file size:** 50 KB per file &bull; **Max package size:** 500 KB &bull; **Max files:** 50

### 2. Submit to this registry

Fork this repo, add a JSON file named `<your-github-username>__<package-name>.json`:

```json
{
  "name": "my-package-name",
  "repo": "your-username/your-repo-name",
  "description": "Short description of what this context package is for",
  "tags": ["nextjs", "supabase", "saas"]
}
```

Open a PR. A GitHub Action will validate your submission and auto-merge it if everything checks out.

### Submission rules

- Filename must follow the format `<your-github-username>__<package-name>.json`
- You can only add or modify files that start with your own GitHub username
- The repo in your submission must be public and contain a valid `tarshub.json`
- One file per package — submit multiple files if you have multiple packages

## How it works

```
Developer publishes         User installs
  their own repo              via CLI or tarshub.com
       │                            │
       ▼                            ▼
  PR to this registry ──→  _index.json (auto-built)
       │                            │
       ▼                            ▼
  GitHub Action validates    CLI fetches files from
  and auto-merges            developer's repo via GitHub CDN
```

No servers. No databases. Just GitHub.

## License

[MIT](LICENSE)
