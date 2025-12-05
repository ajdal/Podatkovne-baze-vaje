import sqlite3

povezava = sqlite3.connect("baze/filmi.sqlite")
kurzor = povezava.cursor()

# 1. Marsovec
print("Podatki o filmu Marsovec".upper())
print("---------------------------------------------------")

poizvedba = "SELECT * FROM film WHERE naslov = 'Marsovec'"
marsovec = kurzor.execute(poizvedba).fetchone()

stolpci = [opis[0] for opis in kurzor.description]
for stolpec, vrednost in zip(stolpci, marsovec):
    print(f"{stolpec}: {vrednost}")


print("===================================================")

# 2. Vsi filmi
print("Vsi naslovi filmov:".upper())
print("---------------------------------------------------")

poizvedba = "SELECT naslov FROM film"
rezultat = kurzor.execute(poizvedba)
for naslov, in rezultat:
    print(naslov)

print("===================================================")

# 3. 20 najbolje ocenjenih filmov
print("20 najboljših filmov".upper())
print("---------------------------------------------------")

poizvedba = """
SELECT naslov 
FROM film 
ORDER BY ocena 
DESC LIMIT 20
"""
dobri_filmi = kurzor.execute(poizvedba)
for naslov, in dobri_filmi:
    print(naslov)

print("===================================================")

# 4. Število filmov po oznakah
print("Število filmov po oznakah:".upper())
print("---------------------------------------------------")

poizvedba = """
SELECT oznaka, COUNT(*)
FROM film
GROUP BY oznaka
"""
for oznaka, stevilo in kurzor.execute(poizvedba):
    print(f"Z oznako {repr(oznaka)} je označenih {stevilo} filmov.")


print("===================================================")

# 5. Število dolgih filmov vsakega režiserja
print("Število dolgih filmov vsakega režiserja:".upper())
print("---------------------------------------------------")

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

kurzor.close()
povezava.close()