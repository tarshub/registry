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

1. Create a public GitHub repo with your context files
2. Add a `tarshub.json` at the root:

```json
{
  "name": "my-package-name",
  "description": "Short description of what this context package is for",
  "keywords": ["nextjs", "supabase", "saas"],
  "version": "1.0.0",
  "listed": true,
  "files": [
    "AGENTS.md",
    ".cursor/rules/general.mdc",
    "tasks/add-feature.md"
  ]
}
```

3. Go to [tarshub.com/publish](https://tarshub.com/publish) and paste your repo URL

That's it. Your package will appear on TarsHub within minutes.

**Allowed file types:** `.md`, `.mdc`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`
**Max file size:** 50 KB per file &bull; **Max package size:** 500 KB &bull; **Max files:** 50

## Consent & listing control

The `tarshub.json` file in your repo is your consent to be listed on TarsHub. No account or login is needed.

| Scenario | Result |
|----------|--------|
| `tarshub.json` exists, no `listed` field | **Listed** (default) |
| `tarshub.json` has `"listed": true` | **Listed** |
| `tarshub.json` has `"listed": false` | **Delisted** — submit the URL again on [tarshub.com/publish](https://tarshub.com/publish) to remove your package |
| `tarshub.json` doesn't exist | **Rejected** — cannot be added to TarsHub |

You control your listing entirely from your own repo. No one else can list or delist your package because only you can change `tarshub.json` in your repository.

## License

[MIT](LICENSE)
