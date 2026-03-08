import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Configuration
st.set_page_config(page_title="Chantier Alpha LIVE", layout="wide")

# URL CSV Directe (sans fioritures pour éviter le 400 Bad Request)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

# Rafraîchissement automatique toutes les 10 secondes
st_autorefresh(interval=10000, key="datarefresh")

st.title("🏗️ Suivi Chantier Alpha - Temps Réel")

def load_data():
    # On lit directement l'URL. Pandas gère très bien la mise à jour sur les URL publiées.
    return pd.read_csv(SHEET_URL)

try:
    df = load_data()
    
    if not df.empty:
        # On renomme les colonnes selon votre structure réelle
        # Colonne 0: Date, 1: Heure, 2: Utilisateur, 3: Message
        df.columns = ['Date', 'Heure', 'Utilisateur', 'Message']
        
        # Stats en haut
        c1, c2, c3 = st.columns(3)
        c1.metric("Messages reçus", len(df))
        c2.metric("Dernière activité", df.iloc[-1]['Heure'])
        c3.metric("Statut", "🟢 Opérationnel")

        # Affichage du dernier message de façon très visible
        dernier_msg = df.iloc[-1]['Message']
        st.info(f"🎤 **Dernière transmission :** {dernier_msg}")

        st.divider()

        # Journal de bord (Inversé pour voir le plus récent en haut)
        st.subheader("📝 Journal de bord en direct")
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("En attente de données...")

except Exception as e:
    st.error(f"Connexion au flux en cours... Veuillez patienter.")
    # Optionnel pour le debug : st.write(e)
