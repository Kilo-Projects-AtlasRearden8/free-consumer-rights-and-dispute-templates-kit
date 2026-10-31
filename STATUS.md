# STATUS

## What was built

Free Consumer Rights & Dispute Templates Kit — fillable, printable, no-account-required templates for consumer-rights paperwork, education only (not legal advice).

Files:
- `README.md` — kit overview, how-to, disclaimer, credit to Asdale Dynamics, LLC, MIT license pointer
- `LICENSE` — MIT License, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `templates/demand-letter.md` — demand letter template with sender/recipient/dispute/resolution/deadline/attachments/checklist
- `templates/warranty-claim.md` — warranty claim form (claimant, product, problem, resolution, documents, where to send, checklist)
- `templates/small-claims-worksheet.md` — small-claims worksheet (case basics, timeline, amount owed, evidence/witnesses, defendant response, pre-file checklist, court prep, after judgment)
- `templates/complaint-tracker.md` — complaint tracker (complaint log, contact log, escalation checklist, evidence tracker)
- `html/demand-letter.html`, `html/warranty-claim.html`, `html/small-claims-worksheet.html`, `html/complaint-tracker.html` — single-file, fillable printable versions with `<input>`/`<textarea>`/checkbox fields, print CSS (`@media print` hides controls, strips field backgrounds), Print / Save as PDF and Reset buttons

No `.github/workflows` files. No secrets, API keys, or personal data in any file.

## How to run

No build step, no server, no account needed.
1. Open any `html/*.html` file directly in a browser (double-click).
2. Fill in the fields.
3. Click "Print / Save as PDF" or use the browser print dialog.
4. Optionally edit the matching `templates/*.md` source to tailor the language.

## Verification results

- All 4 HTML files parse cleanly with Python `html.parser` (no errors).
- `LICENSE` contains exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `README.md` credits Asdale Dynamics, LLC.
- Secret-pattern scan (api_key/secret/password/token/sk-/AKIA, case-insensitive): 0 hits across all files.
- Git initialized and committed as `0932f11` (plain message, no Co-authored-by trailer), using existing git identity. Not pushed; no remote created.

## Known gaps

- Templates are generic U.S. consumer-rights forms; state-specific small-claims limits, court forms, and filing procedures are not included — users must check their local court.
- No automated form validation or data storage (by design: local-first, no account).
- Not reviewed by an attorney; disclaimers state education only, not legal advice.
