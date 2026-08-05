# Context — harta-iezuiti

O hartă interactivă cu așezările istorice ale iezuiților din Cluj-Napoca (1579–prezent),
destinată publicului larg / turismului cultural. Livrată ca bloc HTML/JS de sine stătător
(Leaflet + OpenStreetMap, fără cheie API), inserat într-un site WordPress existent.

Sursa de adevăr pentru scope, decizii de produs și motivația lor e
**`planificare/planificare-harta-iezuiti.md`** — citește-l înainte de orice lucru pe acest
workspace. Pentru pașii de deploy/integrare: **`instructiuni-wordpress.md`**.

## Status

Implementat și testat (vizual + funcțional, desktop + mobil, cu Playwright/Chromium: toate
cele 8 locații, imagini, toggle „citește mai mult", zero erori de consolă, zero overflow).
Gata de integrare în WordPress — rămâne doar upload-ul pozelor în Media Library și
înlocuirea URL-urilor în cod (vezi `instructiuni-wordpress.md`).

## Structură

```
harta-iezuiti/
├── CONTEXT.md
├── planificare/
│   └── planificare-harta-iezuiti.md
├── instructiuni-wordpress.md      # pași deploy: upload poze, integrare Custom HTML block
├── harta.html                     # previzualizare locală (pagină completă, self-contained)
├── harta-embed-wordpress.html     # codul de lipit în WordPress (fără doctype/html/head/body)
└── content/
    ├── Prezenta_Iezuitilor_Cluj-Napoca_1.md    # text sursă pentru popup-uri (convertit din PDF-ul original, șters după conversie)
    └── photo/                                   # 8 fotografii de arhivă (Fortepan, Wikimedia)
```

## De știut înainte să lucrezi aici

- Stack: Leaflet.js + OpenStreetMap + Leaflet.markercluster, totul via CDN (cu integrity
  hash-uri SRI) — fără build, fără cont, fără cheie API.
- Coordonatele celor 8 locații sunt geocodate real via Nominatim/OpenStreetMap (6 din 8 cu
  potrivire exactă). Locațiile 6 (Seminarul Sf. Iosif) și 7 (Strada Búza) sunt aproximative
  — marcate `approx: true` în array-ul `locations` din cod.
- Numerotarea locațiilor (`id`, badge-urile de pe hartă, legenda) e **cronologică** (1579 →
  anii 2000), nu ordinea din PDF-ul sursă. Numele fișierelor din `content/photo/` au rămas cu
  numerotarea veche — sunt referințe interne, nu contează pentru utilizator.
- Clustering-ul (Leaflet.markercluster) e necesar, nu opțional: câteva locații sunt la doar
  ~20-100m distanță, deci la zoom-ul care încape toate cele 8 puncte s-ar suprapune complet
  și ar deveni imposibil de apăsat individual fără el.
- Butoanele custom din popup-uri (`toggle-btn`) trebuie să cheme `ev.stopPropagation()` —
  vezi comentariul din cod. Fără el, Leaflet.markercluster închide popup-ul la primul click
  intern (bug reprodus și reparat în sesiunea de implementare).
- `harta.html` și `harta-embed-wordpress.html` sunt sincronizate manual (același conținut,
  ambalaj diferit) — orice modificare a hărții/popup-urilor/datelor se face în ambele.
- Limba conținutului: doar română (decizie explicită, vezi planificarea).
- Git nu e inițializat în acest workspace.
