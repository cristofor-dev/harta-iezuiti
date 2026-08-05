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

**Decizie ulterioară, la cererea explicită a utilizatorului:** cerința "se văd toate 8 la
încărcare" a fost relaxată — utilizatorul a preferat un zoom inițial mult mai mare (fix, pe
grupul cel mai dens: locațiile 4, 5, 6, la doar 25-100m una de alta), chiar dacă asta lasă
locațiile 1, 3 și 8 în afara cadrului inițial (rămân accesibile prin legendă sau zoom-out
manual). Motivul: la orice zoom suficient de mic încât să încapă toate cele 8, grupul dens
tot se suprapunea vizual — fie ca markere individuale ating despre-atinse, fie ca un cluster
albastru care, deși nu se mai confundă cu un badge individual, tot ascundea detaliul. Zoom-ul
fix (18, centrat pe grup) elimină problema la origine: la încărcare, locațiile din centrul
istoric apar deja complet separate, fără nicio suprapunere sau clusterizare.

**Interacțiune adăugată:** hover pe un cluster (grup) declanșează, după ~450ms de cursor
susținut pe el (nu instant, ca să nu se activeze din greșeală doar trecând pe acolo), un
zoom automat spre acel grup — exact ca la click, dar și la simpla trecere cu mausul. Testat
cu Playwright: hover scurt (<450ms) sau cursor plecat înainte de prag nu schimbă zoom-ul;
hover susținut peste prag mărește zoom-ul și desparte grupul.

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

### Revizuire de design (la cererea utilizatorului: „după reguli profesioniste de UI/UX”)

**Sistem de culoare — un singur accent.** Varianta anterioară acumulase trei culori fără
ierarhie: pini negri, grupuri albastre, hover verde. Acum: neutre calde (paleta „stone”) +
**un** accent chihlimbariu (`#b45309`) pentru tot ce e interactiv sau activ. Chihlimbariul a
fost ales și cartografic: verdele intra în conflict cu parcurile de pe dalele OSM, albastrul
cu apa. _Notă: hover-ul verde fusese cerut explicit anterior; a fost înlocuit pentru
coerență, iar schimbarea i-a fost semnalată utilizatorului._

**Cronologia devine lizibilă.** Harta era „cronologică” doar prin numerotare — anii nu apărau
nicăieri. Acum fiecare loc își arată reperul temporal (1579, 1581, 1693 … anii 2000) în
cronologie, în popup (pastilă) și în tooltip. Lista de sub hartă e desenată ca o linie a
timpului, cu un fir vertical care leagă numerele.

**Pini vs. grupuri — limbaje vizuale diferite.** Pinul e un cerc plin, închis la culoare, cu
vârf care indică poziția exactă. Grupul e un cerc deschis, cu contur, fără vârf, cu numărul
plus cuvântul „locuri”. Confuzia „grup de 5” ↔ „locul 5” devine imposibilă structural, nu
doar cromatic.

**Stare activă sincronizată.** Deschiderea unui popup — din hartă sau din cronologie —
evidențiază simultan pinul și rândul corespunzător (`aria-current`).

**Alte corecții rezultate din testare:** buton „Vezi toate locurile” (vederea de ansamblu era
altfel greu de recuperat după zoom-ul inițial); înălțimea popup-ului calculată din înălțimea
reală a hărții, ca textul extins să nu fie tăiat; butonul de restrângere lipit jos în
popup-ul derulabil; zoom cu rotița doar după un click pe hartă (altfel harta „fura”
scroll-ul paginii); aducerea hărții în ecran când se alege un loc din capătul de jos al
cronologiei; focus vizibil pe tot ce e interactiv și respectarea `prefers-reduced-motion`.

### Izolarea CSS — blocul trăiește în tema altcuiva

Blocul e integrat într-un WordPress necunoscut, deci a fost testat automat într-o pagină cu o
temă deliberat ostilă (fonturi serif impuse, text centrat, `text-transform: uppercase` pe
titluri, `button:hover { … !important }`, `ol { list-style: upper-roman }`, chenare groase pe
`img`). Testul a scos patru defecte reale, invizibile în previzualizarea locală:

1. **Dalele hărții sunt elemente `<img>`** — regula `img { border: 6px solid }` a temei
   desena un chenar pe fiecare dală, brăzdând harta cu o grilă. Leaflet se apără singur doar
   pentru `max-width`; restul e neutralizat explicit pe panourile Leaflet.
2. **`button:hover { background: … !important }`** din temă câștiga: butonul devenea negru cu
   text chihlimbariu (contrast prost). De aici `!important` țintit pe culorile stărilor
   interactive — singurul mod de a bate `!important`-ul temei.
3. **Leaflet impune „Helvetica Neue”** în interiorul hărții, deci popup-urile și tooltip-urile
   ieșeau din sistemul tipografic al blocului.
4. **`h2`/`h3`/`p` preluau** `text-transform`, fontul și `line-height` de la temă (titluri cu
   majuscule, paragrafe cu `line-height: 2.4`).

Toate au fixuri comentate în cod, plus aserțiuni în suita de test — sunt exact genul de
defect care reapare la o „curățenie” ulterioară a CSS-ului.

### Sursă unică + generator

`harta.html` e sursa de adevăr; `harta-embed-wordpress.html` se generează din ea cu
`python sync-embed.py`. Cele două fișiere erau întreținute manual în paralel și divergaseră
deja o dată — cu ~850 de linii duplicate, sincronizarea manuală era o eroare care aștepta să
se întâmple.

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
