import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_vzp():
    vsichni = []
    
    # Zjistíme počet stránek z první stránky
    url = "https://dusevnizdravi.vzp.cz/seznam-terapeutu/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Najdeme poslední číslo stránky
    strankovani = soup.select("a[href*='stranka=']")
    cisla = []
    for a in strankovani:
        try:
            cislo = int(a.text.strip())
            cisla.append(cislo)
        except:
            pass
    
    max_stranka = max(cisla) if cisla else 1
    print(f"Celkem stranek: {max_stranka}")
    
    for stranka in range(1, max_stranka + 1):
        url = f"https://dusevnizdravi.vzp.cz/seznam-terapeutu/?queryKraj=&queryZamereni=&queryForma=&queryKapacita=&queryText=&stranka={stranka}"
        print(f"Scraping stranky {stranka}/{max_stranka}...")
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        
        radky = soup.select("table tr")[1:]
        
        for radek in radky:
            sloupce = radek.find_all("td")
            if len(sloupce) < 5:
                continue
            
            jmeno_tag = sloupce[0].find("a")
            jmeno = jmeno_tag.text.strip() if jmeno_tag else ""
            adresa = sloupce[0].get_text(separator=" ").replace(jmeno, "").strip()
            web = "https://dusevnizdravi.vzp.cz" + jmeno_tag["href"] if jmeno_tag else ""
            
            vsichni.append({
                "jmeno": jmeno,
                "adresa": adresa,
                "kraj": sloupce[1].text.strip(),
                "zamereni": sloupce[2].text.strip(),
                "forma": sloupce[3].text.strip(),
                "kapacita": sloupce[4].text.strip(),
                "zdroj": "VZP",
                "web": web,
            })
        
        time.sleep(1)
    
    with open("terapeuti_vzp.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=vsichni[0].keys())
        writer.writeheader()
        writer.writerows(vsichni)
    
    print(f"\nHotovo! Celkem {len(vsichni)} terapeutu")
    print("Ulozeno do terapeuti_vzp.csv")

scrape_vzp()