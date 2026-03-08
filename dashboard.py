import streamlit as st
import pandas as pd

# 1. Configuration
st.set_page_config(page_title="Chantier Alpha", layout="wide")

# URL CSV de votre Google Sheet
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

st.title("🏗️ Suivi Chantier Alpha")

# Bouton de rafraîchissement manuel pour tester
if st.button('Actualiser les données'):
    st.rerun()

# 2. Chargement simple
try:
    # On force pandas à ne pas utiliser de cache interne
    df = pd.read_csv(URL)
    
    if not df.empty:
        st.metric("Messages", len(df))
        st.success(f"Dernière entrée : {df.iloc[-1, -1]}")
        st.divider()
        st.dataframe(df.iloc[::-1], use_container_width=True)
    else:
        st.info("Le tableau est vide.")
except Exception as e:
    st.error(f"Erreur de lecture : {e}")

st.caption("Appuyez sur 'R' au clavier ou sur le bouton pour actualiser.")
