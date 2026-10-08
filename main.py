"""Stáhne obecní výsledky voleb do Poslanecké sněmovny 2017."""

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def validate_url(value: str) -> str:
    """Ověří odkaz na seznam obcí vybraného územního celku."""
    parsed = urlparse(value)
    query = parse_qs(parsed.query)
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.netloc not in {"volby.cz", "www.volby.cz", "volby.gov.cz"}
        or parsed.path != "/pls/ps2017nss/ps32"
        or any(len(query.get(key, [])) != 1 for key in
               ("xjazyk", "xkraj", "xnumnuts"))
        or query.get("xjazyk") != ["CZ"]
        or not all(query[key][0].isdigit() for key in
                   ("xkraj", "xnumnuts"))
    ):
        raise argparse.ArgumentTypeError(
            "Zadejte český odkaz volby.cz/pls/ps2017nss/ps32 "
            "s parametry xjazyk, xkraj a xnumnuts."
        )
    return parsed._replace(netloc="volby.gov.cz").geturl()


def validate_output(value: str) -> Path:
    """Ověří příponu a umístění výstupního CSV."""
    path = Path(value)
    if path.suffix.lower() != ".csv" or not path.parent.is_dir():
        raise argparse.ArgumentTypeError(
            "Výstup musí mít příponu .csv a existující nadřazenou složku."
        )
    if path.exists():
        raise argparse.ArgumentTypeError(
            "Výstupní soubor již existuje. Vyberte jiný název."
        )
    return path


def arguments() -> argparse.Namespace:
    """Načte právě dva povinné argumenty příkazové řádky."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", type=validate_url, help="URL seznamu obcí")
    parser.add_argument("output", type=validate_output,
                        help="nový soubor .csv")
    return parser.parse_args()


def download(session: requests.Session, url: str) -> BeautifulSoup:
    """Stáhne HTML a ověří stav i případné přesměrování."""
    response = session.get(url, timeout=(10, 30))
    response.raise_for_status()
    if urlparse(response.url).hostname not in {
        "volby.cz", "www.volby.cz", "volby.gov.cz"
    }:
        raise ValueError("Server přesměroval požadavek mimo volby.cz.")
    return BeautifulSoup(response.content, "html.parser")


def municipalities(page: BeautifulSoup, base: str) -> list[tuple]:
    """Vrátí kód, název a odkaz všech obcí bez duplicit."""
    result = {}
    for row in page.select("tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        link = cells[0].find("a", href=True)
        if link is None:
            continue
        code = link.get_text(strip=True)
        url = urljoin(base, link["href"])
        if code.isdigit() and urlparse(url).path.endswith("/ps311"):
            result[code] = (code, cells[1].get_text(strip=True), url)
    if not result:
        raise ValueError("Na odkazu nebyl nalezen seznam výsledků obcí.")
    return list(result.values())


def number(text: str) -> int:
    """Převede celé číslo včetně nezalomitelných mezer."""
    cleaned = "".join(text.split())
    if not cleaned.isdigit():
        raise ValueError(f"Neplatná číselná hodnota: {text!r}")
    return int(cleaned)


def results(page: BeautifulSoup) -> tuple[list[int], dict[str, int]]:
    """Vybere souhrn účasti a absolutní hlasy všech stran."""
    totals = []
    for header in ("sa2", "sa3", "sa6"):
        cell = page.find("td", headers=header)
        if cell is None:
            raise ValueError("Chybí tabulka účasti ve výsledcích obce.")
        totals.append(number(cell.get_text()))
    parties = {}
    for row in page.select("tr"):
        cells = row.find_all("td")
        name = next((c for c in cells if any(
            re.fullmatch(r"t\d+sb2", h) for h in c.get("headers", [])
        )), None)
        if name is None:
            continue
        prefix = next(h[:-3] for h in name["headers"]
                      if h.endswith("sb2"))
        code = row.select_one(f'td[headers~="{prefix}sb1"]')
        if code is None or not code.get_text(strip=True).isdigit():
            continue
        votes = row.select_one(f'td[headers~="{prefix}sb3"]')
        if votes is None:
            raise ValueError("U strany chybí počet hlasů.")
        label = name.get_text(" ", strip=True)
        if label in parties:
            raise ValueError("Duplicitní název strany v tabulce.")
        parties[label] = number(votes.get_text())
    if not parties or sum(parties.values()) != totals[2]:
        raise ValueError("Součet hlasů stran neodpovídá platným hlasům.")
    return totals, parties


def scrape(url: str) -> tuple[list[str], list[list]]:
    """Stáhne všechny obce a sestaví jednotnou tabulku CSV."""
    rows = []
    names = []
    with requests.Session() as session:
        session.headers["User-Agent"] = "ElectionScraper2017/1.0"
        places = municipalities(download(session, url), url)
        for index, (code, name, detail_url) in enumerate(places, 1):
            print(f"[{index}/{len(places)}] {name}")
            totals, parties = results(download(session, detail_url))
            if not names:
                names = list(parties)
            if set(names) != set(parties):
                raise ValueError(f"Nesouhlasí seznam stran v obci {name}.")
            rows.append([code, name, *totals, *[parties[n] for n in names]])
    header = ["kod_obce", "nazev_obce", "volici_v_seznamu",
              "vydane_obalky", "platne_hlasy", *names]
    return header, rows


def save(path: Path, header: list[str], rows: list[list]) -> Path:
    """Zapíše nový CSV soubor v UTF-8, existující nepřepisuje."""
    with path.open("x", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(header)
        writer.writerows(rows)
    return path


def main() -> int:
    """Spustí scraper a při chybě vrátí nenulový návratový kód."""
    args = arguments()
    try:
        header, rows = scrape(args.url)
        path = save(args.output, header, rows)
    except (requests.RequestException, ValueError, OSError) as error:
        print(f"Chyba: {error}", file=sys.stderr)
        return 1
    print(f"Uloženo {len(rows)} obcí do {path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
