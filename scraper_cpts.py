import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_cpts():
    vsichni = []
    stranka = 0

    while True:
        url = f"https://www.psychoterapeuti.cz/adresar-psychoterapeutu?start={stranka}"
        print(f"Scraping (start={stranka})...")

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        zaznamy = soup.find_all("h2")
        if not zaznamy:
            print("Konec!")
            break

        pocet_pred = len(vsichni)

        for h2 in zaznamy:
            a = h2.find("a")
            if not a or "adresar" not in a.get("href", ""):
                continue

            jmeno = a.text.strip()
            blok = h2.parent
            text = blok.get_text(separator="\n")

            def vytahni(label):
                lines = text.split("\n")
                for i, line in enumerate(lines):
                    if label in line and i + 1 < len(lines):
                        return lines[i + 1].strip()
                return ""

            vsichni.append({
                "jmeno": jmeno,
                "mesto": vytahni("Místo poskytování"),
                "telefon": vytahni("Telefon:"),
                "email": vytahni("E-mail:"),
                "web": "https://www.psychoterapeuti.cz" + a.get("href", ""),
                "cilova_skupina": vytahni("Cílová skupina:"),
                "forma": vytahni("Psychoterapeutické služby:"),
                "styl_terapie": vytahni("Psychoterapeutický směr:"),
                "zdroj": "CPtS",
            })

        print(f"  -> přidáno {len(vsichni) - pocet_pred}, celkem: {len(vsichni)}")

        # Pokud nepřibylo nic nového, končíme
        if len(vsichni) == pocet_pred:
            print("Žádná nová data — konec!")
            break

        stranka += 10
        time.sleep(1)

    if not vsichni:
        print("Žádná data!")
        return

    with open("terapeuti_cpts.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=vsichni[0].keys())
        writer.writeheader()
        writer.writerows(vsichni)

    print(f"\nHotovo! Celkem {len(vsichni)} terapeutů")
    print("Uloženo do terapeuti_cpts.csv")

scrape_cpts()