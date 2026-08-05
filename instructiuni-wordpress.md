# Instrucțiuni de integrare în WordPress

## Ce fișiere ai primit

- `harta.html` — pagina completă, de sine stătătoare, pentru previzualizare locală în browser (deschide-o direct sau vezi mai jos cum să o rulezi cu un mic server local).
- `harta-embed-wordpress.html` — **acesta e cel pe care îl copiezi în WordPress** (aceeași hartă, dar fără `<!doctype>`/`<html>`/`<head>`/`<body>`, care nu au ce căuta într-un bloc de conținut).
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

- Markerele sunt numerotate **cronologic** (1 = cea mai veche prezență iezuită în Cluj, 1579; 8 = revenirea din anii 2000), nu în ordinea din documentul sursă.
- Sub hartă apare o **legendă** cu toate cele 8 locații, în aceeași ordine cronologică — click/tap pe orice rând din listă duce harta direct la locația respectivă (dezgrupând clusterul dacă e nevoie) și îi deschide popup-ul automat.
- Harta se încarcă direct pe grupul dens din centrul istoric (locațiile 4, 5, 6), suficient de mărită încât acestea să apară deja separate. Locațiile 1, 3 și 8 nu sunt vizibile inițial (sunt la 400m - 3km distanță) — se ajunge la ele fie din legendă, fie dând zoom-out manual.
- Dacă totuși apare un cerc **albastru** cu o cifră (la zoom mic/după zoom-out), acela e un grup de mai multe locații, nu o locație individuală (locațiile individuale sunt cercuri **negre**) — un click/tap sau chiar hover susținut peste el îl desparte.
- Click/tap pe fiecare marker deschide un popup cu titlu (cu numărul cronologic în față), poză (unde există) și un rezumat scurt.
- Butonul „Citește mai mult” extinde textul la varianta completă.
- Testează și pe telefon — harta e gândită mobil-first.

## De reținut

- Harta nu are nevoie de nicio cheie API sau cont (folosește OpenStreetMap, gratuit).
- Coordonatele locațiilor 6 (Seminarul Sf. Iosif) și 7 (Strada Búza) sunt aproximative — dacă cineva cu cunoștințe locale poate confirma poziția exactă, se pot ajusta valorile `lat`/`lng` din cod pentru acele două locații.
- Momentan harta e doar în română (decizie din faza de planificare — vezi `.tmp/grill-me/harta-iezuiti.md`).
