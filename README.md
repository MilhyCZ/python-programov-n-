# Election Scraper – volby do Poslanecké sněmovny 2017

Program stahuje z volby.cz výsledky všech obcí vybraného územního celku.
Každá obec má jeden řádek: kód, název, voliči v seznamu, vydané obálky,
platné hlasy a absolutní počty hlasů všech kandidujících stran.

## Instalace

Vyžaduje Python 3.10 nebo novější. Vytvořte pro projekt samostatný repozitář
a virtuální prostředí. Příkazy spouštějte ve složce projektu.

```console
python -m venv .venv
```

Aktivace ve Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Aktivace v Linuxu nebo macOS:

```sh
source .venv/bin/activate
```

Instalace knihoven:

```console
python -m pip install -r requirements.txt
```

Soubor requirements.txt byl vygenerován příkazem `python -m pip freeze`
v samostatném virtuálním prostředí s knihovnami requests a beautifulsoup4.

## Spuštění

Program vyžaduje dva argumenty v tomto pořadí:

1. Český odkaz na seznam obcí územního celku z voleb 2017 (stránka ps32).
2. Název nového výstupního souboru s příponou .csv.

Příklad pro Benešov:

```console
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```

URL musí být v uvozovkách kvůli znakům `&`. V hlavním přehledu
https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ vyberte odkaz ve sloupci
Výběr obce u požadovaného územního celku a zkopírujte adresu stránky ps32.
Web dnes používá také doménu volby.gov.cz; program přijímá obě domény.
Přímý odkaz na jednu obec (ps311) není vstupem tohoto programu.

Během stahování program vypisuje postup. Po dokončení oznámí počet obcí
a cestu k CSV. CSV používá čárku jako oddělovač a UTF-8 s BOM pro české
znaky. V Excelu lze soubor importovat přes Data → Z textu/CSV.

Přiložený vysledky.csv obsahuje výsledky územního celku Benešov.
Při dalším spuštění použijte nový název; existující soubory se nepřepisují.

## Kontroly a chyby

Chybějící argumenty, nesprávné pořadí, neplatný odkaz či přípona ukončí
program s vysvětlením. Stejně se zpracují síťové chyby, neplatná struktura
stránek nebo nemožnost zápisu. Program kontroluje také shodný seznam stran
a součet jejich hlasů proti počtu platných hlasů. Výstup se zapisuje až
po úspěšném stažení všech obcí. Návratový kód je 0 při úspěchu, jinak 1
(chyba běhu) nebo 2 (chyba argumentů).

## Obsah projektu

- main.py - jediný Python soubor, méně než 200 řádků.
- requirements.txt – vygenerovaný seznam knihoven a verzí.
- README.md – instalace a používání.
- vysledky.csv – skutečně stažený výstup pro Benešov.
