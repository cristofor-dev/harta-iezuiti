# Harta Iezuiților în Cluj-Napoca

Hartă interactivă cu așezările istorice ale iezuiților din Cluj-Napoca (1579–prezent), pentru
publicul larg / turism cultural. Nu e o aplicație de sine stătătoare, ci un bloc de conținut
inserat într-un site WordPress deja existent.

## Stack

- Leaflet.js + tile-uri OpenStreetMap + Leaflet.markercluster, toate încărcate via CDN (cu
  integrity hash-uri SRI) — **fără build, fără cont, fără cheie API, fără cost**.
- Livrare: bloc HTML/JS complet autonom (`<div>` + `<style>` + `<script>` inline), compatibil
  cu blocul „Custom HTML" din Gutenberg sau widget-ul HTML din orice page builder (Elementor,
  Divi etc.) — nu depinde de care anume folosește site-ul țintă.
- Limba interfeței: **doar română** pentru v1. Traducerea (ex. engleză, utilă pentru turiști)
  rămâne o îmbunătățire viitoare separată — nu există structură de multi-limbă în cod acum.

> Decizie: s-a renunțat la Google Maps (varianta inițial cerută) în favoarea Leaflet+OSM,
> după ce utilizatorul a înțeles că Google Maps ar fi cerut cont Google Cloud, card de
> facturare activat și administrarea unei chei API — nejustificat pentru 8 markere fixe.

## De ce clustering (Leaflet.markercluster)

Nu e o alegere estetică — e necesară funcțional. Câteva perechi de locații sunt la doar
~20-100m distanță una de alta (ex. Convictus Nobilium și Seminarul Sf. Iosif). La zoom-ul
care încape toate cele 8 puncte pe hartă, markerele s-ar suprapune complet și ar deveni
imposibil de apăsat individual. Clustering-ul grupează vizual punctele apropiate într-un
cerc cu cifră; un click/tap le desparte (zoom sau spiderfy).

`maxClusterRadius` (30px) și `disableClusteringAtZoom` (16) sunt calibrate ca zona
Universității (locațiile 2, 3, 4, 5, 6, 7 — toate în centrul istoric) să se despartă în
markere individuale de îndată ce utilizatorul dă zoom puțin peste vederea inițială de
ansamblu — nu doar la zoom maxim. Valorile inițiale (50px / zoom 18) erau prea agresive:
încă mai clusteriza locații la un zoom la care utilizatorul se aștepta deja să le vadă
distinct.

La vederea de ansamblu inițială (toate cele 8 locații vizibile deodată — cerință explicită,
nu se poate "da zoom mai mare" fără a scoate din cadru locațiile 1 și 8, aflate la ~2-3km de
restul), un grup de 5 locații apropiate tot se clusterizează într-un singur cerc — inevitabil
geometric, nu un bug. Problema reală era că acel cerc arăta cifra „5" (numărul de locuri din
grup) în același stil vizual (negru, cerc, cifră albă) ca badge-ul individual al locației
#5 — ușor de confundat. Rezolvat prin recolorarea cluster-elor în **albastru**, complet
diferit de negrul badge-urilor individuale, ca cele două să nu mai poată fi confundate la
prima vedere.

## Conținut sursă

Utilizatorul a furnizat un PDF cu text istoric și fotografii de arhivă. A fost convertit în
`content/Prezenta_Iezuitilor_Cluj-Napoca_1.md`, iar cele 8 fotografii au fost extrase în
`content/photo/` (surse: Fortepan.hu, licență CC-BY-SA 3.0, și Wikimedia Commons). PDF-ul
original a fost șters după conversie — nu mai era necesar, tot conținutul lui e păstrat în
`.md` și în `photo/`.

Cele 8 locații documentate, numerotate **cronologic** (nu în ordinea din documentul sursă):

| # | Locație | Reper cronologic | Adresă / context | Poze | Coordonate |
| --- | --- | --- | --- | --- | --- |
| 1 | Fosta mănăstire iezuită (Calea Mănăștur) | 1579 — sosirea iezuiților la Cluj | Calea Mănăștur nr. 9 | 1 | exacte (OSM) |
| 2 | Universitatea Babeș-Bolyai, clădirea centrală | 1581 — fondarea Colegiului Iezuit | Str. Mihail Kogălniceanu 1 | 1 | exacte (OSM) |
| 3 | Biserica Franciscanilor | 1693 — folosire temporară de iezuiți | Piața Muzeului | 0 | exacte (OSM) |
| 4 | Convictus Nobilium (azi Clădirea Echinox) | ~1700 — construcție | Str. Universității nr. 7 | 2 | exacte (OSM) |
| 5 | Biserica Piariștilor (fosta Biserică Iezuită) | 1718-1725 — construcție/sfințire | Str. Universității nr. 5 | 2 | exacte (OSM) |
| 6 | Seminarul „Sfântul Iosif" | 1725 — construcția porții | adiacent Convictus Nobilium, fără adresă proprie | 0 | **aproximative** |
| 7 | Strada Búza (Str. Inocențiu Micu Klein) | 1962 — datarea fotografiei de context | context istoric, fără adresă exactă | 1 | **aproximative** |
| 8 | Mănăstirea din cartierul Zorilor (Centrul Manresa) | anii 2000 — revenirea ordinului | cartierul Zorilor | 1 | exacte (OSM) |

Coordonatele au fost geocodate real prin API-ul Nominatim/OpenStreetMap (nu doar estimate din
memorie) — 6 din 8 locații au potrivire exactă cu o clădire/adresă existentă în OSM. Locațiile
6 și 7 rămân aproximative pentru că sursa nu oferă o adresă exactă; sunt marcate `approx: true`
în cod și pot fi corectate ulterior dacă apare o sursă mai precisă.

### Numerotare și navigare (adăugat ulterior, la cererea utilizatorului)

Markerele de pe hartă poartă un număr vizibil (badge circular) corespunzător ordinii
cronologice de mai sus, nu ordinii din PDF-ul sursă sau din numele fișierelor foto (acelea au
rămas neschimbate — sunt referințe interne, invizibile utilizatorului final). Sub hartă există
o **legendă** — o listă cu toate cele 8 locații, în aceeași ordine — unde click/tap pe un rând
duce harta direct la locația respectivă (via `clusterGroup.zoomToShowLayer`, dezgrupând
clusterul dacă e nevoie) și îi deschide automat popup-ul.

## Interactivitate

Click/tap pe marker deschide un popup pe hartă cu:
- titlu și adresă/context;
- fotografiile locației (dacă există) — locațiile 3 și 6 arată în schimb un mesaj discret
  „Fără fotografie disponibilă pentru această locație", fără să strice layout-ul;
- un **rezumat scurt** (2-3 fraze);
- un buton **„Citește mai mult"** care extinde textul la varianta istorică completă (din
  `content/Prezenta_Iezuitilor_Cluj-Napoca_1.md`).

Popup-ul are o înălțime maximă (`maxHeight`) cu scroll intern, ca varianta extinsă (text
lung) să nu depășească niciodată vizual harta.

## Stil vizual

Neutru și minimal — nu preia paleta auriu/maro/siglă IHS din PDF-ul sursă, ca să nu intre în
conflict cu tema WordPress a site-ului țintă (necunoscută în detaliu la momentul construcției).

## Responsive

Mobil-first: popup-uri, imagini și butoane dimensionate explicit pentru ecran de telefon
(buton „Citește mai mult" de minimum 46px înălțime, pentru target tactil), pornind de la
premisa că turiștii vor accesa harta de pe teren, în timp ce se plimbă prin oraș.

## Integrare în WordPress

Site-ul WordPress țintă există deja; nu se știe exact ce editor/builder folosește (Gutenberg
nativ vs. Elementor/Divi) — de aceea livrabilul e construit ca bloc HTML/JS generic, care
funcționează în orice bloc/widget „Custom HTML". Nu s-a decis cine face integrarea efectivă
(utilizatorul sau altcineva cu acces la site) — pașii sunt documentați în
`instructiuni-wordpress.md` ca să fie „predabili oricui", inclusiv unei persoane fără
cunoștințe de cod.

## Testare (cerință explicită)

Implementarea trebuie verificată efectiv într-un browser — vizual și funcțional, nu doar prin
citirea codului — pe **ambele** viewport-uri: desktop și mobil. S-a folosit Playwright cu
Chromium real pentru a clicka fiecare din cele 8 markere, verifica popup-urile, imaginile și
butonul „Citește mai mult", pe ambele viewport-uri.

Din testare a rezultat un bug real (nu doar teoretic): butoanele custom din popup-uri
închideau popup-ul la primul click, din cauza interferenței dintre click-ul intern și
Leaflet.markercluster — reparat prin `ev.stopPropagation()` explicit în handler (vezi
comentariul din cod). Alte ajustări rezultate din testare: mărimea minimă a butonului de
touch (40px → 46px) și limita de înălțime a popup-ului cu scroll intern.

După adăugarea numerotării cronologice și a legendei, s-a repetat testarea Playwright pe
ambele viewport-uri: cele 8 rânduri din legendă, în ordinea corectă (1-8), fiecare click
navighează la markerul corect și deschide popup-ul cu titlul care începe cu numărul așteptat
(ex. „5. Biserica Piariștilor”) — 0 probleme găsite.

## Ce nu e în scope (v1)

- Traducere multi-limbă.
- Fotografii suplimentare pentru locațiile 3 și 6 (căutare de surse noi).
- Coordonate GPS confirmate manual pentru locațiile 6 și 7 (rămân aproximative până la
  o corecție explicită).
- Identitate vizuală proprie (paletă/branding) — stilul rămâne neutru.

## Istoricul deciziilor

Sesiunea completă de grilling (întrebări, recomandări, răspunsuri și motivația fiecărei
decizii) e păstrată în `.tmp/grill-me/harta-iezuiti.md`, la rădăcina workspace-ului
`Aplicatii`. Documentul de față e sinteza ei finală.
