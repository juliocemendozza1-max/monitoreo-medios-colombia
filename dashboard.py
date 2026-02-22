import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitoreo Medios", layout="wide")

st.title("📊 Dashboard Monitoreo de Medios")

df = pd.read_excel("base_monitoreo.xlsx")

if df.empty:
    st.warning("No hay datos disponibles.")
else:
    medio = st.selectbox("Filtrar por medio", ["Todos"] + list(df["medio"].unique()))

    if medio != "Todos":
        df = df[df["medio"] == medio]

    st.dataframe(df)

    st.subheader("Noticias por medio")
    st.bar_chart(df["medio"].value_counts())
