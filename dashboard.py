import streamlit as st
import pandas as pd
import time

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Chantier Alpha",
    page_icon="🏗️",
    layout="wide"
)

# --- CONFIGURATION DU LIEN ---
# Votre URL de publication CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

# Titre du Dashboard
st.title("🏗️ Suivi de Chantier en Temps Réel")
st.markdown("Ce dashboard se met à jour automatiquement dès qu'un message est envoyé depuis l'iPhone.")

# Fonction pour charger les données avec bypass du cache Google
def load_data():
    # On ajoute un timestamp à l'URL pour forcer Google à donner les données les plus récentes
    query_url = f"{SHEET_CSV_URL}&cache_buster={time.time()}"
    data = pd.read_csv(query_url)
    
    # Nettoyage : on enlève les lignes où le message est vide
    if not data.empty:
        # On suppose que la colonne 4 (index 3) est le message
        # On renomme les colonnes pour être sûr du rendu
        data.columns = ['Date', 'Heure', 'Utilisateur', 'Message']
        data = data.dropna(subset=['Message'])
    return data

# --- ZONE D'AFFICHAGE DYNAMIQUE ---
placeholder = st.empty()

# Boucle de rafraîchissement automatique
while True:
    try:
        df = load_data()
        
        with placeholder.container():
            # 1. Barre de statistiques (Metrics)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rapports", len(df))
            
            if not df.empty:
                dernier_log = df.iloc[-1]
                col2.metric("Dernier passage", dernier_log['Heure'])
                st.success(f"**Dernier message reçu :** {dernier_log['Message']}")
            else:
                col2.metric("Dernier passage", "--")
                st.info("En attente de données du terrain...")

            st.divider()

            # 2. Tableau principal (Derniers messages en haut)
            st.subheader("📋 Historique des transmissions")
            # On inverse l'ordre pour voir le plus récent en premier
            st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Erreur de connexion au flux Google : {e}")

    # Attendre 5 secondes avant de recommencer la boucle
    time.sleep(5)
