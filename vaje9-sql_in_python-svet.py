import sqlite3

povezava = sqlite3.connect("baze/svet.sqlite")
kurzor = povezava.cursor()


# Ustvarimo tabeli kontinent in drzava
tabela_kontinent = """
CREATE TABLE kontinent (
    id INTEGER PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL
);"""

tabela_drzava = """
CREATE TABLE drzava (
    id INTEGER PRIMARY KEY,
    ime TEXT UNIQUE NOT NULL,
    id_kontinenta NOT NULL REFERENCES kontinet(id),
    povrsina FLOAT CHECK (povrsina > 0),
    UNIQUE (ime, id_kontinenta)
);
"""

kurzor.execute(tabela_kontinent)
kurzor.execute(tabela_drzava)


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


def dodaj_drzavo(povezava, kontinent, drzava, povrsina):
    kurzor = povezava.cursor()
    id_kontinenta = kurzor.execute("SELECT id FROM kontinent WHERE ime = ?", [kontinent]).fetchone()[0]
    if id_kontinenta is None:
        return False
    ukaz = """INSERT INTO drzava(ime, id_kontinenta, povrsina)
    VALUES (:ime, :id_kontinenta, :povrsina)
    """
    try:
        kurzor.execute(ukaz, {"ime": drzava, "id_kontinenta": id_kontinenta, "povrsina": povrsina})
        povezava.commit()
    except sqlite3.IntegrityError as e:
        print(f"Napaka pri vstavljanju države {drzava}: {e.sqlite_errorname}")
        return False
    return True


def izpisi_drzave(povezava):
    kurzor = povezava.cursor()
    poizvedba = "SELECT ime FROM drzava"
    for drzava, in kurzor.execute(poizvedba):
        print(drzava)


def drzave_kontinenta(povezava, kontinent):
    kurzor = povezava.cursor()
    poizvedba = f"""
    SELECT drzava.ime
    FROM drzava
        JOIN kontinent ON kontinent.id = drzava.id_kontinenta
    WHERE kontinent.ime = ?
    """
    for drzava, in kurzor.execute(poizvedba, (kontinent,)):
        print(drzava)


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

# Vstavimo kontinente
for kontinent in kontinenti:
    dodaj_kontinent(povezava, kontinent)

# Vstavimo države
for kontinent, drzava, povrsina in drzave:
    dodaj_drzavo(povezava, kontinent, drzava, povrsina)

# Izpis vseh držav
print("Vse države na svetu:")
print("---------------------------------------------------")
izpisi_drzave(povezava)
print("===================================================")

kontinent = input("Vnesi ime kontinenta:")
print(f"Države na kontinentu {kontinent}")
print("---------------------------------------------------")
drzave_kontinenta(povezava, kontinent)
print("===================================================")

povezava.close()