import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_cskbt():
    vsichni = []

    url = "https://cskbt.cz/adresar-terapeutu/"
    print("Stahuji data z cskbt.cz...")

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    bloky = soup.find_all("div", class_="profile-card")

    print(f"Nalezeno karet: {len(bloky)}")

    for blok in bloky:
        text = blok.get_text(separator="\n")
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        def najdi(label):
            for i, line in enumerate(lines):
                if line.startswith(label):
                    val = line.replace(label, "").strip()
                    return val if val else (lines[i + 1] if i + 1 < len(lines) else "")
            return ""

        jmeno_tag = blok.find("p", class_="profile-name")
        jmeno = jmeno_tag.text.strip() if jmeno_tag else ""
        jmeno = re.sub(r'\(.*?\)', '', jmeno).strip()

        if not jmeno:
            continue

        email_tag = blok.find("a", href=lambda h: h and "mailto:" in h)
        email = email_tag.text.strip() if email_tag else ""

        tel_tag = blok.find("a", href=lambda h: h and "tel:" in h)
        telefon = tel_tag.text.strip() if tel_tag else ""

        web_tag = blok.find("a", href=lambda h: h and h.startswith("http") and "cskbt" not in h and "mailto" not in h and "tel:" not in h)
        web = web_tag["href"] if web_tag else ""

        dostupnost = ""
        if "Přijímám nové pacienty" in text:
            dostupnost = "Přijímám nové pacienty"
        elif "Nepřijímám nové pacienty" in text:
            dostupnost = "Nepřijímám nové pacienty"

        vsichni.append({
            "jmeno": jmeno,
            "mesto": najdi("Město:"),
            "kraj": najdi("Kraj:"),
            "email": email,
            "telefon": telefon,
            "web": web,
            "styl_terapie": najdi("Terapeutické zaměření:"),
            "cilova_skupina": najdi("Specializace:"),
            "forma": "Online" if "Pracuji online" in text else "Osobně",
            "dostupnost": dostupnost,
            "zdroj": "ČSKBT",
        })

    if not vsichni:
        print("Žádná data!")
        return

    with open("terapeuti_cskbt.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=vsichni[0].keys())
        writer.writeheader()
        writer.writerows(vsichni)

    print(f"\nHotovo! Celkem {len(vsichni)} terapeutů KBT")
    print("Uloženo do terapeuti_cskbt.csv")

scrape_cskbt()