import pandas as pd

czap = pd.read_csv("terapeuti.csv", encoding="utf-8-sig")
vzp = pd.read_csv("terapeuti_vzp.csv", encoding="utf-8-sig")
mvcr = pd.read_csv("terapeuti_mvcr.csv", encoding="utf-8-sig")
cpts = pd.read_csv("terapeuti_cpts.csv", encoding="utf-8-sig")
cskbt = pd.read_csv("terapeuti_cskbt.csv", encoding="utf-8-sig")

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

# MVČR
mvcr["mesto"] = mvcr["adresa"]
mvcr["dostupnost"] = mvcr["kapacita"]
mvcr["styl_terapie"] = mvcr["zamereni"]

# ČPtS
cpts["dostupnost"] = ""
cpts["kraj"] = ""

# ČSKBT - již má správné sloupce

sloupce = ["jmeno", "mesto", "web", "email", "telefon", "dostupnost",
           "cilova_skupina", "forma", "styl_terapie", "zdroj", "kraj"]

vsechni = pd.concat([
    czap.reindex(columns=sloupce, fill_value=""),
    vzp.reindex(columns=sloupce, fill_value=""),
    mvcr.reindex(columns=sloupce, fill_value=""),
    cpts.reindex(columns=sloupce, fill_value=""),
    cskbt.reindex(columns=sloupce, fill_value=""),
], ignore_index=True)

vsechni.to_csv("terapeuti_vse.csv", index=False, encoding="utf-8-sig")
print(f"Hotovo! Celkem {len(vsechni)} terapeutů")