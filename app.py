from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def nacti_terapeuty():
    df = pd.read_csv("terapeuti.csv", encoding="utf-8-sig")
    df = df.fillna("")
    return df

@app.route("/")
def index():
    df = nacti_terapeuty()

    # Filtry z URL parametrů
    mesto = request.args.get("mesto", "").strip()
    dostupnost = request.args.get("dostupnost", "").strip()
    forma = request.args.get("forma", "").strip()
    styl = request.args.get("styl", "").strip()

    # Filtrování
    if mesto:
        df = df[df["mesto"].str.contains(mesto, case=False, na=False)]
    if dostupnost:
        df = df[df["dostupnost"].str.contains(dostupnost, case=False, na=False)]
    if forma:
        df = df[df["forma"].str.contains(forma, case=False, na=False)]
    if styl:
        df = df[df["styl_terapie"].str.contains(styl, case=False, na=False)]

    terapeuti = df.to_dict(orient="records")
    celkem = len(terapeuti)

    return render_template("index.html",
        terapeuti=terapeuti[:50],
        celkem=celkem,
        mesto=mesto,
        dostupnost=dostupnost,
        forma=forma,
        styl=styl
    )

if __name__ == "__main__":
    app.run(debug=True)
