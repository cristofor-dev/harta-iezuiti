# Context — harta-iezuiti

O hartă interactivă cu așezările istorice ale iezuiților din Cluj-Napoca (1579–prezent),
destinată publicului larg / turismului cultural. Livrată ca bloc HTML/JS de sine stătător
(Leaflet + OpenStreetMap, fără cheie API), inserat într-un site WordPress existent.

Sursa de adevăr pentru scope, decizii de produs și motivația lor e
**`planificare/planificare-harta-iezuiti.md`** — citește-l înainte de orice lucru pe acest
workspace. Pentru pașii de deploy/integrare: **`instructiuni-wordpress.md`**.

## Status

Implementat, redesenat (UI/UX) și testat cu Playwright/Chromium pe desktop + mobil: toate cele
8 locuri, imaginile, cronologia, starea activă, popup-urile și izolarea CSS într-o temă
WordPress ostilă — zero probleme, zero erori de consolă. Gata de integrare — rămâne doar
upload-ul pozelor în Media Library și înlocuirea `PHOTO_BASE` (vezi `instructiuni-wordpress.md`).

Repository: https://github.com/cristofor-dev/harta-iezuiti (privat)

## Structură

```
harta-iezuiti/
├── CONTEXT.md
├── planificare/
│   └── planificare-harta-iezuiti.md
├── instructiuni-wordpress.md      # pași deploy: upload poze, integrare Custom HTML block
├── harta.html                     # SURSA DE ADEVĂR — pagină completă, previzualizare locală
├── harta-embed-wordpress.html     # GENERAT din harta.html — codul de lipit în WordPress
├── sync-embed.py                  # regenerează ambele embed-uri din sursele lor
├── harta-1730.html                # SURSA a hărții istorice Cluj 1730 (imagine + zoom/pan, 7 locații, modal)
├── harta-1730-embed-wordpress.html # GENERAT din harta-1730.html
└── content/
    ├── Prezenta_Iezuitilor_Cluj-Napoca_1.md    # text sursă pentru popup-uri (convertit din PDF-ul original, șters după conversie)
    ├── harta-1730/cluj-map-1730.webp           # harta 1730, comprimată (WebP q82, 2560×1706, ~870 KB)
    └── photo/                                   # 8 fotografii de arhivă (Fortepan, Wikimedia)
```

## De știut înainte să lucrezi aici

- **Editează doar `harta.html`, apoi rulează `python sync-embed.py`.** Fișierul de WordPress e
  generat — editat direct, modificarea se pierde la următoarea regenerare. (Înainte erau
  întreținute manual în paralel și au divergat.)
- Stack: Leaflet.js + OpenStreetMap + Leaflet.markercluster, totul via CDN (cu integrity
  hash-uri SRI) — fără build, fără cont, fără cheie API. `MarkerCluster.Default.css` NU se
  încarcă: grupurile au stil propriu, prin `iconCreateFunction`.
- Coordonatele celor 8 locații sunt geocodate real via Nominatim/OpenStreetMap (6 din 8 cu
  potrivire exactă). Locațiile 6 (Seminarul Sf. Iosif) și 7 (Strada Búza) sunt aproximative
  — marcate `approx: true` în array-ul `locations` din cod.
- Numerotarea locațiilor (`id`, pinii, cronologia) e **cronologică** (1579 → anii 2000), nu
  ordinea din PDF-ul sursă. Numele fișierelor din `content/photo/` au rămas cu numerotarea
  veche — sunt referințe interne, nu contează pentru utilizator.
- Vederea inițială e un `setView` fix la zoom 18 pe grupul dens (locurile 4, 5, 6), nu
  `fitBounds` peste toate cele 8: la orice zoom care le încape pe toate, grupul dens se
  suprapune. Locurile 1, 3 și 8 se ating din cronologie sau din butonul „Vezi toate locurile”.
- Butoanele custom din popup trebuie să cheme `ev.stopPropagation()` — fără el,
  Leaflet.markercluster închide popup-ul la primul click intern (bug reprodus și reparat).
- **Popup-ul nu are `maxHeight` — intenționat.** Cerință explicită: nimic nu se derulează în
  el. În schimb `fitMapToPopup()` crește harta cât e nevoie, iar `resetMapHeight()` o readuce
  la loc. Extinderea lărgește și popup-ul (rânduri mai lungi = mai puțină înălțime).
- Extinderea e într-un singur sens (nu există „Arată mai puțin”); `popupclose` readuce
  popup-ul la rezumat, altfel s-ar redeschide extins și fără cale înapoi.
- Cât timp e deschis un popup, controalele de sus ale hărții se ascund
  (`.iez-has-popup .leaflet-top`) — acopereau titlul și butonul de închidere. Nu încerca să
  rezolvi cu `z-index`: panoul hărții are `transform`, deci propriul context de stivuire.
  Ascunderea trebuie făcută cu `visibility`, nu doar `opacity` (Leaflet forțează
  `pointer-events: auto` pe controale). Atribuirea OSM, de jos, rămâne vizibilă — obligatorie
  prin licență.
- **Capcane de integrare WordPress, toate prinse rulând blocul într-o temă ostilă** (fiecare
  are un comentariu în cod, nu le „curăța” fără să testezi din nou):
  - dalele hărții sunt `<img>`, deci `img { border: … }` din temă desenează o grilă peste
    hartă — de aici resetul pe `.leaflet-*-pane img`;
  - temele folosesc `button:hover { … !important }`, de unde `!important` pe culorile
    stărilor interactive;
  - Leaflet impune „Helvetica Neue” în interiorul hărții — readus la `font-family: inherit`;
  - `h2/h3/p` preiau `text-transform`, fonturi și `line-height` de la temă — de aici blocul
    de normalizare defensivă.
- Limba conținutului: doar română (decizie explicită, vezi planificarea).

## Harta Cluj 1730 (`harta-1730.html`)

Pagină separată, independentă de harta Leaflet; implementează `design_handoff_harta_cluj_1730`
(Cinzel + EB Garamond, paletă pergament). Vanilla JS, fără build, scopată sub `#iezuiti-1730-wrap`.
Același flux ca la prima hartă: editezi `harta-1730.html`, rulezi `python sync-embed.py`; în WordPress
se înlocuiește `IMG_BASE` cu URL-ul din Media Library (încarcă `cluj-map-1730.webp`).

- Pozițiile (x, y în %) și coordonatele GPS ale celor 7 locații sunt **estimate**, din handoff — de verificat.
- Textele sunt provizorii. Imaginile locațiilor lipsesc: câmpul opțional `photo` din `LOCS` (fișier în
  `IMG_BASE`); fără el, modalul arată un placeholder.
- Pan/zoom: limita de pan e `(zoom−1)*50/zoom` (translate vine după scale), nu `(zoom−1)*50` ca în
  prototip, altfel apar margini goale; drag-ul e 1:1 cu degetul.
- Sub 760px modalul e `position: fixed` pe tot ecranul — harta e prea mică pe telefon pentru un modal în ea.
