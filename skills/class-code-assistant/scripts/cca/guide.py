"""Parse the company's classification guide excerpt into paragraphs and class codes."""

import re
from dataclasses import dataclass

PARAGRAPH = re.compile(
    r"\*\*(?P<ref>CG-\d+)\.\s+(?:(?P<code>[A-Z]-\d{3})\s+)?(?P<title>[^*]+?)\.?\*\*\s*(?P<body>.*?)(?=\n\s*\n|\Z)",
    re.S,
)
EDITION = re.compile(r"Edition of ([A-Z][a-z]+ \d{4})")


@dataclass(frozen=True)
class Paragraph:
    ref: str
    code: str | None
    title: str
    body: str


class Guide:
    def __init__(self, text):
        self.text = text
        m = EDITION.search(text)
        self.edition = m.group(1) if m else None
        self.paragraphs = {}
        for m in PARAGRAPH.finditer(text):
            body = " ".join(m["body"].split())
            self.paragraphs[m["ref"]] = Paragraph(m["ref"], m["code"], " ".join(m["title"].split()), body)
        self.code_ref = {p.code: p.ref for p in self.paragraphs.values() if p.code}
        if not self.code_ref:
            raise ValueError("no class code paragraphs (**CG-nn. X-nnn Title.**) found in the classification guide")

    def ref_for(self, code):
        """The paragraph identifier, exactly as printed, that describes a class code."""
        try:
            return self.code_ref[code]
        except KeyError:
            raise ValueError(f"class code {code} is not described in the classification guide "
                             f"(known: {', '.join(sorted(self.code_ref))})") from None

    def label(self, code):
        p = self.paragraphs[self.ref_for(code)]
        return f"{code} {p.title}"
