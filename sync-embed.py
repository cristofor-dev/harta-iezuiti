#!/usr/bin/env python3
"""Generează harta-embed-wordpress.html din harta.html.

`harta.html` e sursa unică de adevăr (pagina completă, pentru previzualizare locală).
Varianta de WordPress e exact același conținut, fără <!doctype>/<html>/<head>/<body> —
care n-au ce căuta într-un bloc de conținut — plus o notă explicită despre PHOTO_BASE.

Rulează după ORICE modificare în harta.html:

    python sync-embed.py
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).parent

PHOTO_BASE_SRC = (
    '  var PHOTO_BASE = "content/photo/"; '
    "// în WordPress: se înlocuiește cu URL-urile din Media Library"
)
PHOTO_BASE_EMBED = """  // ATENȚIE: înlocuiește valoarea de mai jos cu URL-ul din Media Library WordPress
  // unde ai încărcat pozele (vezi instructiuni-wordpress.md), păstrând "/" la final.
  // Exemplu: "https://numelesitei.ro/wp-content/uploads/2026/08/"
  var PHOTO_BASE = "content/photo/";"""

# Fiecare pagină: (sursă, ieșire, id-ul div-ului rădăcină, linia IMG_BASE din sursă, forma ei în embed)
PAGES = [
    {
        "src": HERE / "harta.html",
        "out": HERE / "harta-embed-wordpress.html",
        "root_id": "iezuiti-harta-wrap",
        "base_src": PHOTO_BASE_SRC,
        "base_embed": PHOTO_BASE_EMBED,
        "title": "Harta Iezuiților în Cluj-Napoca",
    },
    {
        "src": HERE / "harta-1730.html",
        "out": HERE / "harta-1730-embed-wordpress.html",
        "root_id": "iezuiti-1730-wrap",
        "base_src": (
            '  var IMG_BASE = "content/harta-1730/"; '
            "// în WordPress: se înlocuiește cu URL-ul din Media Library\n"
            '  var PHOTO_BASE = "content/photo/"; '
            "// fotografiile locațiilor (aceleași ca la harta Leaflet)"
        ),
        "base_embed": """  // ATENȚIE: înlocuiește valoarea de mai jos cu URL-ul din Media Library WordPress
  // unde ai încărcat imaginea hărții (cluj-map-1730.webp), păstrând "/" la final.
  // Exemplu: "https://numelesitei.ro/wp-content/uploads/2026/08/"
  var IMG_BASE = "content/harta-1730/";
  // Fotografiile locațiilor: același folder din Media Library ca la harta Leaflet (vezi instructiuni-wordpress.md).
  var PHOTO_BASE = "content/photo/";""",
        "title": "Harta Cluj 1730",
    },
]

BANNER = """<!--
  {title} — bloc pentru WordPress (Custom HTML).
  GENERAT AUTOMAT din {src} — nu edita direct acest fișier;
  modifică {src} și rulează `python sync-embed.py`.
-->"""


def fail(msg):
    print(f"EROARE: {msg}", file=sys.stderr)
    sys.exit(1)


def build(page):
    src, out_path = page["src"], page["out"]
    if not src.exists():
        fail(f"nu găsesc {src}")
    html = src.read_text(encoding="utf-8")

    head_match = re.search(
        r'(<link rel="stylesheet".*?</style>)', html, re.S
    )
    if not head_match:
        fail(f"{src.name}: nu am găsit blocul <link>…</style> din <head>")

    body_match = re.search(
        r'(<div id="%s">.*</script>)' % re.escape(page["root_id"]), html, re.S
    )
    if not body_match:
        fail(f"{src.name}: nu am găsit conținutul dintre <div id=\"{page['root_id']}\"> și ultimul </script>")

    assets = head_match.group(1).strip()
    body = body_match.group(1).strip()

    if page["base_src"] not in body:
        fail(f"{src.name}: linia cu URL-ul de bază nu mai are forma așteptată — actualizează sync-embed.py")
    body = body.replace(page["base_src"], page["base_embed"])

    banner = BANNER.format(title=page["title"], src=src.name)
    out = f"{banner}\n\n{assets}\n\n{body}\n"
    out_path.write_text(out, encoding="utf-8")

    print(f"OK — {out_path.name} regenerat din {src.name} ({len(out.splitlines())} linii).")


def main():
    for page in PAGES:
        build(page)


if __name__ == "__main__":
    main()
