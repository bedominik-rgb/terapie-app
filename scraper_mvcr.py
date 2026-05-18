import requests
import csv

# Google Sheets export jako CSV
sheet_id = "1VAemd9F3hhMVG4q3iIxaVxguwPlyN67l"
gid = "2112430091"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

print("Stahuji data ze ZP MVČR...")
response = requests.get(url)
response.encoding = "utf-8"

radky = response.text.splitlines()
import csv as csvmod
reader = csvmod.reader(radky)

terapeuti = []
hlavicka = next(reader)  # přeskočíme hlavičku
print(f"Sloupce: {hlavicka[:7]}")

for radek in reader:
    if not radek or not radek[0].strip():
        continue
    terapeuti.append({
        "jmeno": radek[0].strip(),
        "adresa": radek[2].strip() if len(radek) > 2 else "",
        "telefon": radek[3].strip() if len(radek) > 3 else "",
        "email": radek[4].strip() if len(radek) > 4 else "",
        "web": radek[5].strip() if len(radek) > 5 else "",
        "zamereni": radek[7].strip() if len(radek) > 7 else "",
        "forma": radek[8].strip() if len(radek) > 8 else "",
        "cilova_skupina": radek[9].strip() if len(radek) > 9 else "",
        "kraj": radek[12].strip() if len(radek) > 12 else "",
        "kapacita": radek[13].strip() if len(radek) > 13 else "",
        "zdroj": "ZP MVČR",
    })

with open("terapeuti_mvcr.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=terapeuti[0].keys())
    writer.writeheader()
    writer.writerows(terapeuti)

print(f"\nHotovo! Celkem {len(terapeuti)} terapeutů")
print("Uloženo do terapeuti_mvcr.csv")