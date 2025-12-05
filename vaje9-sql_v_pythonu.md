# SQL v Pythonu

## Primeri na bazi Filmi

Celotno kodo brez razlage najdete v skripti [sql_in_python-filmi.py](sql_in_python-filmi.py). Bazo najdete na spletni učilnici.

Modul `sqlite3`, ki je del standardne namestitve Pythona, nam omogoča delo s SQLite podatkovnimi bazami. Bazo odpremo tako, da se nanjo povežemo:

```python
import sqlite3

povezava = sqlite3.connect("filmi.sqlite")
```

Za izvajanje poizvedb bomo uporabili objekt tipa kurzor, ki ga ustvarimo na objektu `povezava`:

```python
kurzor = povezava.cursor()
```

Kurzor bomo uporabili za izvajanje poizvedb na bazi.

Na koncu programa, ko zaključimo z delom z bazo


**1) Izpišite podatke o filmu Marsovec.**
Pripravimo si SQL poizvedbo v obliki niza. Kurzorju nato povemo, da želimo izvesti to poizvedbo (metoda `execute`). 
```python
poizvedba = "SELECT * FROM film WHERE naslov = 'Marsovec'"
rezultat = kurzor.execute(poizvedba)
print(rezultat)
```
Rezultat poizvedbe bo objekt tipa kurzor:
```
<sqlite3.Cursor object at 0x000002C607715E40>
```

Vrednosti dobimo šele, ko jih eksplicitno zahtevamo. Ker nas zanima le en rezultat, uporabimo kar metodo `fetchone`.
```python
marsovec = rezultat.fetchone()
print(marsovec)
```
Rezultat v spremenljivki `marsovec` je nabor:
```
(3659388, 'Marsovec', 144, 2015, 8.0, 80, 694443, 228433663, 'PG-13', 'An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.')
```

_Bonus:_

Izpis lahko seveda še uredimo, na primer z f-nizi. Če želimo biti "fancy" in imena stolpcev pridobiti avtomatsko, lahko uporabimo lastnost [`description`](https://peps.python.org/pep-0249/#description) objekta tipa `cursor`, ki vsebuje podatke za vsak stolpec. Prvi element opisa za vsak stolpec je njegovo ime.
```python
stolpci = [opis[0] for opis in kurzor.description]
for stolpec, vrednost in zip(stolpci, marsovec):
    print(f"{stolpec}: {vrednost}")
```
Izpis:
```
id: 3659388
naslov: Marsovec
dolzina: 144
leto: 2015
ocena: 8.0
metascore: 80
glasovi: 694443
zasluzek: 228433663
oznaka: PG-13
opis: An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive.
```

**2) Izpišite vse naslove filmov.**

Naloge se lahko lotimo podobno kot prej: zapišemo poizvedbo in jo izvedemo. Ker imamo tokrat opravka z večjim številom vrstic, lahko uporabimo metodo `fetchall`, ki vse vrstice vrne kot seznam.

```python
poizvedba = "SELECT naslov FROM film"
rezultat = kurzor.execute(poizvedba).fetchall()
print(rezultat)
```
Ker imamo pri delu s podatkovnimi bazami pogosto opravka z večjo količino podatkov, je lahko branje vseh rezultatov v seznam prostorsko (in celo časovno) zelo neučinkovito. Kadar ne potrebujemo vseh podatkov naenkrat, je lepše, da se s for zanko sprehodimo čez rezultat (tipa `cursor`) in podatke pridobivamo enega po enega:

```python
rezultat = kurzor.execute(poizvedba)
for naslov in rezultat:
    print(naslov)
```

Rezultat bo nekaj takega (s precej več vrsticami):
```
('The Birth of a Nation',)
("Intolerance: Love's Struggle Throughout the Ages",)
('Broken Blossoms or The Yellow Man and the Girl',)
('Das Cabinet des Dr. Caligari',)
('The Kid',)
('Körkarlen',)
('Dr. Mabuse, der Spieler',)
('Nosferatu, simfonija groze',)
('Naše gostoljubje',)
('Resitev v zadnjem trenutku',)
```

Čeprav smo sedaj vrnili le en stolpec, so posamezni elementi (vrstice) rezultata še vedno nabori. Če želimo posamezne elemente, moramo torej vrstice sproti razbiti `for naslov, in rezultat` (razbijamo kot nabor z enim elementom) ali pa pri uporabi/izpisu izbrati ustrezni (edini) element `print(naslov[0])`.


**3) Izpišite 20 najbolje ocenjenih filmov.**
Če je poizvedba daljša, jo lahko za boljšo preglednost razbijemo na več vrstic. V tem primeru moramo niz zapakirati v trojne narekovaje. 

```python
poizvedba = """
SELECT naslov 
FROM film 
ORDER BY ocena 
DESC LIMIT 20
"""
dobri_filmi = kurzor.execute(poizvedba)
for naslov, in dobri_filmi:
    print(naslov)
```

**4) Izpišite število filmov glede na oznako**

Združimo filme po oznakah. Zaradi lepšega 

```python
poizvedba = """
SELECT oznaka, COUNT(*)
FROM film
GROUP BY oznaka
"""
for oznaka, stevilo in kurzor.execute(poizvedba):
    print(f"Z oznako {repr(oznaka)} je označenih {stevilo} filmov.")
```
Opazimo, da se ime skupine za filme brez oznake (oznaka je `NULL`) v Pythonu prikaže kot `None`. Funkcijo `repr` smo uporabili, da vidimo razliko med ostalimi imeni oznak, ki so običajni nizi, ter `None`.

**5) Izpišite režiserje filmov in naslove njihovih filmov, ki trajajo več kot 2 uri in pol**

Kot že znamo, moramo za to poizvedbo povezati podatke iz več tabel: oseba, vloga in film.

```python
poizvedba = """
SELECT oseba.ime, COUNT(DISTINCT naslov) AS st_filmov
FROM oseba
    JOIN vloga ON oseba.id = vloga.oseba
    JOIN film ON vloga.film = film.id
WHERE dolzina > 150 AND vloga.tip = 'R'
GROUP BY oseba.id, oseba.ime
ORDER BY st_filmov DESC, oseba.ime ASC;
"""

for reziser, st_filmov in kurzor.execute(poizvedba):
    print(f"{reziser}: {st_filmov}")
```

Če bi želeli, lahko izpišemo tudi režiserje brez filmov, daljših od 150 minut. To vam prepuščam za vajo. _Namig: spomnite se naloge s kolokvija. Verjetno bo treba uporabiti levi stik, morda prav pride tudi `COALESCE`._

## Primeri na bazi Svet

Celotno kodo brez razlage najdete v skripti [sql_in_python-svet.py](sql_in_python-filmi.py).

**1. Ustvarimo bazo `svet`**

Če se s `connect` povežemo na bazo, ki ne obstaja, se ustvari nova baza. Ustvarimo bazo v datoteki `svet.sqlite`:

```python
import sqlite3

povezava = sqlite3.connect("baze/svet.sqlite")
```

V niza `tabela_kontinent` in `tabela_drzava` zapišemo ukaza za ustvarjanje tabel. Pri tem upoštevamo lastnosti stopcih v navodilu:
* `ime` kontinenta je zahtevana vrednost (`NOT NULL`),
* `ime` države je zahtevana vrednost,
* `povrsina` je večja od 0.

Dodatno zahtevamo še, da se imena kontinentov ne ponavljajo (nimamo dveh različnih kontinentov z istim imenom). Zahtevamo tudi, da država zagotovo pripada kontinentu. Enako kot s poizvedbami (`SELECT`), moramo tudi ta dva ukaza izvesti (`execute`).

```python
tabela_kontinent = """
CREATE TABLE kontinent (
    id INTEGER PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL
);"""

tabela_drzava = """
CREATE TABLE drzava (
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    id_kontinenta NOT NULL REFERENCES kontinet(id),
    povrsina FLOAT CHECK (povrsina > 0)
);
"""

kurzor.execute(tabela_kontinent)
kurzor.execute(tabela_drzava)
```

**2. Dodajanje kontinentov**

Napišimo funkcijo `dodaj_kontinent`, ki sprejme povezavo na bazo in ime kontinenta. Funkcija naj kontinent vstavi v tabelo `kontinenti`.

Podobno kot s poizvedbami `SELECT`, lahko tudi ostale ukaze za delo z bazo "zapakiramo" v niz in izvedemo z `execute`. Da se izognemo morebitnim težavam z ranljivostjo SQL injection (primeri na koncu poglavja), uporabimo vstavljanje vrednosti. Na mestu v nizu, kjer želimo vstaviti vrednost (ime kontinenta), postavimo vprašaj. Ob izvedbi nato kot seznam ali nabor navedemo vse vrednostim, ki jih želimo vstaviti.

```python
def dodaj_kontinent(povezava, kontinent):
    """Doda nov kontinent."""
    kurzor = povezava.cursor()
    ukaz = "INSERT INTO kontinent(ime) VALUES (?)"
    kurzor.execute(ukaz, [kontinent])
    povezava.commit()
```
__Pozor: tudi kadar vstavljamo le eno vrednost, jo moramo zapakirati v nabor ali seznam__

Sedaj lahko vstavimo Evropo in Azijo:

```python
dodaj_kontinent(povezava, "Evropa")
dodaj_kontinent(povezava, "Azija")
```

Pri vstavljanju podatkov v bazo lahko pride do napake, tudi, kadar smo poizvedbe sestavili pravilno. Primer: v tabelo smo že vstavili Evropo. Če pomotoma Evropo poskusimo ponovno, bomo dobili napako:

```
sqlite3.IntegrityError: UNIQUE constraint failed: kontinent.ime
```

Ker ponavadi ne želimo, da se aplikacija sesuje ob vsaki napaki, je pametno te napake poloviti v `try/except` bloku in napako zabeležiti (na standardni izhod ali pa v datoteko) ter z vrnjeno vrednostjo klicatelju povedati, da se ukaz ni izvedel (Evrope nismo ponovno vstavili v tabelo). Spodnja funkcija ob uspešnem vstavljanju vrne `True`, ob neuspešnem pa `False`.

```python
def dodaj_kontinent(povezava, kontinent):
    """Doda nov kontinent."""
    kurzor = povezava.cursor()
    ukaz = "INSERT INTO kontinent(ime) VALUES (?)"
    try:
        kurzor.execute(ukaz, [kontinent])
        povezava.commit()
    except sqlite3.IntegrityError as e:
        print(f"Napaka pri vstavljanju kontinenta {kontinent}: {e.sqlite_errorname}")
        return False
    return True
```

Namesto `True` in `False` je včasih smiselno vrniti tudi številko vrstice, ki smo jo vstavili: `kurzor.lastrowid` (če za primarni ključ id uporabljamo stolpec tipa integer, je ta enaka idju.), v primeru neuspeha pa `None`.

**3. Dodajanje držav**

Vrednosti v SQL ukaze lahko vstavljamo tudi po imenih, da zmanjšamo možnost napake. V tem primeru vrednosti metodi `execute` podamo v obliki slovarja:

```python
def dodaj_drzavo(povezava, kontinent, drzava, povrsina):
    kurzor = povezava.cursor()
    id_kontinenta = kurzor.execute("SELECT id FROM kontinent WHERE ime = ?", [kontinent]).fetchone()[0]
    if id_kontinenta is None:
        return False
    ukaz = """
    INSERT INTO drzava(ime, id_kontinenta, povrsina)
    VALUES (:ime, :id_kontinenta, :povrsina)
    """
    try:
        kurzor.execute(ukaz, {"ime": drzava, "id_kontinenta": id_kontinenta, "povrsina": povrsina})
        povezava.commit()
    except sqlite3.IntegrityError as e:
        print(f"Napaka pri vstavljanju države {drzava}: {e.sqlite_errorname}")
        return False
    return True
```

**4. Izpišimo vse države**

V for zanki eno po eno izpisujemo imena držav:

```python
def izpisi_drzave(povezava):
    kurzor = povezava.cursor()
    poizvedba = "SELECT ime FROM drzava"
    for drzava, in kurzor.execute(poizvedba):
        print(drzava)
```

V praksi bo pogosto pametneje rezultate poizvedbe vrniti kot rezultat funkcije ali pa funkcijo celo pripraviti v obliki iteratorja (vrednosti eno po eno "vračamo" z `yield`.). Več o tem na vajah čez dva tedna. 



**5. Izpišimo države na enem kontinentu**

```python
def drzave_kontinenta(povezava, kontinent):
    kurzor = povezava.cursor()
    poizvedba = f"""
    SELECT drzava.ime
    FROM drzava
        JOIN kontinent ON kontinent.id = drzava.id_kontinenta
    WHERE kontinent.ime = '{kontinent}'
    """
    # for drzava in kurzor.execute(poizvedba, [kontinent]):
    for drzava, in kurzor.execute(poizvedba):
        print(drzava)
```



```python
def drzave_kontinenta_ranljiva(povezava, kontinent):
    kurzor = povezava.cursor()
    poizvedba = f"""
    SELECT drzava.ime
    FROM drzava
        JOIN kontinent ON kontinent.id = drzava.id_kontinenta
    WHERE kontinent.ime = '{kontinent}'
    """
    # for drzava in kurzor.execute(poizvedba, [kontinent]):
    for drzava, in kurzor.execute(poizvedba):
        print(drzava)

```

