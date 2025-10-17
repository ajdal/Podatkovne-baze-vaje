# Osnove SQL

Oblika osnovne SQL poizvedbe:
```sql
SELECT stolpec1, stolpec2, stolpec3 / 1000 AS ime_stolpca, ROUND(stolpec4, 3), stolpec5
FROM tabela
WHERE (stolpec1 = 'vrednost1' AND ime_stolpca LIKE '%vrednost_' OR ime_stolpca > 25) AND stolpec6 IN ('vzhod', 'zahod')
ORDER BY stolpec1 DESC, stolpec4
LIMIT 32;
```

Vrstni red je pomemben! Ne moremo, na primer, urejanja (`ORDER BY`) opraviti pred izbiro (`WHERE`).

## Primeri z bazo `filmi`:

1. Izpišimo vse naslove filmov
```sql
SELECT naslov
FROM film
```

2. Izpišimo vse naslove, dolžine in ocene
```sql
SELECT naslov, dolzina, ocena
FROM film
```

3. Uredimo izpis padajoče po ocenah
```sql
SELECT naslov, dolzina, ocena
FROM film
ORDER BY ocena DESC
```

4. Zanimajo nas le filmi, ki so dolgi največ 2,5h
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina <= 150
ORDER BY ocena DESC
```

_Pazi na enačaj!_

5. A taki, ki niso krajši od 2h
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC
```

6. Zanima nas le prvih 20 takšnih filmov.
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC
LIMIT 20
```

7. Dodatno filme uredimo še naraščajoče po trajanju
```sql
SELECT naslov, dolzina, ocena
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC, dolzina
LIMIT 20
```

8. Stolpce uredimo po številu glasov na minuto filma.
```sql
SELECT naslov, glasovi/dolzina AS glasovi_dolzina
FROM film
WHERE dolzina BETWEEN 120 AND 150
ORDER BY ocena DESC, glasovi_dolzina
```
Stolpcu, ki ga izračunamo kot kvocient števila glasov in dolžine filma, priredimo ime `glasovi_dolzina`. To ime lahko nato uporabimo kot kriterij za urejanje, da ne ponavljamo formule.

9. Kako izračunamo skupno število glasov, ki so jih prejeli vsi filmi, katerih naslovi se začnejo z veliko tiskano črko A?
```sql
SELECT SUM(ocena)
FROM film
WHERE naslov LIKE 'A%'
```