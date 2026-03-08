import streamlit as st
import pandas as pd
import time

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Dashboard Chantier Alpha", layout="wide")

# URL CSV de votre Google Sheet
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ26Il3JhjmDpmhM-TaSsA7e7qPxCsg7H4cX1xcUbolrRfDBjOcD7HvCRMpQQKa936DNfwaKyVSYQLX/pub?gid=0&single=true&output=csv"

# 2. CONFIGURATION DU RAFRAÎCHISSEMENT (Toutes les 5 secondes)
# Cette fonction force Streamlit à relancer tout le script automatiquement
if "load_count" not in st.session_state:
    st.session_state.load_count = 0

# Commande magique pour le rafraîchissement auto
st.empty() # Aide à la fluidité
st_autorefresh = st.empty() 

# 3. FONCTION DE CHARGEMENT (SANS CACHE POUR LE LIVE)
def load_data():
    # Le timestamp force Google à ignorer sa propre mise en cache
    query_url = f"{SHEET_CSV_URL}&nocache={time.time()}"
    data = pd.read_csv(query_url)
    if not data.empty:
        data.columns = ['Date', 'Heure', 'Utilisateur', 'Message']
    return data

# --- AFFICHAGE ---
st.title("🏗️ Suivi Chantier Alpha (LIVE)")

try:
    df = load_data()
    
    # Indicateurs
    col1, col2 = st.columns(2)
    col1.metric("Total Messages", len(df))
    
    if not df.empty:
        dernier_log = df.iloc[-1]
        col2.metric("Dernière MAJ", dernier_log['Heure'])
        st.success(f"**Dernier message :** {dernier_log['Message']}")
        
        st.divider()
        
        # Tableau (Plus récent en haut)
        st.subheader("Historique des transmissions")
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("En attente de données...")

except Exception as e:
    st.warning("Synchronisation avec Google Sheets en cours...")

# 4. LE MOTEUR DE RAFRAÎCHISSEMENT (Solution stable)
time.sleep(5)
st.rerun() # Force Streamlit à relancer le code proprement
