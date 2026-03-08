import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Dashboard Chantier Alpha", layout="wide")

# --- CONFIGURATION ---
# Collez ici le lien "Publier sur le web" (format CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

st.title("🏗️ Suivi Chantier Alpha - Temps Réel")

# Fonction pour charger les données
def load_data():
    # On ajoute un paramètre bidon à l'URL pour forcer Google à nous donner les données fraîches
    df = pd.read_csv(f"{SHEET_CSV_URL}&cache={time.time()}")
    return df

# Création d'un espace vide pour rafraîchir le contenu
placeholder = st.empty()

while True:
    try:
        df = load_data()
        
        with placeholder.container():
            # 1. Indicateurs clés
            col1, col2, col3 = st.columns(3)
            col1.metric("Messages reçus", len(df))
            col2.metric("Dernière activité", df.iloc[-1, 1] if not df.empty else "--")
            col3.metric("Statut Système", "🟢 Opérationnel")

            st.divider()

            # 2. Le flux d'activité (les derniers messages en haut)
            st.subheader("📝 Journal de bord en direct")
            if not df.empty:
                # On inverse l'ordre pour voir le plus récent en haut
                st.dataframe(df.iloc[::-1], use_container_width=True)
            else:
                st.info("En attente de la première retranscription...")

            # 3. Petit graphique pour faire "pro" (nombre de messages par heure)
            # (Optionnel selon vos colonnes)

    except Exception as e:
        st.error(f"Connexion au flux en cours... {e}")

    # Attendre 5 secondes avant de rafraîchir
    time.sleep(5)board.py
