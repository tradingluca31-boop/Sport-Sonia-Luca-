import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Configuration
st.set_page_config(
    page_title="FitCouple - Luca & Sonia",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main-header {
        font-size: 2rem; font-weight: 700; text-align: center; padding: 1.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 16px; margin-bottom: 1.5rem;
    }
    .profile-card {
        background: #f5f7fa; padding: 1.2rem; border-radius: 12px;
        margin-bottom: 1rem; border-left: 4px solid #667eea;
    }
    .abdos-circuit {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white; padding: 1rem; border-radius: 12px; margin: 1rem 0;
    }
    .day-card {
        padding: 0.8rem; border-radius: 10px; text-align: center;
        margin: 0.2rem; min-height: 100px;
    }
    .day-today { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .day-normal { background: #f0f0f0; color: #333; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE (PERSISTANCE) ====================
if 'weight_data' not in st.session_state:
    st.session_state.weight_data = {'Luca': [], 'Sonia': []}
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = {'Luca': [], 'Sonia': []}

# ==================== VIDEOS EXERCICES ====================
VIDEOS = {
    "Crunch classique": "https://youtube.com/watch?v=Xyd_fa5zoEU",
    "Obliques crunch": "https://youtube.com/watch?v=pDTHSnoGoEc",
    "Russian twist": "https://youtube.com/watch?v=wkD8rjkodUI",
    "Scissor kicks": "https://youtube.com/watch?v=WoNCIBVLbgY",
    "Portefeuille (V-ups)": "https://youtube.com/watch?v=iP2fjvG0g3w",
    "Gainage (Planche)": "https://youtube.com/watch?v=ASdvN_XEl_c",
    "Gainage latéral": "https://youtube.com/watch?v=K2VljzCC16g",
    "Bicycle crunch": "https://youtube.com/watch?v=9FGilxCbdz8",
    "Mountain climbers": "https://youtube.com/watch?v=nmwgirgXLYM",
    "Pompes": "https://youtube.com/watch?v=IODxDxX7oi4",
    "Pompes serrées": "https://youtube.com/watch?v=J0DnG1_S92I",
    "Pompes inclinées": "https://youtube.com/watch?v=4dF1DOWzf20",
    "Pike push-ups": "https://youtube.com/watch?v=sposDXWEB0A",
    "Dips chaise": "https://youtube.com/watch?v=0326dy_-CzM",
    "Curl biceps": "https://youtube.com/watch?v=ykJmrZ5v0Oo",
    "Curl marteau": "https://youtube.com/watch?v=zC3nLlEvin4",
    "Extension triceps": "https://youtube.com/watch?v=_gsUck-7M74",
    "Rowing haltère": "https://youtube.com/watch?v=roCP6wCXPqo",
    "Élévations latérales": "https://youtube.com/watch?v=3VcKaXpzqRo",
    "Développé haltères": "https://youtube.com/watch?v=qEwKCR5JCog",
    "Superman": "https://youtube.com/watch?v=z6PJMT2y8GQ",
    "Oiseau": "https://youtube.com/watch?v=EA7u4Q_8HQ0",
    "Squats": "https://youtube.com/watch?v=ultWZbUMPL8",
    "Squats sumo": "https://youtube.com/watch?v=9ZuXKqRbT9k",
    "Fentes": "https://youtube.com/watch?v=QOVaHwm-Q6U",
    "Hip thrust": "https://youtube.com/watch?v=SEdqd1n0cvg",
    "Glute bridge": "https://youtube.com/watch?v=OUgsJ8-Vi0E",
    "Donkey kicks": "https://youtube.com/watch?v=SJ1Xuz9D-ZQ",
    "Fire hydrants": "https://youtube.com/watch?v=La3xrTxLXSE",
    "Jumping jacks": "https://youtube.com/watch?v=c4DAnQ6DtF8",
    "Burpees": "https://youtube.com/watch?v=TU8QYVW0gDU",
    "High knees": "https://youtube.com/watch?v=D0bLJnSBNI8",
    "Squat jumps": "https://youtube.com/watch?v=A-cFYWvaHr0",
}

# ==================== CIRCUIT ABDOS LUCA ====================
CIRCUIT_ABDOS = [
    {"nom": "Gainage (Planche)", "reps": "45 sec"},
    {"nom": "Gainage latéral", "reps": "30 sec/côté"},
    {"nom": "Obliques crunch", "reps": "20/côté"},
    {"nom": "Russian twist", "reps": "20 total"},
    {"nom": "Scissor kicks", "reps": "20"},
    {"nom": "Portefeuille (V-ups)", "reps": "15"},
    {"nom": "Crunch classique", "reps": "20"},
    {"nom": "Bicycle crunch", "reps": "20 total"},
]

# ==================== PROGRAMMES ====================
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

PROGRAM_LUCA = {
    0: {"nom": "PUSH (Pecs/Épaules/Triceps)", "type": "Musculation", "duree": 50, "abdos": True,
        "exercices": [
            {"nom": "Pompes", "sets": "4x12-15", "muscle": "Pectoraux"},
            {"nom": "Pompes inclinées", "sets": "3x12", "muscle": "Haut pecs"},
            {"nom": "Pike push-ups", "sets": "3x10", "muscle": "Épaules"},
            {"nom": "Développé haltères", "sets": "3x12", "muscle": "Épaules"},
            {"nom": "Élévations latérales", "sets": "3x15", "muscle": "Épaules"},
            {"nom": "Pompes serrées", "sets": "3x12", "muscle": "Triceps"},
            {"nom": "Dips chaise", "sets": "3x12", "muscle": "Triceps"},
            {"nom": "Extension triceps", "sets": "3x12", "muscle": "Triceps"},
        ]},
    1: {"nom": "PULL (Dos/Biceps)", "type": "Musculation", "duree": 45, "abdos": False,
        "exercices": [
            {"nom": "Rowing haltère", "sets": "4x10-12/bras", "muscle": "Dos"},
            {"nom": "Superman", "sets": "3x15", "muscle": "Lombaires"},
            {"nom": "Oiseau", "sets": "3x15", "muscle": "Arrière épaule"},
            {"nom": "Curl biceps", "sets": "4x12", "muscle": "Biceps"},
            {"nom": "Curl marteau", "sets": "3x12", "muscle": "Biceps"},
        ]},
    2: {"nom": "LEGS + HIIT", "type": "Jambes/Cardio", "duree": 55, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x15", "muscle": "Quadriceps"},
            {"nom": "Squats sumo", "sets": "3x15", "muscle": "Adducteurs"},
            {"nom": "Fentes", "sets": "3x12/jambe", "muscle": "Fessiers"},
            {"nom": "--- HIIT 15min ---", "sets": "", "muscle": ""},
            {"nom": "Jumping jacks", "sets": "3x45sec", "muscle": "Cardio"},
            {"nom": "High knees", "sets": "3x45sec", "muscle": "Cardio"},
            {"nom": "Burpees", "sets": "3x10", "muscle": "Full body"},
        ]},
    3: {"nom": "REPOS ACTIF", "type": "Récupération", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Marche ou vélo léger", "sets": "20-30min", "muscle": "Cardio"},
            {"nom": "Étirements", "sets": "10min", "muscle": "Mobilité"},
        ]},
    4: {"nom": "FULL BODY", "type": "Musculation", "duree": 55, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x12", "muscle": "Jambes"},
            {"nom": "Pompes", "sets": "4x15", "muscle": "Pectoraux"},
            {"nom": "Rowing haltère", "sets": "4x12/bras", "muscle": "Dos"},
            {"nom": "Fentes", "sets": "3x10/jambe", "muscle": "Jambes"},
            {"nom": "Développé haltères", "sets": "3x12", "muscle": "Épaules"},
            {"nom": "Curl biceps", "sets": "3x12", "muscle": "Biceps"},
            {"nom": "Dips chaise", "sets": "3x12", "muscle": "Triceps"},
        ]},
    5: {"nom": "CARDIO", "type": "Cardio", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Vélo ou course", "sets": "30-40min", "muscle": "Cardio"},
            {"nom": "Le cardio brûle les graisses !", "sets": "", "muscle": ""},
        ]},
    6: {"nom": "REPOS COMPLET", "type": "Repos", "duree": 0, "abdos": False,
        "exercices": [
            {"nom": "Récupération totale", "sets": "-", "muscle": "-"},
        ]},
}

PROGRAM_SONIA = {
    0: {"nom": "BAS DU CORPS - Fessiers", "type": "Renforcement", "duree": 45, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x15", "muscle": "Quadriceps"},
            {"nom": "Hip thrust", "sets": "4x15", "muscle": "Fessiers"},
            {"nom": "Fentes", "sets": "3x12/jambe", "muscle": "Fessiers"},
            {"nom": "Glute bridge", "sets": "3x20", "muscle": "Fessiers"},
            {"nom": "Donkey kicks", "sets": "3x20/côté", "muscle": "Fessiers"},
            {"nom": "Fire hydrants", "sets": "3x20/côté", "muscle": "Fessiers"},
        ]},
    1: {"nom": "HIIT BRÛLE-GRAISSE", "type": "Cardio HIIT", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Jumping jacks", "sets": "4x30sec", "muscle": "Cardio"},
            {"nom": "Squat jumps", "sets": "4x30sec", "muscle": "Jambes"},
            {"nom": "Mountain climbers", "sets": "4x30sec", "muscle": "Core"},
            {"nom": "Burpees", "sets": "4x30sec", "muscle": "Full body"},
            {"nom": "High knees", "sets": "4x30sec", "muscle": "Cardio"},
        ]},
    2: {"nom": "HAUT DU CORPS + CORE", "type": "Renforcement", "duree": 40, "abdos": True,
        "exercices": [
            {"nom": "Pompes (genoux ok)", "sets": "3x12", "muscle": "Pectoraux"},
            {"nom": "Rowing haltère", "sets": "3x12/bras", "muscle": "Dos"},
            {"nom": "Élévations latérales", "sets": "3x15", "muscle": "Épaules"},
            {"nom": "Curl biceps", "sets": "3x15", "muscle": "Biceps"},
            {"nom": "Extension triceps", "sets": "3x15", "muscle": "Triceps"},
            {"nom": "Gainage (Planche)", "sets": "3x30sec", "muscle": "Core"},
        ]},
    3: {"nom": "CARDIO MODÉRÉ", "type": "Cardio", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Marche rapide ou vélo", "sets": "35min", "muscle": "Cardio"},
            {"nom": "Étirements", "sets": "10min", "muscle": "Récupération"},
        ]},
    4: {"nom": "CIRCUIT FULL BODY", "type": "Circuit", "duree": 40, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "3x15", "muscle": "Jambes"},
            {"nom": "Pompes (genoux ok)", "sets": "3x10", "muscle": "Pectoraux"},
            {"nom": "Fentes", "sets": "3x10/jambe", "muscle": "Jambes"},
            {"nom": "Rowing haltère", "sets": "3x10/bras", "muscle": "Dos"},
            {"nom": "Glute bridge", "sets": "3x15", "muscle": "Fessiers"},
            {"nom": "Gainage (Planche)", "sets": "3x30sec", "muscle": "Core"},
        ]},
    5: {"nom": "FESSIERS INTENSIF", "type": "Renforcement", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Hip thrust", "sets": "4x20", "muscle": "Fessiers"},
            {"nom": "Squats sumo", "sets": "4x15", "muscle": "Fessiers"},
            {"nom": "Donkey kicks", "sets": "4x20/côté", "muscle": "Fessiers"},
            {"nom": "Fire hydrants", "sets": "4x20/côté", "muscle": "Fessiers"},
            {"nom": "Glute bridge", "sets": "50 reps", "muscle": "Fessiers"},
        ]},
    6: {"nom": "REPOS / YOGA", "type": "Récupération", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Yoga ou étirements", "sets": "20-30min", "muscle": "Mobilité"},
        ]},
}

# ==================== FONCTIONS ====================
def get_today_index():
    return date.today().weekday()

def render_calendar(program):
    today_idx = get_today_index()
    cols = st.columns(7)
    
    for i, jour in enumerate(JOURS):
        with cols[i]:
            is_today = (i == today_idx)
            p = program.get(i, {})
            
            css_class = "day-today" if is_today else "day-normal"
            today_marker = "👉 " if is_today else ""
            abdos_marker = "🔥" if p.get('abdos') else ""
            
            st.markdown(f"""
            <div class="day-card {css_class}">
                <b>{today_marker}{jour}</b><br>
                <small>{p.get('nom', 'Repos')[:18]}</small><br>
                <small>{p.get('duree', 0)}min {abdos_marker}</small>
            </div>
            """, unsafe_allow_html=True)
    
    return today_idx

def render_workout(program, day_idx, user):
    workout = program.get(day_idx, {})
    
    st.markdown(f"## 🎯 {workout.get('nom', 'Repos')}")
    
    if workout.get('type') == 'Repos':
        st.success("💤 Jour de repos - Récupération !")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Type", workout.get('type', '-'))
    col2.metric("Durée", f"{workout.get('duree', 0)} min")
    col3.metric("Abdos", "✅ OUI" if workout.get('abdos') else "❌ Non")
    
    st.markdown("---")
    st.markdown("### 📝 Exercices")
    
    for ex in workout.get('exercices', []):
        if ex['nom'].startswith('---'):
            st.markdown(f"**{ex['nom']}**")
            continue
        
        with st.expander(f"▶️ {ex['nom']} | {ex['sets']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Muscle:** {ex.get('muscle', '-')}")
                st.write(f"**Séries/Reps:** {ex['sets']}")
            with col2:
                video = VIDEOS.get(ex['nom'])
                if video:
                    st.markdown(f"[🎬 Vidéo]({video})")
    
    # Circuit abdos si applicable
    if workout.get('abdos'):
        st.markdown("---")
        st.markdown("""<div class="abdos-circuit">
            <h4>🔥 CIRCUIT ABDOS (2 tours - 30s repos entre tours)</h4>
        </div>""", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, ex in enumerate(CIRCUIT_ABDOS):
            with cols[i % 2]:
                video = VIDEOS.get(ex['nom'], '')
                link = f" [🎬]({video})" if video else ""
                st.markdown(f"• **{ex['nom']}** - {ex['reps']}{link}")
    
    st.markdown("---")
    
    # Enregistrement
    feeling = st.slider("Comment était la séance ?", 1, 5, 3)
    if st.button("✅ Séance terminée !", type="primary", use_container_width=True):
        st.session_state.workout_data[user].append({
            'date': date.today().isoformat(),
            'workout': workout.get('nom'),
            'feeling': feeling
        })
        st.success("🎉 Bravo ! Séance enregistrée !")
        st.balloons()

def render_measurements(user, default_weight):
    st.markdown("### 📏 Enregistrer mes mensurations")
    
    with st.form(f"form_{user}"):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Poids (kg)", 30.0, 200.0, float(default_weight), 0.1)
            belly = st.number_input("Tour ventre (cm)", 50.0, 150.0, 90.0, 0.5)
        with col2:
            arms = st.number_input("Tour bras (cm)", 20.0, 60.0, 35.0, 0.5)
            thighs = st.number_input("Tour cuisses (cm)", 30.0, 100.0, 55.0, 0.5)
        
        if st.form_submit_button("✅ Enregistrer", use_container_width=True):
            st.session_state.weight_data[user].append({
                'date': date.today().isoformat(),
                'weight': weight,
                'belly': belly,
                'arms': arms,
                'thighs': thighs
            })
            st.success("Mensurations enregistrées !")
            st.rerun()

def render_progress(user, target, start, is_loss):
    st.markdown("### 📈 Progression")
    
    data = st.session_state.weight_data[user]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Départ", f"{start} kg")
    col2.metric("Objectif", f"{target} kg")
    
    if data:
        current = data[-1]['weight']
        diff = current - start
        col3.metric("Actuel", f"{current} kg", f"{diff:+.1f} kg")
        
        # Graphique
        df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['weight'], mode='lines+markers', name='Poids'))
        fig.add_hline(y=target, line_dash="dash", line_color="green", annotation_text=f"Objectif: {target}kg")
        fig.update_layout(title="Évolution du poids", height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        col3.metric("Actuel", "- kg")
        st.info("Enregistrez vos mensurations pour voir votre progression !")

def render_nutrition():
    tab = st.radio("", ["📖 Recettes", "🧮 Calories", "🍽️ Plans"], horizontal=True)
    
    if tab == "📖 Recettes":
        recettes = [
            {"nom": "Porridge Protéiné", "cat": "Petit-déj", "kcal": 380, "prot": 28},
            {"nom": "Bowl Poulet Quinoa", "cat": "Déjeuner", "kcal": 520, "prot": 45},
            {"nom": "Saumon Légumes", "cat": "Dîner", "kcal": 420, "prot": 38},
            {"nom": "Shake Protéiné", "cat": "Collation", "kcal": 250, "prot": 35},
            {"nom": "Salade Protéinée", "cat": "Déjeuner", "kcal": 380, "prot": 32},
            {"nom": "Omelette Légumes", "cat": "Petit-déj", "kcal": 320, "prot": 25},
        ]
        
        portions = st.number_input("Portions", 1, 10, 2)
        
        for r in recettes:
            st.markdown(f"**{r['nom']}** ({r['cat']}) - {r['kcal']*portions} kcal - {r['prot']*portions}g prot")
    
    elif tab == "🧮 Calories":
        user = st.selectbox("Profil", ["Luca", "Sonia"])
        if user == "Luca":
            st.metric("Calories/jour", "~2500 kcal")
            st.metric("Protéines", "176g (2g/kg)")
        else:
            st.metric("Calories/jour", "~1400 kcal")
            st.metric("Protéines", "125g (1.6g/kg)")
    
    else:
        user = st.selectbox("Profil", ["Luca", "Sonia"], key="plan")
        if user == "Luca":
            st.markdown("""### Plan ~2500 kcal
- **7h:** Porridge protéiné (380 kcal)
- **10h:** Shake protéiné (250 kcal)
- **12h30:** Poulet + riz + légumes (550 kcal)
- **16h:** Yaourt grec + amandes (200 kcal)
- **19h30:** Saumon + patate douce (500 kcal)
- **Post-training:** Shake (250 kcal)""")
        else:
            st.markdown("""### Plan ~1400 kcal
- **8h:** Omelette 2 oeufs (280 kcal)
- **10h30:** Yaourt 0% + fruits (120 kcal)
- **12h30:** Salade protéinée (380 kcal)
- **16h:** Amandes (100 kcal)
- **19h:** Poisson + légumes (350 kcal)""")

# ==================== MAIN ====================
st.markdown('<div class="main-header">💪 FitCouple - Luca & Sonia</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🥗 NUTRITION"])

with tab1:
    st.markdown("""<div class="profile-card">
    <b>Luca</b> | 88kg → 90kg | 1m95 | Objectif: Masse sèche + Perte ventre<br>
    <small>🔥 Circuit abdos: 3x/semaine (Lundi, Mercredi, Vendredi)</small>
    </div>""", unsafe_allow_html=True)
    
    nav = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression"], horizontal=True, key="luca_nav")
    
    if nav == "📅 Programme":
        day_idx = render_calendar(PROGRAM_LUCA)
        st.markdown("---")
        render_workout(PROGRAM_LUCA, day_idx, "Luca")
    elif nav == "📏 Mensurations":
        render_measurements("Luca", 88)
    else:
        render_progress("Luca", 90, 88, False)

with tab2:
    st.markdown("""<div class="profile-card">
    <b>Sonia</b> | 78kg → 65kg | 1m50 | Objectif: Perte poids + Tonification<br>
    <small>🔥 Circuit abdos: 3x/semaine (Lundi, Mercredi, Vendredi)</small>
    </div>""", unsafe_allow_html=True)
    
    nav = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression"], horizontal=True, key="sonia_nav")
    
    if nav == "📅 Programme":
        day_idx = render_calendar(PROGRAM_SONIA)
        st.markdown("---")
        render_workout(PROGRAM_SONIA, day_idx, "Sonia")
    elif nav == "📏 Mensurations":
        render_measurements("Sonia", 78)
    else:
        render_progress("Sonia", 65, 78, True)

with tab3:
    render_nutrition()

st.markdown("---")
st.caption("💪 FitCouple v2.1 | Entraînement Maison | Abdos 3x/semaine")
