# Ustvarjanje tabel

```sql
CREATE TABLE tabela (
    stolpec tip 
        [PRIMARY KEY]                   -- stolpec je glavni ključ tabele
        [NOT NULL]                      -- vrednost stolpca ne sme biti NULL
        [UNIQUE]                        -- vrednosti v stolpcu se ne smejo ponavljati
        [CHECK (pogoj)]                 -- pogoj, ki mora veljati za vse vrednosti v stopcu
        [DEFAULT (vrednost)]            -- privzeta vrednost, ki se uporabi, če vrednosti ne podamo ob vstavljanju
        [REFERENCES tabela2(stolpec2)]  -- tuji ključ: vredost stolpca povezuje tabelo s tabelo tabela2 preko stolpca stolpec2
        [AUTOINCREMENT]                 -- če vrednost stolpca ni podana, se avtomatsko uporabi za eno večja vrednost od prej največje
    [PRIMARY KEY (st1, st2, ...)]       -- glavni ključ tabele je sestavljen iz več stolpcev
    [UNIQUE (st1, st2, ...)]            -- kombinacija vrednosti v stolpcih se ne sme ponavljati
    [CHECK (pogoj)]                     -- pogoj, ki vključuje več stolpcev
    [FOREIGN KEY (st1, st2, ...)] REFERENCES tabela2(s1, s2, ...) -- tuji ključ je sestavljen iz več stolpcev
    ...
);
```
Določila v oglatih oklepajih so opcijska. Nabor in imena določil se lahko razlikujejo med različnimi tipi podatkovnih baz (RDMBS - npr. SQLite, MySQL, PostgreSQL, MariaDB, Microsoft SQL Server, Oracle Database, ...).

Opomba: Določilo `PRIMARY KEY`, če je stolpec tipa `INTEGER`, vključuje pogoj `NOT NULL` ter avtomatsko poskrbi za prirejanje/povečevanje vrednosti, če ta ni podana, zato določilo `AUTOINCREMENT` ni potrebno. ([več o tem](https://www.sqlitetutorial.net/sqlite-primary-key/))

Tipi v `SQLite`:
* `integer` - celo ševilo
* `real`, `numeric(p, s)`, `decimal(p, s)` - decimalno število
* `text` - niz
* `char(n)`, `varchar(n)` - omejena dolžina niza
* `date` - datum (`YYYY-MM-DD`)
* `time` - čas (`hh:mm:ss`)
* `datetime` - datum in čas (`YYYY-MM-DD hh:mm:ss`)