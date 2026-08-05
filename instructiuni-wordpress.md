# Instrucțiuni de integrare în WordPress

## Ce fișiere ai primit

- `harta.html` — pagina completă, de sine stătătoare, pentru previzualizare locală în browser (deschide-o direct sau vezi mai jos cum să o rulezi cu un mic server local).
- `harta-embed-wordpress.html` — **acesta e cel pe care îl copiezi în WordPress** (aceeași hartă, dar fără `<!doctype>`/`<html>`/`<head>`/`<body>`, care nu au ce căuta într-un bloc de conținut).

> Fișierul de WordPress e **generat automat** din `harta.html`. Dacă cineva modifică harta,
> se editează `harta.html` și se rulează `python sync-embed.py` — nu se editează direct
> fișierul de embed, pentru că modificarea s-ar pierde.
- `content/Prezenta_Iezuitilor_Cluj-Napoca_1.md` — textul istoric complet, sursă pentru popup-uri.
- `content/photo/` — cele 8 fotografii de arhivă folosite în popup-uri.

## Pas 1 — Încarcă pozele în Media Library

Din `content/photo/`, încarcă în Media Library a site-ului WordPress aceste 8 fișiere:

Numele fișierelor păstrează numerotarea din documentul sursă original — nu mai corespunde cu
numerele de pe hartă, care sunt acum **cronologice** (vezi Pasul 4). Nu contează: fiecare
fișier e descris explicit mai jos.

| Fișier local | Locația (numerotare cronologică pe hartă) |
| --- | --- |
| `04-fosta-manastire-manastur_poarta-acces.jpg` | 1. Fosta mănăstire iezuită — Calea Mănăștur |
| `02-universitatea-babes-bolyai_fortepan-29760-1910.jpg` | 2. Universitatea Babeș-Bolyai |
| `05-convictus-nobilium_fortepan-56853-1969.jpg` | 4. Convictus Nobilium |
| `05-convictus-nobilium_fortepan-55012-1988-echinox.jpg` | 4. Convictus Nobilium |
| `01-biserica-piaristilor_fortepan-24209-1940.jpg` | 5. Biserica Piariștilor |
| `01-biserica-piaristilor_fortepan-202175-1972.jpg` | 5. Biserica Piariștilor |
| `03-strada-buza_fortepan-308559-1962.jpg` | 7. Strada Búza |
| `08-manastirea-zorilor_centrul-manresa-aerian.jpg` | 8. Mănăstirea Zorilor |

(Locațiile 3 — Biserica Franciscanilor — și 6 — Seminarul Sf. Iosif — nu au fotografie; nu
lipsește nimic.)

După încărcare, deschide fiecare poză în Media Library și copiază-i **URL-ul** (butonul „Copy URL to clipboard” din panoul din dreapta). WordPress păstrează de obicei numele fișierului neschimbat — dar dacă apare vreun sufix (`-1`, `-2`) din cauza unui conflict de nume, folosește URL-ul real, nu presupune.

## Pas 2 — Actualizează URL-urile pozelor în cod

Deschide `harta-embed-wordpress.html` cu un editor de text și caută linia:

```js
var PHOTO_BASE = "content/photo/";
```

**Dacă toate cele 8 URL-uri copiate au același „folder" de bază** (ex. toate încep cu `https://numelesitei.ro/wp-content/uploads/2026/08/` și numele fișierelor sunt neschimbate), e suficient să înlocuiești doar această linie:

```js
var PHOTO_BASE = "https://numelesitei.ro/wp-content/uploads/2026/08/";
```

**Dacă WordPress a schimbat vreun nume de fișier** (conflict de nume), găsește liniile `photos: [PHOTO_BASE + "..."]` pentru locația respectivă și înlocuiește-le cu URL-ul complet copiat din Media Library, între ghilimele, fără `PHOTO_BASE +`.

## Pas 3 — Inserează codul în pagina WordPress

1. Creează o pagină/articol nou (sau editează una existentă).
2. Adaugă un bloc **„Custom HTML”** (Gutenberg) — se caută în meniul „+” de adăugare bloc. Dacă site-ul folosește Elementor/Divi/alt builder, caută widget-ul echivalent, de obicei numit **„HTML”** sau **„Cod HTML”**.
3. Deschide `harta-embed-wordpress.html` (cel actualizat la Pasul 2), selectează tot conținutul (Ctrl+A) și copiază-l (Ctrl+C).
4. Lipește-l în blocul „Custom HTML”.
5. Salvează/publică pagina și verifică previzualizarea — ar trebui să vezi harta cu cele 8 markere.

## Pas 4 — Verificare rapidă după publicare

- Punctele sunt numerotate **cronologic** (1 = cea mai veche prezență iezuită în Cluj, 1579; 8 = revenirea din anii 2000), nu în ordinea din documentul sursă. Fiecare loc își arată și anul.
- Sub hartă apare **cronologia** — toate cele 8 locuri, în ordine, cu anul fiecăruia. Click/tap pe orice rând duce harta la locul respectiv și îi deschide detaliile; rândul ales și punctul de pe hartă se colorează simultan, ca să vezi unde te afli.
- Harta se încarcă direct pe grupul dens din centrul istoric (locurile 4, 5, 6), suficient de mărită încât acestea să apară deja separate. Locurile 1, 3 și 8 nu sunt vizibile inițial (sunt la 400 m – 3 km distanță) — se ajunge la ele din cronologie sau din butonul **„Vezi toate locurile”** din colțul hărții.
- Un cerc **alb, cu contur și cuvântul „locuri”** înseamnă mai multe locuri grupate, nu un loc individual (locurile individuale sunt cercuri **pline, închise la culoare, cu vârf în jos**). Click/tap — sau doar ținerea cursorului peste el — îl desparte.
- Click/tap pe un punct deschide detaliile: anul, titlul, poza (unde există) și un rezumat scurt; **„Citește mai mult”** extinde textul complet.
- Pe desktop, trecerea cu mausul peste un punct îi arată denumirea și îl colorează.
- Rotița mausului dă zoom doar după ce dai un click pe hartă — altfel derulezi pagina normal, fără ca harta să „fure” scroll-ul.
- Testează și pe telefon — harta e gândită mobil-first.

## De reținut

- Harta nu are nevoie de nicio cheie API sau cont (folosește OpenStreetMap, gratuit).
- Coordonatele locațiilor 6 (Seminarul Sf. Iosif) și 7 (Strada Búza) sunt aproximative — dacă cineva cu cunoștințe locale poate confirma poziția exactă, se pot ajusta valorile `lat`/`lng` din cod pentru acele două locații.
- Momentan harta e doar în română (decizie din faza de planificare — vezi `.tmp/grill-me/harta-iezuiti.md`).
