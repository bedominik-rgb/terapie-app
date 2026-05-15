from playwright.sync_api import sync_playwright
import csv
import time

JS_SCRAPE = (
    "() => {"
    "  const vysledky = [];"
    "  const radky = document.querySelectorAll('td.memberDirectoryColumn1');"
    "  radky.forEach(td => {"
    "    const jmeno = td.querySelector('.memberValue');"
    "    if (!jmeno || !jmeno.innerText.trim()) return;"
    "    const radek = td.parentElement;"
    "    const col2 = radek.querySelector('.memberDirectoryColumn2');"
    "    const col3 = radek.querySelector('.memberDirectoryColumn3');"
    "    const nextRadek = radek.nextElementSibling;"
    "    const bottom = nextRadek ? nextRadek.querySelector('.memberDirectoryBottomRow .memberValue') : null;"
    "    const h2 = col2 ? col2.querySelectorAll('.memberValue') : [];"
    "    const h3 = col3 ? col3.querySelectorAll('.memberValue') : [];"
    "    vysledky.push({"
    "      jmeno: jmeno.innerText.trim(),"
    "      mesto: h2[0] ? h2[0].innerText.trim() : '',"
    "      web: h2[1] ? h2[1].innerText.trim() : '',"
    "      dostupnost: h3[0] ? h3[0].innerText.trim() : '',"
    "      cilova_skupina: h3[1] ? h3[1].innerText.trim() : '',"
    "      forma: h3[2] ? h3[2].innerText.trim() : '',"
    "      styl_terapie: bottom ? bottom.innerText.trim() : '',"
    "    });"
    "  });"
    "  return vysledky;"
    "}"
)

JS_MOZNOSTI = (
    "() => {"
    "  const sel = document.querySelector('#idPagingData select');"
    "  if (!sel) return [];"
    "  return Array.from(sel.options).map(o => o.value || o.text);"
    "}"
)

def scrape_stranku(page):
    return page.evaluate(JS_SCRAPE)

def scrape_czap():
    vsichni = []

    with sync_playwright() as p:
        print("Spoustim prohlizec...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.czap.cz/adresar")
        print("Cekam na nacteni...")
        time.sleep(8)

        moznosti = page.evaluate(JS_MOZNOSTI)
        print(f"Nalezeno stranek: {len(moznosti)}")

        for i, moznost in enumerate(moznosti):
            print(f"Scraping stranky {i+1}/{len(moznosti)} ({moznost})...")

            js_klik = (
                "() => {"
                "  const sel = document.querySelector('#idPagingData select');"
                "  sel.value = '" + moznost + "';"
                "  sel.dispatchEvent(new Event('change', {bubbles: true}));"
                "}"
            )
            page.evaluate(js_klik)
            time.sleep(5)

            data = scrape_stranku(page)
            if not data:
                print("  Zadna data, preskakuji...")
                continue
            vsichni.extend(data)
            print(f"  -> {len(data)} terapeutu, celkem: {len(vsichni)}")

        browser.close()

    if not vsichni:
        print("Zadna data!")
        return

    with open("terapeuti.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=vsichni[0].keys())
        writer.writeheader()
        writer.writerows(vsichni)

    print(f"\nHotovo! Celkem {len(vsichni)} terapeutu")
    print("Ulozeno do terapeuti.csv")

scrape_czap()
