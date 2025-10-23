# Združevanje in podpoizvedbe

## Združevanje

### Primeri z bazo `filmi`:

1. Poiščimo skupno dolžino in število vseh filmov v tabeli `film`.
```sql
SELECT SUM(dolzina), COUNT(*)
FROM film;
```

2. Poiščimo skupno dolžino in število filmov, izdanih leta 2019.
```sql
SELECT SUM(dolzina), COUNT(*)
FROM film
WHERE leto = 2019;
```

3. Poiščimo skupno dolžino in število filmov za vsako leto.

```sql
SELECT leto, SUM(dolzina), COUNT(*)
FROM film
GROUP BY leto;
```

4. Poiščimo skupno dolžino in število filmov z oceno vsaj 6,5 za vsako leto.

```sql
SELECT leto, SUM(dolzina), COUNT(*)
FROM film
WHERE ocena >= 6.5
GROUP BY leto;

```

5. Poiščimo skupno dolžino in število filmov za vsako leto, ko je bila povprečna ocena vsaj 6,5.

```sql
SELECT leto, SUM(dolzina), COUNT(*), AVG(ocena) as povp_ocena
FROM film
GROUP BY leto
HAVING povp_ocena >= 6.5
ORDER BY povp_ocena;
```

6. Kaj vrne spodnja poizvedba?
```sql
SELECT leto, naslov
FROM film
GROUP BY leto
```

Za vsako leto vrne eno vrstico - leto in nek naslov (ne vemo zares, katerega bo vrnilo). V nekaterih drugih različicah jezika SQL ta poizvedba ne bo delovala, v SQLite pa se samo obnaša nepričakovano.


## Podpoizvedbe




### Primeri z bazo `filmi`

1. Filmi, ocenjeni bolje od povprečja.

```sql
SELECT naslov, ocena
FROM film
WHERE ocena > (SELECT AVG(ocena) FROM film);
```

2. Filmi z boljšo oceno kot najbolje ocenjen del Vojne zvezd.

```sql
SELECT naslov, ocena
FROM film
WHERE ocena > (
    SELECT MAX(ocena)
    FROM film
    WHERE naslov LIKE 'Vojna zvezd%');
```


3. Najbolje ocenjen film vsakega leta.

```sql
SELECT leto, naslov
FROM film f1
WHERE ocena = (SELECT MAX(ocena) FROM film f2 WHERE f1.leto = f2.leto);
```

4. Filmi, ki so ocenjeni bolje od povprečja preteklih let.

5. Film, ki je najboljši in najbolje ocenjen v svojem letu.
