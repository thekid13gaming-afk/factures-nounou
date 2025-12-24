import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Facture Nounou Connectée", page_icon="👶")

# ==============================================================================
# ⚠️ COLLE TON LIEN CI-DESSOUS (Entre les guillemets)
# ==============================================================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZMV9OmQDVfpBrIik74i_CYA-b45b0Wicp4WtVTNjRS_uajR-gIxDsJlBGqAEVmJKaaN_exuSqJfa0/pub?output=csv" 

# --- TITRE & SIDEBAR ---
st.title("👶 Suivi Mensuel Nounou")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Paramètres Facture")
    parent_name = st.text_input("Nom Parent", "Famille Martin")
    child_name = st.text_input("Enfant", "Léo")
    rate = st.number_input("Taux horaire (€)", value=4.0, step=0.1)
    st.markdown("---")
    if st.button("🔄 Actualiser les données"):
        st.rerun()

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data(ttl=60)
def load_data():
    try:
        # On lit le lien CSV du Google Sheet
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception:
        return None

df_raw = load_data()

# --- VÉRIFICATION ---
if df_raw is None:
    st.error("⚠️ Erreur : Je n'arrive pas à lire le tableau.")
    st.info("Vérifie que tu as bien collé le lien 'Publier sur le web' (format CSV) dans le code, à la ligne 'SHEET_URL'.")
    st.stop()

# --- NETTOYAGE (ADAPTÉ À TON IMAGE) ---
try:
    # On sélectionne uniquement les colonnes B, C, D, E (Date, Heures, Repas, Entretien)
    # On ignore la colonne A (Horodateur) et F (Évaluation)
    df = df_raw.iloc[:, 1:5].copy()
    
    # On renomme les colonnes pour que les calculs fonctionnent
    df.columns = ["Date", "Heures", "Repas", "Entretien"]
    
    # Nettoyage des chiffres (remplace les vides par 0)
    df = df.fillna(0)
except Exception as e:
    st.error("Les colonnes de ton tableau ont changé. Vérifie ton Google Sheet.")
    st.write("Voici ce que l'application voit :", df_raw.head())
    st.stop()

# --- AFFICHAGE DU TABLEAU ---
st.subheader("📝 Les jours enregistrés")
st.dataframe(df, use_container_width=True)

# --- CALCULS ---
total_heures = df["Heures"].sum()
salaire_net = total_heures * rate
total_indemnites = df["Repas"].sum() + df["Entretien"].sum()
total_a_payer = salaire_net + total_indemnites

# --- RÉSULTATS ---
st.markdown(f"""
<div style='background-color:#effdf3; padding:20px; border-radius:10px; border:1px solid #c3e6cb;'>
    <h3 style='color:#155724; margin-top:0;'>💰 Total à payer : {total_a_payer:.2f} €</h3>
    <p><b>Détails :</b></p>
    <ul>
        <li>⏱️ Heures totales : <b>{total_heures}h</b> (x {rate}€ = {salaire_net:.2f}€)</li>
        <li>🍎 Indemnités (Repas/Entretien) : <b>{total_indemnites:.2f}€</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- MESSAGE TYPE ---
st.subheader("📲 Message à copier")
message = f"""Bonjour {parent_name},

Voici le récapitulatif du mois pour {child_name} :

📅 Jours travaillés : {len(df)}
⏱️ Total Heures : {total_heures}h
💶 Salaire Net : {salaire_net:.2f}€
🍼 Indemnités : {total_indemnites:.2f}€

TOTAL À REGLER : {total_a_payer:.2f} €

Merci !"""

st.text_area("Texte pour WhatsApp/SMS", message, height=250)
