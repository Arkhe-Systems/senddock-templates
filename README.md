# SendDock Templates

Community-maintained library of starter email templates for [SendDock](https://senddock.dev).

Every SendDock instance (Cloud and self-hosted) loads this manifest at runtime to power the **Browse library** modal on the templates page. Pick a template, click *Use template*, and SendDock clones it into your project — ready to edit.

```
GET https://raw.githubusercontent.com/Arkhe-Systems/senddock-templates/main/index.json
```

## How it works

- `index.json` — manifest with metadata for every template (id, name, category, thumbnail, html URL, declared variables).
- `templates/<id>.html` — the actual HTML body. Must use Handlebars variables.
- `templates/<id>.png` — the preview thumbnail shown in the gallery.

SendDock backends cache the manifest in Redis for 1 hour, so changes here propagate to all instances within an hour without any redeploy.

## Contributing

PRs are open and welcome — one PR per template. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the format, HTML rules, thumbnail specs, and review checklist.

This is the only SendDock repo that accepts external code contributions. The core engine at [Arkhe-Systems/senddock](https://github.com/Arkhe-Systems/senddock) is core-team-only by design.

## License

All templates and code in this repo are released under the [MIT License](./LICENSE). Use them anywhere, modify freely, no attribution required.

SendDock itself is AGPL-3.0.
