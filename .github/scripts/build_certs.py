"""Rebuild the certificates gallery in README.md from files in certificates/."""
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "certificates"
README = ROOT / "README.md"
IMAGES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
PER_ROW = 3


def title(path):
    return re.sub(r"[_-]+", " ", path.stem).strip()


def cell(path):
    url = "./certificates/" + quote(path.name)
    if path.suffix.lower() in IMAGES:
        body = f'<a href="{url}"><img src="{url}" width="260" alt="{title(path)}"/></a>'
    else:
        body = f'<a href="{url}">📄 Open PDF</a>'
    return f'    <td align="center" valign="top">{body}<br/><sub><b>{title(path)}</b></sub></td>'


files = sorted(
    (p for p in CERT_DIR.glob("*") if p.suffix.lower() in IMAGES | {".pdf"}),
    key=lambda p: p.name.lower(),
)

if files:
    rows = []
    for i in range(0, len(files), PER_ROW):
        rows.append("  <tr>\n" + "\n".join(cell(p) for p in files[i:i + PER_ROW]) + "\n  </tr>")
    gallery = '<table align="center">\n' + "\n".join(rows) + "\n</table>"
else:
    gallery = '<p align="center"><em>Certificates coming soon…</em></p>'

text = README.read_text(encoding="utf-8")
new = re.sub(
    r"<!-- CERTS:START -->.*?<!-- CERTS:END -->",
    f"<!-- CERTS:START -->\n{gallery}\n<!-- CERTS:END -->",
    text,
    flags=re.S,
)
README.write_text(new, encoding="utf-8")
print(f"{len(files)} certificate(s) rendered")
