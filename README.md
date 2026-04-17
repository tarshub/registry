# TarsHub Registry

The community registry for [TarsHub](https://tarshub.com) — agent context packages that make any AI coding tool smarter about your stack.

## What is a TarsHub package?

A TarsHub package is a collection of plain-text context files (`AGENTS.md`, `.cursor/rules/`, task prompts) bundled for a specific tech stack. Install one, and your AI coding agent instantly knows your conventions, patterns, and workflows.

Packages work with **any agent** — Cursor, Claude Code, Windsurf, and more.

## How packages are stored here

Each listed package has a **single manifest file** named `tarshub.json`. The **folders under `packages/` mirror the GitHub repo path** (owner, repo, optional subfolders for a subdirectory package). Examples:

- `packages/johndoe/react-tailwind-configs/tarshub.json`
- `packages/PatrickJS/awesome-cursorrules/rules/htmx-flask/tarshub.json`

The leaf name is always `tarshub.json` (not `<repo-name>.json`). The automated **`_index.json`** file is rebuilt on every push to `main` by collecting every `packages/**/tarshub.json`.

## Install a package

```bash
npx tarshub install @johndoe/react-tailwind-configs
npx tarshub install @PatrickJS/awesome-cursorrules/rules/htmx-flask
```

Or browse and download from [tarshub.com](https://tarshub.com).

## Submit a package

Anyone can submit a public GitHub repo (or a subdirectory within one) to TarsHub. No account needed.

1. Go to [tarshub.com/publish](https://tarshub.com/publish)
2. Paste the GitHub URL (repo or subdirectory)
3. Done — your package will appear on TarsHub within minutes

**Examples of URLs you can submit:**
- `https://github.com/johndoe/react-tailwind-configs`
- `https://github.com/PatrickJS/awesome-cursorrules/tree/main/rules/htmx-flask`

### Optional: add a `tarshub.json` in your repo

Adding a `tarshub.json` to your repo (or subdirectory) is **optional** but gives you richer metadata and listing control. When present, publish stores the same JSON under the matching path in this registry, with `repo` set to the full GitHub slug (`owner/repo` or `owner/repo/nested/path`).

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

Without `tarshub.json` in your repo, TarsHub uses your repo's description and topics from GitHub and still writes a generated `tarshub.json` here.

### Opt out

If you don't want your repo listed on TarsHub, add a `tarshub.json` with `"listed": false`:

```json
{
  "listed": false
}
```

Then re-submit the URL at [tarshub.com/publish](https://tarshub.com/publish) to remove it.

| Scenario | Result |
|----------|--------|
| No `tarshub.json` in repo | **Listed** — metadata from GitHub API, manifest generated here |
| `tarshub.json` exists, no `listed` field | **Listed** — metadata from the file |
| `tarshub.json` has `"listed": true` | **Listed** |
| `tarshub.json` has `"listed": false` | **Delisted** — `packages/.../tarshub.json` removed |

**Allowed file types:** `.md`, `.mdc`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`
**Max file size:** 50 KB per file &bull; **Max package size:** 500 KB &bull; **Max files:** 50

## License

[MIT](LICENSE)
