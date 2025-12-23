import streamlit as st
import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Assistant Facturation Nounou",
    page_icon="👶",
    layout="centered"
)

# --- STYLE CSS POUR SIMPLIFIER L'INTERFACE ---
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #FF4B4B;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 3em;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TITRE ---
st.title("👶 Assistant Factures")
st.write("Remplissez les cases ci-dessous pour calculer la semaine.")

# --- FORMULAIRE ---
with st.container():
    st.subheader("1. Informations")
    col1, col2 = st.columns(2)
    with col1:
        parent_name = st.text_input("Nom du Parent", placeholder="Ex: M. Martin")
    with col2:
        child_name = st.text_input("Prénom de l'enfant", placeholder="Ex: Léo")

    st.subheader("2. Les Heures")
    # On utilise des sliders ou des champs numériques simples
    hours = st.number_input("Nombre d'heures travaillées", min_value=0.0, step=0.5, format="%.1f")
    rate = st.number_input("Taux horaire (€/heure)", value=4.0, step=0.5, format="%.2f")

    st.subheader("3. Les Frais Annexes")
    col3, col4 = st.columns(2)
    with col3:
        meals = st.number_input("Repas / Goûters (€)", min_value=0.0, step=1.0)
    with col4:
        maintenance = st.number_input("Indemnités entretien (€)", min_value=0.0, step=0.1)

# --- CALCUL ---
total_salary = hours * rate
total_fees = meals + maintenance
total_to_pay = total_salary + total_fees

# --- AFFICHAGE DES RÉSULTATS ---
st.markdown("---")
if st.button("CALCULER LE TOTAL"):
    st.balloons()
    
    st.markdown(f"<p class='big-font'>Total à payer : {total_to_pay:.2f} €</p>", unsafe_allow_html=True)
    
    # Détails pour vérification
    with st.expander("Voir le détail du calcul"):
        st.write(f"💼 Salaire : {hours}h x {rate}€ = **{total_salary:.2f} €**")
        st.write(f"🍎 Frais (Repas + Entretien) = **{total_fees:.2f} €**")
    
    # --- GÉNÉRATEUR DE MESSAGE WHATSAPP ---
    st.subheader("📲 Message prêt à envoyer")
    st.write("Copiez ce texte et envoyez-le aux parents :")
    
    current_date = datetime.date.today().strftime("%d/%m/%Y")
    
    message_text = f"""Bonjour {parent_name},

Voici le récapitulatif pour la garde de {child_name} (le {current_date}) :

- Heures effectuées : {hours}h
- Salaire : {total_salary:.2f}€
- Frais (repas/entretien) : {total_fees:.2f}€

TOTAL À REGLER : {total_to_pay:.2f} €

Merci et bonne journée !"""

    st.code(message_text, language=None)
    st.info("Astuce : Cliquez sur la petite icône 'copier' en haut à droite du cadre gris ci-dessus.")
