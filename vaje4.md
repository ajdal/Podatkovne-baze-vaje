# Stikanje

```sql
SELECT stolpci
FROM tab1
   [NATURAL] [LEFT | RIGHT | FULL] JOIN tab2 [ON pogoj | USING (stolpci)]
WHERE pogoj
GROUP BY stolpci
HAVING pogoj
ORDER BY stolpci
LIMIT stevilo
```

* `ON pogoj` - poveže vrstice iz obeh tabel, kjer velja pogoj (npr. `ON oseba.id = vloga.oseba`)
* `USING` - stakne po istoimenskih stolpcih v obeh tabelah, ki jih navedemo (npr. `USING id`)
* `NATURAL JOIN` - stakne po vseh istoimenskih stolpcih v obeh tabelah. Pogoja stikanja potem ne navajamo. Moramo pa biti previdni, saj lahko poveže tudi stolpce, za katere tega ne želimo.
* stikanje se izvede pred filtriranjem z `WHERE`!


## Različni tipi stikanja

Dano imamo podatkovno bazo naročil s tabelama `stranka` in `narocilo`.

Tabela `stranka`:
| id | ime    |
|----|--------|
| 1  | Alenka |
| 2  | Branko |
| 3  | Cvetka |
| 4  | David  |

Tabela `narocilo`:
| id | kolicina | stranka |
|----|----------|---------|
| 1  | 500      | 2       |
| 2  | 300      | 6       |
| 3  | 800      | 2       |
| 4  | 150      | 1       |
| 5  | 400      | 4       |

Povezati želimo količino naročenih izdelkov z imeni strank.

### Notranji stik (INNER JOIN)

Pridobiti želimo le vrstice, za katere poznamo vnos tako v levi kot v desni tabeli.

```sql
SELECT *
FROM stranka
    JOIN narocilo ON stranka.id = narocilo.stranka
```

Če izberemo vse stolpce (`*`), poizvedba vrne vse stolpce iz prve (`stranka`), nato pa še vse stolpce iz druge tabele (`narocilo`), za vrstice, kjer se id stranke ujema s stolpcem stranka v tabeli `narocilo`:

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 2  | Branko | 1    | 500      | 2       |
| 2  | Branko | 3    | 800      | 2       |
| 1  | Alenka | 4    | 150      | 1       |
| 4  | David  | 5    | 400      | 4       |

_Opomba:_ Pri izpisu je stolpec `id` iz tabele `narocilo` označen kot `id:1`, da ločimo enako poimenovana stolpca iz obeh tabel (tako bo izgledal tudi rezultat v SQLite Studiu).

V stavku `SELECT` lahko torej izberemo katerikoli stolpec iz te staknjene tabele.
Denimo, da želimo prikazati le ime stranke, id naročila in količino:

```sql
SELECT ime, narocilo.id AS narocilo_id, kolicina
FROM stranka
    JOIN narocilo ON stranka.id = narocilo.stranka
```
Poizvedba vrne:

| ime    | narocilo_id | kolicina |
|--------|-------------|----------|
| Alenka | 4           | 150      |
| Branko | 1           | 500      |
| Branko | 3           | 800      |
| David  | 5           | 400      |

Ker se stolpec `id` nahaja tako v tabeli `stranka`, kot v tabeli `narocilo`, moramo povedati, iz katere tabele želimo pridobiti stolpec `id` → `narocilo.id`. V izogib napakam, stolpec v rezultatu poimenujemo `narocilo_id`.

### Zunanji stik (OUTER JOIN)

Ločimo tri vrste zunanjih stikov.

**Levi zunanji stik** (`LEFT OUTER JOIN`) ohrani vse vrstice iz prve tabele – vse stranke:

```sql
SELECT *
FROM stranka
    LEFT JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1  | Alenka | 4    | 150      | 1       |
| 2  | Branko | 1    | 500      | 2       |
| 2  | Branko | 3    | 800      | 2       |
| 3  | Cvetka | NULL | NULL     | NULL    |
| 4  | David  | 5    | 400      | 4       |

Ker Cvetka ni opravila nobenega naročila, stolpci iz desne tabele (`narocilo`) dobijo vrednost `NULL`.

**Desni zunanji stik** (RIGHT OUTER JOIN) ohrani vse vrstice iz druge tabele - vsa naročila:

```sql
SELECT *
FROM stranka
    RIGHT JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1     | Alenka    |	4 |	150 | 1 |
| 2     | Branko    |	1 |	500 | 2 |
| 2     | Branko    |	3 |	800 | 2 |
| 4     | David     |	5 |	400 | 4 |
| NULL  | NULL      |	2 |	300 | 6 |

Opazimo, da se ohrani vrstni red iz leve tabele.

**Polni zunanji stik** (FULL OUTER JOIN) ohrani vse vrstice iz obeh tabel:

```sql
SELECT *
FROM stranka
    FULL JOIN narocilo ON stranka.id = narocilo.stranka
```

| id | ime    | id:1 | kolicina | stranka |
|----|--------|------|----------|---------|
| 1  | Alenka | 5    | 150      | 1       |
| 2  | Branko | 2    | 500      | 2       |
| 2  | Branko | 4    | 800      | 2       |
| 3  | Cvetka | NULL | NULL     | NULL    |
| 4  | David  | 5    | 400      | 4       |
| NULL| NULL   |	2    | 300      | 6       |

## Primeri z bazo `filmi`

1. Naslovi filmov in imena glavnih igralcev (urejeno po imenih, nato pa po naslovih).

* Tabela `vloga` povezuje igralce in režiserje iz tabele `oseba` s filmi iz tabele `film` .
* Staknemo vrstice z istim id filma in id osebe.
* Tip vloge mora biti `'I'`.
* Mesto vloge mora biti 1.

```sql
SELECT naslov, ime
FROM film
    JOIN vloga ON film.id = vloga.film
    JOIN oseba ON oseba.id = vloga.oseba
WHERE tip = 'I' AND mesto = 1
ORDER BY ime, naslov
```

_Ker so ime, naslov, tip in mesto prisotni vsak le v eni tabeli, nam imena tabele ni treba podati ob imenu stolpca. Stolpec id se pojavi tako v tabeli film, kot v tabeli oseba, zato smo ju zapisali kot `film.id` in `oseba.id`_

2. Za vsakega režiserja (izpišite ga z IDjem in imenom) izpišite skupno dolžino filmov, ki jih je režiral (brez igranja). Rezultate uredite po imenu režiserja.

* Staknemo tabele `oseba`, `vloga`, `film` po ID-jih.
* Izberemo le vrstice, kjer je tip `'R'` (režiser) – to moramo storiti pred združevanjem (z `WHERE`).
* Združimo po id in imenu osebe – v `SELECT` imamo lahko le stolpce, po katerih združujemo (z `GROUP BY`) in agregirane stolpce (`SUM`, `MIN`, `MAX`, ...).
* Uredimo.

```sql
SELECT oseba.id, ime, SUM(film.dolzina)
FROM oseba
    JOIN vloga ON oseba.id = vloga.oseba
    JOIN film ON vloga.film = film.id
WHERE vloga.tip = 'R'
GROUP BY oseba.id, ime
ORDER BY ime;
```

3. Za vsak žanr (izpišite ga z imenom) izpišite število različnih igralcev in število različnih režiserjev, ki so sodelovali pri filmih tega žanra. Rezultate uredite padajoče po vsoti števila igralcev in števila režiserjev (če se nekdo pojavi tako kot igralec kot režiser, se tukaj šteje dvakrat).


* Sestaviti moramo seznam igralcev in seznam režiserjev za vsak žanr, nato pa prešteti le različne za vsako vlogo.
* Tabele oseba tu ne potrebujemo, ker nas ne zanimajo imena, ampak le število.
* Stakniti bo treba tabele `film`, `pripada` in `zanr`, da bomo lahko združili filme po žanrih in izpisali nazive žanrov.
* Ločeno bomo morali poiskati igralce in režiserje (osebe z dvojno vlogo se štejejo k obema vlogama). To lahko storimo na dva načina:
    1. Ustvarimo vse pare igralec-režizer za posamezen film, nato izberemo le ustrezne.
    2. Ločeno naredimo gnezdeni poizvedbi za igralce in režiserje.


1. Ustvarimo pare vlog:

* Začnemo s tabelo `film` in ji pripnemo tabeli `pripada` in `zanr`, da dobimo podatke o žanrih filmov.
* Vse skupaj staknemo z dvema kopijama tabele `vloga` - eno vlogo imenujno `igralec`, drugo pa `reziser`.
* Uporabimo **levi** stik po id filma ter poskrbimo, da bodo v prvem stiku upoštevane samo vrstice z vlogo `'I'`, v drugem pa z vlogo `'R'`.
    * z levim stikom poskrbimo, da bo vsaki vrstici iz staknjene tabele filmov in žanrov pripadla vrstica v rezultatu, tudi če ni vlog tega tipa;
    * če bi uporabili notranji stik, bi izgubili filme, ki nimajo igralcev ali režiserjev (na primer film Drobizki ima dva režiserja in nobenega igralca);
* Dobimo vse pare oblike (igralec, reziser) za posamezen film.
* Ker nas zanimajo podatki za posamezne žanre, jih združimo po žanrih.
* Preštejemo število **različnih** igralcev in število **različnih** režiserjev, ter vrednostima priredimo ime (`AS stevilo_igralcev`), da se lahko pri urejanju sklicujemo nanju.
* Uredimo po vsoti obeh vrednosti.

```sql
SELECT naziv,
    COUNT(DISTINCT igralec.oseba) AS stevilo_igralcev,
    COUNT(DISTINCT reziser.oseba) AS stevilo_reziserjev
FROM film
  JOIN pripada ON film.id = pripada.film
  JOIN zanr ON pripada.zanr = zanr.id
  LEFT JOIN vloga AS igralec ON film.id = igralec.film AND igralec.tip = 'I'
  LEFT JOIN vloga AS reziser ON film.id = reziser.film AND reziser.tip = 'R'
GROUP BY zanr.id, naziv
ORDER BY stevilo_igralcev + stevilo_reziserjev DESC;
```

2. Uporabimo pogojno štetje s `CASE`:

* Začnemo s tabelo `film` in ji pripnemo tabeli `pripada` in `zanr`, da dobimo podatke o žanrih filmov.
* Tokrat tabelo `vloga` pripnemo le enkrat, z običajnim notranjim stikom
* Dobimo seznam vseh vlog za vsak film.
* Ker nas zanimajo podatki za posamezne žanre, jih združimo po žanrih.
* Preštejemo število **različnih** igralcev in število **različnih** režiserjev, tokrat z uporabo pogojnega stavka `CASE`. Ponovno vrednostima priredimo ime (`AS stevilo_igralcev`), da se lahko pri urejanju sklicujemo nanju.
    * `CASE` omogoča izbiro vrednosti glede na pogoj, podobno kot to počnemo z `if` stavkom v Pythonu.
    * Poizvedba `SELECT (CASE WHEN vloga.tip = 'I' THEN vloga.oseba END) FROM vloga` bo sestavila stolpec, kjer bodo v vrsticah, ki pripadajo igralcem, njihovi id-ji, v vrsticah režiserjev pa bo vrednost `NULL`.
    * Ker agregacija s `COUNT` ne upošteva vrednosti `NULL` bo torej preštevanje unikatnih vrednosti v stolpcu vrnilo natanko število različnih igralcev.
* Uredimo po vsoti obeh vrednosti.


```sql
SELECT
    zanr.naziv AS zanr,
    COUNT(DISTINCT CASE WHEN vloga.tip = 'I' THEN vloga.oseba END) AS st_igralcev,
    COUNT(DISTINCT CASE WHEN vloga.tip = 'R' THEN vloga.oseba END) AS st_reziserjev
FROM zanr
JOIN pripada ON zanr.id = pripada.zanr
JOIN film ON pripada.film = film.id
JOIN vloga ON film.id = vloga.film
GROUP BY zanr.id, zanr.naziv
ORDER BY st_igralcev + st_reziserjev DESC;
```