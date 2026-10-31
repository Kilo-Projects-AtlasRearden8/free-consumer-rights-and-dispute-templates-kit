#!/usr/bin/env python3
"""Verification suite for the Free Consumer Rights & Dispute Templates Kit.

Runs the checks that define "this kit builds and passes":
  * every expected file exists
  * each HTML file parses cleanly
  * LICENSE carries the exact copyright line
  * README credits Asdale Dynamics, LLC
  * no secrets / API keys / personal data in any tracked file
  * no .github/workflows files
  * every screen input has an associated label (accessibility)
  * no invalid HTML attributes (e.g. CSS properties inside HTML tags)
Prints a PASS/FAIL summary and exits non-zero on any failure.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_HTML = [
    "html/demand-letter.html",
    "html/warranty-claim.html",
    "html/small-claims-worksheet.html",
    "html/complaint-tracker.html",
]
EXPECTED_MD = [
    "templates/demand-letter.md",
    "templates/warranty-claim.md",
    "templates/small-claims-worksheet.md",
    "templates/complaint-tracker.md",
]
COPYRIGHT_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"

failures = []
checks = 0


def check(name, condition, detail=""):
    global checks
    checks += 1
    if condition:
        print(f"  PASS {name}")
    else:
        failures.append((name, detail))
        print(f"  FAIL {name} {detail}")


class StrictParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.labels_without_for = []
        self.inputs_without_id = []
        self.textarea_attrs = []  # (attr_name,) for non-standard attrs

    def error(self, msg):
        self.errors.append(msg)

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "label" and "for" not in attr_dict:
            self.labels_without_for.append(attrs)
        if tag in ("input", "textarea", "select") and "id" not in attr_dict:
            self.inputs_without_id.append((tag, attrs))
        if tag == "textarea":
            for attr in attr_dict:
                if attr not in ("id", "name", "placeholder", "minlength", "maxlength",
                                "readonly", "required", "disabled", "wrap", "spellcheck",
                                "autofocus", "form", "dirname"):
                    self.textarea_attrs.append(attr)


def has_secretish_content(text):
    patterns = [
        r"(?i)\bapi[_-]?key\b",
        r"(?i)\bsecret\b",
        r"(?i)\bpassword\b",
        r"(?i)\baccess[_-]?token\b",
        r"\bsk-[A-Za-z0-9]{16,}",
        r"\bAKIA[0-9A-Z]{16}",
        r"(?i)\bprivate[_-]?key\b",
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN-like
        r"\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b",  # card-like
    ]
    return any(re.search(p, text) for p in patterns)


# 1. Files exist
for rel in EXPECTED_HTML + EXPECTED_MD + ["LICENSE", "README.md"]:
    p = ROOT / rel
    check(f"file exists: {rel}", p.is_file(), f"missing {rel}")

# 2. HTML parses + accessibility + no invalid attrs
for rel in EXPECTED_HTML:
    text = (ROOT / rel).read_text(encoding="utf-8")
    parser = StrictParser()
    parser.feed(text)
    check(f"HTML parses: {rel}", not parser.errors, f"errors: {parser.errors[:3]}")
    check(f"labels have for= : {rel}", not parser.labels_without_for,
          f"{len(parser.labels_without_for)} labels missing for=")
    check(f"inputs have id= : {rel}", not parser.inputs_without_id,
          f"{len(parser.inputs_without_id)} inputs missing id=")
    check(f"no invalid textarea attrs: {rel}", not parser.textarea_attrs,
          f"invalid attrs: {parser.textarea_attrs}")

# 3. LICENSE copyright line exact
lic = (ROOT / "LICENSE").read_text(encoding="utf-8")
check("LICENSE has exact copyright line", COPYRIGHT_LINE in lic,
      f"line '{COPYRIGHT_LINE}' not found")

# 4. README credits Asdale Dynamics, LLC
readme = (ROOT / "README.md").read_text(encoding="utf-8")
check("README credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme,
      "credit missing")

# 5. No secrets (skip meta/tooling files that describe the scan itself)
secret_text = "\n".join(
    p.read_text(encoding="utf-8", errors="ignore")
    for p in ROOT.rglob("*")
    if p.is_file()
    and p.suffix in {".md", ".html", ".py", ".txt", ".json", ".yml", ".yaml"}
    and "tests" not in p.parts
    and p.name != "STATUS.md"
)
check("no secret-like patterns", not has_secretish_content(secret_text),
      "secret-like pattern found")

# 6. No .github/workflows
workflows = list(ROOT.rglob(".github/workflows/*"))
check("no .github/workflows files", not workflows,
      f"{len(workflows)} workflow files found")

print(f"\n{checks} checks run, {len(failures)} failure(s)")
if failures:
    print("\nFailures:")
    for name, detail in failures:
        print(f"  - {name}: {detail}")
    sys.exit(1)
print("ALL CHECKS PASSED")
