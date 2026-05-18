import pandas as pd

# Načteme všechny databáze
czap = pd.read_csv("terapeuti.csv", encoding="utf-8-sig")
vzp = pd.read_csv("terapeuti_vzp.csv", encoding="utf-8-sig")
mvcr = pd.read_csv("terapeuti_mvcr.csv", encoding="utf-8-sig")

# CZAP
czap["zdroj"] = "CZAP"
czap["kapacita"] = czap["dostupnost"]
czap["kraj"] = ""
czap["adresa"] = ""
czap["zamereni"] = czap["cilova_skupina"]
czap["email"] = ""
czap["telefon"] = ""

# VZP
vzp["mesto"] = vzp["adresa"]
vzp["dostupnost"] = vzp["kapacita"]
vzp["cilova_skupina"] = vzp["zamereni"]
vzp["styl_terapie"] = ""
vzp["email"] = ""
vzp["telefon"] = ""

# MVČR - upravíme sloupce
mvcr["mesto"] = mvcr["adresa"]
mvcr["dostupnost"] = mvcr["kapacita"]
mvcr["cilova_skupina"] = mvcr["cilova_skupina"]
mvcr["styl_terapie"] = mvcr["zamereni"]
mvcr["forma"] = mvcr["forma"]

# Společné sloupce
sloupce = ["jmeno", "mesto", "web", "email", "telefon", "dostupnost", 
           "cilova_skupina", "forma", "styl_terapie", "zdroj", "kraj"]

czap_final = czap.reindex(columns=sloupce, fill_value="")
vzp_final = vzp.reindex(columns=sloupce, fill_value="")
mvcr_final = mvcr.reindex(columns=sloupce, fill_value="")

# Spojíme
vsechni = pd.concat([czap_final, vzp_final, mvcr_final], ignore_index=True)

vsechni.to_csv("terapeuti_vse.csv", index=False, encoding="utf-8-sig")
print(f"Hotovo! Celkem {len(vsechni)} terapeutů")
print("Uloženo do terapeuti_vse.csv")