# Združevanje in podpoizvedbe

## Združevanje

### Primeri z bazo `filmi`:

1. Poiščimo skupno dolžino in število vseh filmov v tabeli `film`.

2. Poiščimo skupno dolžino in število filmov, izdanih leta 2019.

3. Poiščimo skupno dolžino in število filmov za vsako leto.

4. Poiščimo skupno dolžino in število filmov z oceno vsaj 6,5 za vsako leto.

5. Poiščimo skupno dolžino in število filmov za vsako leto, ko je bila povprečna ocena vsaj 6,5.

6. Kaj vrne spodnja poizvedba?
```sql
SELECT leto, naslov
FROM film
GROUP BY leto
```


## Podpoizvedbe




### Primeri z bazo `filmi`

1. Filmi, ocenjeni bolje od povprečja.

2. Filmi z boljšo oceno kot najbolje ocenjen del Vojne zvezd.

3. Najbolje ocenjen film vsakega leta.

4. Filmi, ki so ocenjeni bolje od povprečja preteklih let.

5. Film, ki je najboljši in najbolje ocenjen v svojem letu.
