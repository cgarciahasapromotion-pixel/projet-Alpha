import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Configuration de base
st.set_page_config(page_title="Chantier Alpha", layout="wide")

# 2. Rafraîchissement automatique (10 secondes)
st_autorefresh(interval=10000, key="datarefresh")

# URL CSV de votre Google Sheet
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

st.title("🏗️ Suivi Chantier Alpha")

# 3. Fonction de chargement avec gestion d'erreur simplifiée
def load_data():
    try:
        # On lit le CSV sans forcer les noms de colonnes au début pour éviter le crash
        df = pd.read_csv(URL)
        return df
    except:
        return None

df = load_data()

# 4. Affichage intelligent
if df is not None:
    if not df.empty:
        # On affiche un petit résumé en haut
        st.metric("Nombre de messages", len(df))
        
        # On affiche le dernier message de la dernière colonne (peu importe son nom)
        dernier_message = df.iloc[-1, -1] 
        st.success(f"**Dernière transmission :** {dernier_message}")
        
        st.divider()
        
        # On affiche le tableau complet (inversé)
        st.subheader("Historique")
        st.dataframe(df.iloc[::-1], use_container_width=True)
    else:
        st.info("Le fichier est vide. Parlez dans l'iPhone pour le remplir !")
else:
    st.error("Connexion à Google Sheets interrompue. Je réessaie dans 10s...")

st.caption(f"Dernière mise à jour : {pd.Timestamp.now().strftime('%H:%M:%S')}")
