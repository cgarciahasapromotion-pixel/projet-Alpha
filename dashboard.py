import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time

# 1. CONFIGURATION
st.set_page_config(page_title="LIVE Chantier Alpha", layout="wide")

# URL CSV de votre Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

# 2. SYSTÈME DE RAFRAÎCHISSEMENT AUTO (Toutes les 10 secondes pour éviter de bloquer Google)
# On utilise un intervalle un peu plus long pour laisser Google respirer
from streamlit_autorefresh import st_autorefresh
count = st_autorefresh(interval=10000, limit=None, key="fec_counter")

# 3. FONCTION DE LECTURE ROBUSTE
def get_data_from_google():
    try:
        # On force Google à ne pas utiliser son cache avec un paramètre aléatoire
        headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
        response = requests.get(f"{SHEET_URL}&t={int(time.time())}", headers=headers)
        
        if response.status_code == 200:
            # On transforme le texte reçu en DataFrame
            data = pd.read_csv(StringIO(response.text))
            
            # Nettoyage et nommage des colonnes
            if not data.empty:
                # On s'assure d'avoir 4 colonnes, même si le Sheet est bizarre
                data.columns = ['Date', 'Heure', 'Utilisateur', 'Message'][:len(data.columns)]
                return data.dropna(subset=[data.columns[-1]]) # On garde si le message n'est pas vide
        return pd.DataFrame()
    except Exception as e:
        return None

# --- AFFICHAGE ---
st.title("🏗️ Dashboard Live - Projet Alpha")

df = get_data_from_google()

if df is not None:
    if not df.empty:
        # Métriques
        c1, c2 = st.columns(2)
        c1.metric("Total Rapports", len(df))
        c2.metric("Statut", "📡 Connecté", delta="Live")

        # Dernier message en évidence
        dernier = df.iloc[-1]
        st.info(f"🎤 **Dernière dictée ({dernier['Heure']}) :** {dernier['Message']}")

        st.divider()

        # Tableau (Plus récent en haut)
        st.subheader("Historique des transmissions")
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.warning("Le tableau Google Sheet est vide ou mal formaté.")
else:
    st.error("Impossible de joindre Google Sheets. Nouvelle tentative dans 10s...")

st.caption(f"Dernière actualisation du dashboard : {time.strftime('%H:%M:%S')}")
