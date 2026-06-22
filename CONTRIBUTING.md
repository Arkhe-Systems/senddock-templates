# Contributing a template

Thanks for adding to the library — this is how the SendDock community gets more starter templates.

**Rule of thumb: one template per PR.** Easier to review, easier to revert, easier to credit.

## Quick start

1. Fork this repo and check out `main`.
2. Pick a short, kebab-case `id` for your template (e.g. `welcome-minimal`, `newsletter-monthly-digest`).
3. Add three things:
   - `templates/<id>.html` — the email body
   - `templates/<id>.png` — the 600×400 preview thumbnail
   - One new entry in `index.json` describing it
4. Run `python3 scripts/validate.py` locally to catch errors before pushing.
5. Open a PR.

## HTML rules

| Rule | Why |
|---|---|
| No `<script>` tags | Email clients strip them anyway. Anything that needs JS doesn't belong in a template. |
| No external assets | Images, fonts, and CSS must be inlined or hosted on `raw.githubusercontent.com` inside this repo. Otherwise the template breaks if the external host goes away or starts blocking hotlinks. |
| Inline CSS only | Most email clients (Gmail, Outlook) strip `<style>` blocks or `<link>` tags. Use the `style=""` attribute. |
| Mobile responsive | Use a fluid layout (max-width tables, percentage widths). Test in a phone-width preview before submitting. |
| Works in dark mode | Avoid pure white backgrounds and pure black text. Use `#fafafa`/`#171717` or similar so it stays legible when the client inverts colors. |
| Include unsubscribe link | Add `<a href="{{unsubscribe_url}}">Unsubscribe</a>` in the footer. SendDock requires this for compliance. |

## Variables

Templates use [Handlebars](https://handlebarsjs.com) syntax. SendDock provides these built-in variables on every send:

| Variable | What it resolves to |
|---|---|
| `{{name}}` | Subscriber's name |
| `{{email}}` | Subscriber's email address |
| `{{subscriber_id}}` | Internal ID (useful for tracking links) |
| `{{unsubscribe_url}}` | One-click unsubscribe URL (RFC 8058 compatible) |

You can also use any custom variable you want (e.g. `{{first_name}}`, `{{company_name}}`, `{{cta_url}}`). Declare each one in the `variables` array of your `index.json` entry so the editor can show them as hints.

## Thumbnail specs

- **Dimensions**: 600×400 pixels
- **Format**: PNG
- **Max size**: 100 KB (compress with [TinyPNG](https://tinypng.com) or `pngquant` if larger)
- **Content**: render the template in a real email client (or a browser preview), screenshot it, crop to 600×400

The thumbnail is what people see in the gallery before they click — make it look like the actual rendered email, not a cropped fragment.

## `index.json` schema

Each entry in the `templates` array looks like this:

```json
{
  "id": "welcome-minimal",
  "name": "Welcome — minimal",
  "category": "welcome",
  "description": "Clean welcome email with a single CTA. Works for SaaS onboarding and newsletter sign-ups.",
  "thumbnail_url": "https://raw.githubusercontent.com/Arkhe-Systems/senddock-templates/main/templates/welcome-minimal.png",
  "html_url": "https://raw.githubusercontent.com/Arkhe-Systems/senddock-templates/main/templates/welcome-minimal.html",
  "variables": ["first_name", "company_name", "cta_url"]
}
```

### Field rules

| Field | Rules |
|---|---|
| `id` | kebab-case, must match the HTML and PNG filenames |
| `name` | Short display name (≤ 40 chars). Use em-dashes for subtitles: `Newsletter — monthly digest` |
| `category` | One of: `welcome`, `newsletter`, `announcement`, `digest`, `transactional` |
| `description` | One sentence (≤ 140 chars). What is it for, who would use it. |
| `thumbnail_url` | Must point at `templates/<id>.png` in this repo |
| `html_url` | Must point at `templates/<id>.html` in this repo |
| `variables` | Custom variables the template references. Don't list the built-in ones. |

## Categories

Right now we have five. Open an issue first if you think we need a new one — adding categories is a coordination decision, not a per-template choice.

- **welcome** — first email after signup
- **newsletter** — recurring content broadcasts
- **announcement** — product launches, feature releases, milestones
- **digest** — periodic summaries (weekly, monthly)
- **transactional** — receipts, password resets, verification codes

## Local validation

Before opening a PR:

```bash
python3 scripts/validate.py
```

This is the same script CI runs. It checks:

- `index.json` parses and has the required top-level fields
- Every template entry has all required fields with valid values
- Every `id` has a matching `.html` and `.png` file
- HTML files don't contain `<script>` tags
- PNG files are under 100 KB
- URLs match the expected `raw.githubusercontent.com` pattern

## Review process

- Two checks must pass: CI validation and a maintainer review.
- Maintainers will test-render your template in SendDock before merging.
- Tweaks may be requested for HTML compatibility (Gmail and Outlook are picky).
- Once merged, your template is live in every SendDock instance within an hour.
