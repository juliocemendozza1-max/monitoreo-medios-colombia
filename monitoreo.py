import feedparser
import pandas as pd
from datetime import datetime, timedelta
import pytz

RSS_FEEDS = {
    "El Tiempo": "https://www.eltiempo.com/rss/justicia.xml",
    "Semana": "https://www.semana.com/rss",
    "Caracol": "https://www.caracol.com.co/rss.aspx"
}

TEMAS = {
    "Víctimas": ["víctima", "reparación"],
    "JEP": ["jep", "justicia especial"],
    "Protesta social": ["protesta", "manifestación"]
}

def clasificar(texto):
    texto = texto.lower()
    encontrados = []
    for tema, palabras in TEMAS.items():
        if any(p in texto for p in palabras):
            encontrados.append(tema)
    return encontrados if encontrados else ["Otros"]

def recolectar():
    noticias = []
    ahora = datetime.now(pytz.UTC)

    for medio, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for e in feed.entries:
            if hasattr(e, "published_parsed"):
                fecha = datetime(*e.published_parsed[:6], tzinfo=pytz.UTC)
                if fecha >= ahora - timedelta(days=1):
                    noticias.append({
                        "medio": medio,
                        "titulo": e.title,
                        "fecha": fecha
                    })
    return pd.DataFrame(noticias)

def main():
    df = recolectar()

    if df.empty:
        print("No hay noticias recientes.")
        return

    df["temas"] = df["titulo"].apply(clasificar)
    df["fecha"] = df["fecha"].dt.tz_localize(None)
    df.to_excel("base_monitoreo.xlsx", index=False)

    print("Monitoreo ejecutado correctamente.")

if __name__ == "__main__":
    main()
