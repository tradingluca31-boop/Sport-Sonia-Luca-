import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.graph_objects as go

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

# ==================== SESSION STATE ====================
if 'weight_luca' not in st.session_state:
    st.session_state.weight_luca = []
if 'weight_sonia' not in st.session_state:
    st.session_state.weight_sonia = []
if 'workouts_luca' not in st.session_state:
    st.session_state.workouts_luca = []
if 'workouts_sonia' not in st.session_state:
    st.session_state.workouts_sonia = []

# ==================== VIDEOS ====================
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

# ==================== CIRCUIT ABDOS ====================
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
    0: {"nom": "PUSH", "type": "Musculation", "duree": 50, "abdos": True,
        "exercices": [
            {"nom": "Pompes", "sets": "4x12-15"},
            {"nom": "Pompes inclinées", "sets": "3x12"},
            {"nom": "Pike push-ups", "sets": "3x10"},
            {"nom": "Développé haltères", "sets": "3x12"},
            {"nom": "Élévations latérales", "sets": "3x15"},
            {"nom": "Pompes serrées", "sets": "3x12"},
            {"nom": "Dips chaise", "sets": "3x12"},
            {"nom": "Extension triceps", "sets": "3x12"},
        ]},
    1: {"nom": "PULL", "type": "Musculation", "duree": 45, "abdos": False,
        "exercices": [
            {"nom": "Rowing haltère", "sets": "4x10-12/bras"},
            {"nom": "Superman", "sets": "3x15"},
            {"nom": "Oiseau", "sets": "3x15"},
            {"nom": "Curl biceps", "sets": "4x12"},
            {"nom": "Curl marteau", "sets": "3x12"},
        ]},
    2: {"nom": "LEGS + HIIT", "type": "Jambes/Cardio", "duree": 55, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x15"},
            {"nom": "Squats sumo", "sets": "3x15"},
            {"nom": "Fentes", "sets": "3x12/jambe"},
            {"nom": "Jumping jacks", "sets": "3x45sec"},
            {"nom": "High knees", "sets": "3x45sec"},
            {"nom": "Burpees", "sets": "3x10"},
        ]},
    3: {"nom": "REPOS ACTIF", "type": "Récup", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Marche/vélo léger", "sets": "20-30min"},
            {"nom": "Étirements", "sets": "10min"},
        ]},
    4: {"nom": "FULL BODY", "type": "Musculation", "duree": 55, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x12"},
            {"nom": "Pompes", "sets": "4x15"},
            {"nom": "Rowing haltère", "sets": "4x12/bras"},
            {"nom": "Fentes", "sets": "3x10/jambe"},
            {"nom": "Développé haltères", "sets": "3x12"},
            {"nom": "Curl biceps", "sets": "3x12"},
            {"nom": "Dips chaise", "sets": "3x12"},
        ]},
    5: {"nom": "CARDIO", "type": "Cardio", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Vélo ou course", "sets": "30-40min"},
        ]},
    6: {"nom": "REPOS", "type": "Repos", "duree": 0, "abdos": False,
        "exercices": [
            {"nom": "Récupération", "sets": "-"},
        ]},
}

PROGRAM_SONIA = {
    0: {"nom": "BAS DU CORPS", "type": "Renforcement", "duree": 45, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "4x15"},
            {"nom": "Hip thrust", "sets": "4x15"},
            {"nom": "Fentes", "sets": "3x12/jambe"},
            {"nom": "Glute bridge", "sets": "3x20"},
            {"nom": "Donkey kicks", "sets": "3x20/côté"},
            {"nom": "Fire hydrants", "sets": "3x20/côté"},
        ]},
    1: {"nom": "HIIT", "type": "Cardio HIIT", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Jumping jacks", "sets": "4x30sec"},
            {"nom": "Squat jumps", "sets": "4x30sec"},
            {"nom": "Mountain climbers", "sets": "4x30sec"},
            {"nom": "Burpees", "sets": "4x30sec"},
            {"nom": "High knees", "sets": "4x30sec"},
        ]},
    2: {"nom": "HAUT + CORE", "type": "Renforcement", "duree": 40, "abdos": True,
        "exercices": [
            {"nom": "Pompes", "sets": "3x12"},
            {"nom": "Rowing haltère", "sets": "3x12/bras"},
            {"nom": "Élévations latérales", "sets": "3x15"},
            {"nom": "Curl biceps", "sets": "3x15"},
            {"nom": "Extension triceps", "sets": "3x15"},
            {"nom": "Gainage (Planche)", "sets": "3x30sec"},
        ]},
    3: {"nom": "CARDIO MODÉRÉ", "type": "Cardio", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Marche rapide/vélo", "sets": "35min"},
            {"nom": "Étirements", "sets": "10min"},
        ]},
    4: {"nom": "CIRCUIT", "type": "Circuit", "duree": 40, "abdos": True,
        "exercices": [
            {"nom": "Squats", "sets": "3x15"},
            {"nom": "Pompes", "sets": "3x10"},
            {"nom": "Fentes", "sets": "3x10/jambe"},
            {"nom": "Rowing haltère", "sets": "3x10/bras"},
            {"nom": "Glute bridge", "sets": "3x15"},
            {"nom": "Gainage (Planche)", "sets": "3x30sec"},
        ]},
    5: {"nom": "FESSIERS", "type": "Renforcement", "duree": 40, "abdos": False,
        "exercices": [
            {"nom": "Hip thrust", "sets": "4x20"},
            {"nom": "Squats sumo", "sets": "4x15"},
            {"nom": "Donkey kicks", "sets": "4x20/côté"},
            {"nom": "Fire hydrants", "sets": "4x20/côté"},
            {"nom": "Glute bridge", "sets": "50 reps"},
        ]},
    6: {"nom": "REPOS/YOGA", "type": "Récup", "duree": 30, "abdos": False,
        "exercices": [
            {"nom": "Yoga/étirements", "sets": "20-30min"},
        ]},
}

# ==================== FONCTIONS ====================
def render_calendar(program, user_key):
    today_idx = date.today().weekday()
    cols = st.columns(7)
    
    for i, jour in enumerate(JOURS):
        with cols[i]:
            is_today = (i == today_idx)
            p = program.get(i, {})
            
            css_class = "day-today" if is_today else "day-normal"
            marker = "👉" if is_today else ""
            abdos = "🔥" if p.get('abdos') else ""
            
            st.markdown(f"""
            <div class="day-card {css_class}">
                <b>{marker}{jour[:3]}</b><br>
                <small>{p.get('nom', 'Repos')[:12]}</small><br>
                <small>{p.get('duree', 0)}min {abdos}</small>
            </div>
            """, unsafe_allow_html=True)
    
    return today_idx

def render_workout(program, day_idx, user_key):
    workout = program.get(day_idx, {})
    
    st.markdown(f"## 🎯 {workout.get('nom', 'Repos')}")
    
    if workout.get('type') == 'Repos':
        st.success("💤 Jour de repos !")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Type", workout.get('type', '-'))
    col2.metric("Durée", f"{workout.get('duree', 0)} min")
    col3.metric("Abdos", "✅" if workout.get('abdos') else "❌")
    
    st.markdown("### 📝 Exercices")
    
    for idx, ex in enumerate(workout.get('exercices', [])):
        video = VIDEOS.get(ex['nom'], '')
        link = f" [🎬]({video})" if video else ""
        st.markdown(f"{idx+1}. **{ex['nom']}** - {ex['sets']}{link}")
    
    if workout.get('abdos'):
        st.markdown("""<div class="abdos-circuit">
            <b>🔥 CIRCUIT ABDOS (2 tours)</b>
        </div>""", unsafe_allow_html=True)
        
        for ex in CIRCUIT_ABDOS:
            video = VIDEOS.get(ex['nom'], '')
            link = f" [🎬]({video})" if video else ""
            st.markdown(f"• **{ex['nom']}** - {ex['reps']}{link}")
    
    st.markdown("---")
    
    feeling = st.slider("Comment était la séance ?", 1, 5, 3, key=f"feeling_{user_key}")
    
    if st.button("✅ Séance terminée !", key=f"btn_{user_key}", type="primary"):
        if user_key == "luca":
            st.session_state.workouts_luca.append({'date': str(date.today()), 'workout': workout.get('nom'), 'feeling': feeling})
        else:
            st.session_state.workouts_sonia.append({'date': str(date.today()), 'workout': workout.get('nom'), 'feeling': feeling})
        st.success("🎉 Bravo !")
        st.balloons()

def render_measurements(user_key, default_weight):
    st.markdown("### 📏 Mensurations")
    
    with st.form(key=f"form_mesure_{user_key}"):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Poids (kg)", 30.0, 200.0, float(default_weight), 0.1, key=f"w_{user_key}")
            belly = st.number_input("Ventre (cm)", 50.0, 150.0, 90.0, 0.5, key=f"b_{user_key}")
        with col2:
            arms = st.number_input("Bras (cm)", 20.0, 60.0, 35.0, 0.5, key=f"a_{user_key}")
            thighs = st.number_input("Cuisses (cm)", 30.0, 100.0, 55.0, 0.5, key=f"t_{user_key}")
        
        if st.form_submit_button("✅ Enregistrer"):
            data = {'date': str(date.today()), 'weight': weight, 'belly': belly, 'arms': arms, 'thighs': thighs}
            if user_key == "luca":
                st.session_state.weight_luca.append(data)
            else:
                st.session_state.weight_sonia.append(data)
            st.success("Enregistré !")
            st.rerun()

def render_progress(user_key, target, start):
    st.markdown("### 📈 Progression")
    
    data = st.session_state.weight_luca if user_key == "luca" else st.session_state.weight_sonia
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Départ", f"{start} kg")
    col2.metric("Objectif", f"{target} kg")
    
    if data:
        current = data[-1]['weight']
        diff = current - start
        col3.metric("Actuel", f"{current} kg", f"{diff:+.1f} kg")
        
        df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['weight'], mode='lines+markers', name='Poids'))
        fig.add_hline(y=target, line_dash="dash", line_color="green")
        fig.update_layout(height=300, title="Évolution du poids")
        st.plotly_chart(fig, use_container_width=True)
    else:
        col3.metric("Actuel", "- kg")
        st.info("Enregistrez vos mensurations !")

def render_nutrition():
    st.markdown("### 🥗 Nutrition")
    
    tab = st.radio("Section", ["📖 Recettes", "🍽️ Plans"], horizontal=True, key="nutri_tab")
    
    if tab == "📖 Recettes":
        recettes = [
            "**Porridge Protéiné** - 380 kcal - 28g prot",
            "**Bowl Poulet Quinoa** - 520 kcal - 45g prot",
            "**Saumon Légumes** - 420 kcal - 38g prot",
            "**Shake Protéiné** - 250 kcal - 35g prot",
            "**Salade Protéinée** - 380 kcal - 32g prot",
            "**Omelette Légumes** - 320 kcal - 25g prot",
        ]
        for r in recettes:
            st.markdown(f"• {r}")
    else:
        user = st.selectbox("Profil", ["Luca", "Sonia"], key="plan_select")
        if user == "Luca":
            st.markdown("""**Plan ~2500 kcal**
- 7h: Porridge protéiné
- 10h: Shake
- 12h30: Poulet + riz + légumes
- 16h: Yaourt + amandes
- 19h30: Saumon + patate douce""")
        else:
            st.markdown("""**Plan ~1400 kcal**
- 8h: Omelette 2 oeufs
- 10h30: Yaourt 0%
- 12h30: Salade protéinée
- 16h: Amandes
- 19h: Poisson + légumes""")

# ==================== MAIN ====================
st.markdown('<div class="main-header">💪 FitCouple - Luca & Sonia</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🥗 NUTRITION"])

with tab1:
    st.markdown("""<div class="profile-card">
    <b>Luca</b> | 88kg → 90kg | 1m95<br>
    <small>🔥 Abdos: Lundi, Mercredi, Vendredi</small>
    </div>""", unsafe_allow_html=True)
    
    nav_luca = st.radio("Navigation", ["📅 Programme", "📏 Mensurations", "📈 Progression"], 
                        horizontal=True, key="nav_luca")
    
    if nav_luca == "📅 Programme":
        day_idx = render_calendar(PROGRAM_LUCA, "luca")
        st.markdown("---")
        render_workout(PROGRAM_LUCA, day_idx, "luca")
    elif nav_luca == "📏 Mensurations":
        render_measurements("luca", 88)
    else:
        render_progress("luca", 90, 88)

with tab2:
    st.markdown("""<div class="profile-card">
    <b>Sonia</b> | 78kg → 65kg | 1m50<br>
    <small>🔥 Abdos: Lundi, Mercredi, Vendredi</small>
    </div>""", unsafe_allow_html=True)
    
    nav_sonia = st.radio("Navigation", ["📅 Programme", "📏 Mensurations", "📈 Progression"], 
                         horizontal=True, key="nav_sonia")
    
    if nav_sonia == "📅 Programme":
        day_idx = render_calendar(PROGRAM_SONIA, "sonia")
        st.markdown("---")
        render_workout(PROGRAM_SONIA, day_idx, "sonia")
    elif nav_sonia == "📏 Mensurations":
        render_measurements("sonia", 78)
    else:
        render_progress("sonia", 65, 78)

with tab3:
    render_nutrition()

st.markdown("---")
st.caption("💪 FitCouple v2.2 | Abdos 3x/semaine")
