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
SRC = HERE / "harta.html"
OUT = HERE / "harta-embed-wordpress.html"

PHOTO_BASE_SRC = (
    '  var PHOTO_BASE = "content/photo/"; '
    "// în WordPress: se înlocuiește cu URL-urile din Media Library"
)
PHOTO_BASE_EMBED = """  // ATENȚIE: înlocuiește valoarea de mai jos cu URL-ul din Media Library WordPress
  // unde ai încărcat pozele (vezi instructiuni-wordpress.md), păstrând "/" la final.
  // Exemplu: "https://numelesitei.ro/wp-content/uploads/2026/08/"
  var PHOTO_BASE = "content/photo/";"""

BANNER = """<!--
  Harta Iezuiților în Cluj-Napoca — bloc pentru WordPress (Custom HTML).
  GENERAT AUTOMAT din harta.html — nu edita direct acest fișier;
  modifică harta.html și rulează `python sync-embed.py`.
-->"""


def fail(msg):
    print(f"EROARE: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not SRC.exists():
        fail(f"nu găsesc {SRC}")
    html = SRC.read_text(encoding="utf-8")

    head_match = re.search(
        r'(<link rel="stylesheet".*?</style>)', html, re.S
    )
    if not head_match:
        fail("nu am găsit blocul <link>…</style> din <head>")

    body_match = re.search(
        r'(<div id="iezuiti-harta-wrap">.*</script>)', html, re.S
    )
    if not body_match:
        fail("nu am găsit conținutul dintre <div id=\"iezuiti-harta-wrap\"> și ultimul </script>")

    assets = head_match.group(1).strip()
    body = body_match.group(1).strip()

    if PHOTO_BASE_SRC not in body:
        fail("linia PHOTO_BASE din harta.html nu mai are forma așteptată — actualizează sync-embed.py")
    body = body.replace(PHOTO_BASE_SRC, PHOTO_BASE_EMBED)

    out = f"{BANNER}\n\n{assets}\n\n{body}\n"
    OUT.write_text(out, encoding="utf-8")

    print(f"OK — {OUT.name} regenerat din {SRC.name} ({len(out.splitlines())} linii).")


if __name__ == "__main__":
    main()
