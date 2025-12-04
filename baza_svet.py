import sqlite3

povezava = sqlite3.connect("baze/svet.sqlite")
kurzor = povezava.cursor()

tabela_kontinent = """
CREATE TABLE kontinent (
    id INTEGER PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL
);"""

tabela_drzava = """
CREATE TABLE drzava (
    id INTEGER PRIMARY KEY,
    ime TEXT NOT NULL,
    id_kontinenta REFERENCES kontinet(id),
    povrsina FLOAT CHECK (povrsina > 0)
);
"""

kurzor.execute(tabela_kontinent)
kurzor.execute(tabela_drzava)


def dodaj_kontinent(povezava, kontinent):
    kurzor = povezava.cursor()
    ukaz = "INSERT INTO kontinent(ime) VALUES (?)"
    kurzor.execute(ukaz, [kontinent])
    povezava.commit()
    return True


def dodaj_drzavo(povezava, kontinent, drzava, povrsina):
    kurzor = povezava.cursor()
    id_kontinenta = "SELECT id FROM kontinent WHERE ime = ?".fetchone()[0]
    ukaz = """INSERT INTO drzava(ime, id_kontinenta, povrsina)
    VALUES (?, ?, ?)
    """
    kurzor.execute(ukaz, [drzava, id_kontinenta, povrsina])
    povezava.commit()


kontinenti = [
    "Afrika",
    "Antarktika",
    "Avstralija",
    "Azija",
    "Evropa",
    "Južna Amerika",
    "Severna Amerika"
]

drzave = [
    ("Azija", "Japonska", 364555),
    ("Azija", "Kitajska", 9388211),
    ("Severna Amerika", "Združene države Amerike", 9147420),
    ("Evropa", "Avstrija", 7682300),
    ("Evropa", "Slovenija", 20140),
    ("Evropa", "Španija", 498800)
]

for kontinent in kontinenti:
    dodaj_kontinent(povezava, kontinent)

for kontinent, drzava, povrsina in drzave:
    dodaj_drzavo(povezava, kontinent, drzava, povrsina)


povezava.close()