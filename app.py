import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import calendar

# Configuration de la page avec PWA
st.set_page_config(
    page_title="FitCouple - Luca & Sonia",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS professionnel + PWA meta tags
st.markdown("""
<head>
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="FitCouple">
    <meta name="theme-color" content="#667eea">
    <link rel="manifest" href="manifest.json">
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .profile-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .calendar-day {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .calendar-day:hover {
        transform: translateY(-2px);
    }
    
    .calendar-today {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .exercise-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
    .video-link {
        display: inline-flex;
        align-items: center;
        background: #ff0000;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    .progress-good { color: #28a745; }
    .progress-neutral { color: #ffc107; }
    .progress-bad { color: #dc3545; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f1f3f4;
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .week-nav {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
            padding: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px;
            font-size: 0.9rem;
        }
    }
    
    /* Cacher le menu Streamlit pour look app */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== BASE DE DONNEES ====================
def init_db():
    conn = sqlite3.connect('fitness_pro.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS weight_tracking
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT UNIQUE,
                  weight REAL,
                  belly_cm REAL,
                  chest_cm REAL,
                  arms_cm REAL,
                  thighs_cm REAL,
                  hips_cm REAL,
                  notes TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS workouts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT,
                  workout_type TEXT,
                  duration INTEGER,
                  exercises TEXT,
                  performance TEXT,
                  feeling INTEGER,
                  notes TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS exercise_progress
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT,
                  exercise_name TEXT,
                  weight_kg REAL,
                  reps INTEGER,
                  sets INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  calories REAL,
                  protein REAL,
                  carbs REAL,
                  fat REAL,
                  ingredients TEXT,
                  instructions TEXT,
                  image_url TEXT)''')
    
    conn.commit()
    return conn

conn = init_db()

# ==================== VIDEOS EXERCICES ====================
EXERCISE_VIDEOS = {
    # Haut du corps
    "Développé couché": "https://www.youtube.com/watch?v=rT7DgCr-3pg",
    "Développé militaire": "https://www.youtube.com/watch?v=2yjwXTZQDDI",
    "Dips": "https://www.youtube.com/watch?v=2z8JmcrW-As",
    "Élévations latérales": "https://www.youtube.com/watch?v=3VcKaXpzqRo",
    "Extensions triceps": "https://www.youtube.com/watch?v=2-LAMcpzODU",
    "Tractions": "https://www.youtube.com/watch?v=eGo4IYlbE5g",
    "Rowing barre": "https://www.youtube.com/watch?v=FWJR5Ve8bnQ",
    "Tirage vertical": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
    "Curl biceps": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
    "Curl marteau": "https://www.youtube.com/watch?v=zC3nLlEvin4",
    "Pompes": "https://www.youtube.com/watch?v=IODxDxX7oi4",
    "Pompes genoux": "https://www.youtube.com/watch?v=jWxvty2KROs",
    "Rowing haltères": "https://www.youtube.com/watch?v=roCP6wCXPqo",
    
    # Bas du corps
    "Squats": "https://www.youtube.com/watch?v=ultWZbUMPL8",
    "Fentes": "https://www.youtube.com/watch?v=QOVaHwm-Q6U",
    "Hip thrust": "https://www.youtube.com/watch?v=SEdqd1n0cvg",
    "Soulevé de terre": "https://www.youtube.com/watch?v=op9kVnSso6Q",
    "Glute bridge": "https://www.youtube.com/watch?v=OUgsJ8-Vi0E",
    "Donkey kicks": "https://www.youtube.com/watch?v=SJ1Xuz9D-ZQ",
    "Fire hydrants": "https://www.youtube.com/watch?v=La3xrTxLXSE",
    "Abducteurs": "https://www.youtube.com/watch?v=FuMn1Gn2gcI",
    
    # Abdos
    "Crunch": "https://www.youtube.com/watch?v=Xyd_fa5zoEU",
    "Planche": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
    "Russian twist": "https://www.youtube.com/watch?v=wkD8rjkodUI",
    "Mountain climbers": "https://www.youtube.com/watch?v=nmwgirgXLYM",
    "Relevé de jambes": "https://www.youtube.com/watch?v=JB2oyawG9KI",
    "Gainage latéral": "https://www.youtube.com/watch?v=K2VljzCC16g",
    
    # Cardio
    "HIIT": "https://www.youtube.com/watch?v=ml6cT4AZdqI",
    "Burpees": "https://www.youtube.com/watch?v=TU8QYVW0gDU",
    "Jumping jacks": "https://www.youtube.com/watch?v=c4DAnQ6DtF8",
    "Squat jumps": "https://www.youtube.com/watch?v=A-cFYWvaHr0",
}

# ==================== PROGRAMMES COMPLETS ====================
PROGRAM_LUCA = {
    0: {  # Lundi
        "nom": "Push - Pectoraux/Épaules/Triceps",
        "type": "Musculation",
        "duree": 60,
        "exercices": [
            {"nom": "Développé couché", "series": 4, "reps": "10-12", "repos": 90, "kg_depart": 60},
            {"nom": "Développé militaire", "series": 3, "reps": "10-12", "repos": 90, "kg_depart": 30},
            {"nom": "Dips", "series": 3, "reps": "Max", "repos": 90, "kg_depart": 0},
            {"nom": "Élévations latérales", "series": 3, "reps": "15", "repos": 60, "kg_depart": 8},
            {"nom": "Extensions triceps", "series": 3, "reps": "12-15", "repos": 60, "kg_depart": 15},
        ]
    },
    1: {  # Mardi
        "nom": "Cardio HIIT + Abdos",
        "type": "Cardio",
        "duree": 45,
        "exercices": [
            {"nom": "HIIT", "series": 1, "reps": "30min", "repos": 0, "kg_depart": 0},
            {"nom": "Crunch", "series": 4, "reps": "20", "repos": 45, "kg_depart": 0},
            {"nom": "Planche", "series": 3, "reps": "60s", "repos": 45, "kg_depart": 0},
            {"nom": "Russian twist", "series": 3, "reps": "20", "repos": 45, "kg_depart": 5},
            {"nom": "Mountain climbers", "series": 3, "reps": "30", "repos": 45, "kg_depart": 0},
        ]
    },
    2: {  # Mercredi
        "nom": "Pull - Dos/Biceps",
        "type": "Musculation",
        "duree": 60,
        "exercices": [
            {"nom": "Tractions", "series": 4, "reps": "8-10", "repos": 120, "kg_depart": 0},
            {"nom": "Rowing barre", "series": 4, "reps": "10", "repos": 90, "kg_depart": 50},
            {"nom": "Tirage vertical", "series": 3, "reps": "12", "repos": 75, "kg_depart": 45},
            {"nom": "Curl biceps", "series": 3, "reps": "12", "repos": 60, "kg_depart": 12},
            {"nom": "Curl marteau", "series": 3, "reps": "12", "repos": 60, "kg_depart": 10},
        ]
    },
    3: {  # Jeudi
        "nom": "Repos Actif",
        "type": "Récupération",
        "duree": 30,
        "exercices": [
            {"nom": "Marche rapide ou vélo léger", "series": 1, "reps": "30min", "repos": 0, "kg_depart": 0},
            {"nom": "Étirements complets", "series": 1, "reps": "15min", "repos": 0, "kg_depart": 0},
        ]
    },
    4: {  # Vendredi
        "nom": "Full Body + Cardio",
        "type": "Mixte",
        "duree": 70,
        "exercices": [
            {"nom": "Squats", "series": 4, "reps": "12", "repos": 90, "kg_depart": 60},
            {"nom": "Soulevé de terre", "series": 3, "reps": "10", "repos": 120, "kg_depart": 70},
            {"nom": "Développé couché", "series": 3, "reps": "10", "repos": 90, "kg_depart": 55},
            {"nom": "Tractions", "series": 3, "reps": "8", "repos": 90, "kg_depart": 0},
            {"nom": "Planche", "series": 3, "reps": "45s", "repos": 45, "kg_depart": 0},
            {"nom": "Course ou vélo", "series": 1, "reps": "20min", "repos": 0, "kg_depart": 0},
        ]
    },
    5: {  # Samedi
        "nom": "Cardio Endurance",
        "type": "Cardio",
        "duree": 60,
        "exercices": [
            {"nom": "Vélo ou course", "series": 1, "reps": "45-60min", "repos": 0, "kg_depart": 0},
            {"nom": "Gainage latéral", "series": 2, "reps": "30s/côté", "repos": 30, "kg_depart": 0},
        ]
    },
    6: {  # Dimanche
        "nom": "Repos Complet",
        "type": "Repos",
        "duree": 0,
        "exercices": [
            {"nom": "Récupération", "series": 0, "reps": "-", "repos": 0, "kg_depart": 0},
        ]
    }
}

PROGRAM_SONIA = {
    0: {  # Lundi
        "nom": "Bas du corps + Fessiers",
        "type": "Renforcement",
        "duree": 50,
        "exercices": [
            {"nom": "Squats", "series": 4, "reps": "15", "repos": 60, "kg_depart": 10},
            {"nom": "Fentes", "series": 3, "reps": "12/jambe", "repos": 60, "kg_depart": 0},
            {"nom": "Hip thrust", "series": 4, "reps": "15", "repos": 60, "kg_depart": 20},
            {"nom": "Abducteurs", "series": 3, "reps": "20", "repos": 45, "kg_depart": 15},
            {"nom": "Glute bridge", "series": 3, "reps": "20", "repos": 45, "kg_depart": 0},
        ]
    },
    1: {  # Mardi
        "nom": "Cardio HIIT Brûle-graisse",
        "type": "Cardio",
        "duree": 35,
        "exercices": [
            {"nom": "Jumping jacks", "series": 4, "reps": "30s", "repos": 15, "kg_depart": 0},
            {"nom": "Squat jumps", "series": 4, "reps": "30s", "repos": 15, "kg_depart": 0},
            {"nom": "Mountain climbers", "series": 4, "reps": "30s", "repos": 15, "kg_depart": 0},
            {"nom": "Burpees", "series": 4, "reps": "30s", "repos": 15, "kg_depart": 0},
            {"nom": "Planche", "series": 3, "reps": "30s", "repos": 30, "kg_depart": 0},
        ]
    },
    2: {  # Mercredi
        "nom": "Haut du corps + Core",
        "type": "Renforcement",
        "duree": 45,
        "exercices": [
            {"nom": "Pompes genoux", "series": 3, "reps": "12", "repos": 60, "kg_depart": 0},
            {"nom": "Rowing haltères", "series": 3, "reps": "12", "repos": 60, "kg_depart": 5},
            {"nom": "Curl biceps", "series": 3, "reps": "15", "repos": 45, "kg_depart": 3},
            {"nom": "Élévations latérales", "series": 3, "reps": "15", "repos": 45, "kg_depart": 2},
            {"nom": "Crunch", "series": 3, "reps": "20", "repos": 45, "kg_depart": 0},
            {"nom": "Planche", "series": 3, "reps": "30s", "repos": 45, "kg_depart": 0},
        ]
    },
    3: {  # Jeudi
        "nom": "Cardio Modéré",
        "type": "Cardio",
        "duree": 45,
        "exercices": [
            {"nom": "Marche rapide ou vélo", "series": 1, "reps": "45min", "repos": 0, "kg_depart": 0},
            {"nom": "Étirements", "series": 1, "reps": "15min", "repos": 0, "kg_depart": 0},
        ]
    },
    4: {  # Vendredi
        "nom": "Circuit Full Body",
        "type": "Circuit",
        "duree": 40,
        "exercices": [
            {"nom": "Squats", "series": 3, "reps": "15", "repos": 30, "kg_depart": 0},
            {"nom": "Pompes genoux", "series": 3, "reps": "10", "repos": 30, "kg_depart": 0},
            {"nom": "Crunch", "series": 3, "reps": "20", "repos": 30, "kg_depart": 0},
            {"nom": "Fentes", "series": 3, "reps": "12/jambe", "repos": 30, "kg_depart": 0},
            {"nom": "Planche", "series": 3, "reps": "30s", "repos": 30, "kg_depart": 0},
            {"nom": "Glute bridge", "series": 3, "reps": "15", "repos": 30, "kg_depart": 0},
        ]
    },
    5: {  # Samedi
        "nom": "Fessiers Focus + Cardio",
        "type": "Mixte",
        "duree": 50,
        "exercices": [
            {"nom": "Hip thrust", "series": 4, "reps": "20", "repos": 45, "kg_depart": 15},
            {"nom": "Donkey kicks", "series": 4, "reps": "20/côté", "repos": 30, "kg_depart": 0},
            {"nom": "Fire hydrants", "series": 4, "reps": "20/côté", "repos": 30, "kg_depart": 0},
            {"nom": "Glute bridge", "series": 4, "reps": "20", "repos": 30, "kg_depart": 0},
            {"nom": "Marche rapide", "series": 1, "reps": "20min", "repos": 0, "kg_depart": 0},
        ]
    },
    6: {  # Dimanche
        "nom": "Repos Actif / Yoga",
        "type": "Récupération",
        "duree": 30,
        "exercices": [
            {"nom": "Yoga ou étirements", "series": 1, "reps": "30min", "repos": 0, "kg_depart": 0},
        ]
    }
}

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# ==================== FONCTIONS UTILITAIRES ====================
def get_week_dates():
    """Retourne les dates de la semaine actuelle"""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    return [start_of_week + timedelta(days=i) for i in range(7)]

def add_weight_entry(user, weight, belly, chest, arms, thighs, hips, notes):
    c = conn.cursor()
    today_str = date.today().isoformat()
    try:
        c.execute("""INSERT OR REPLACE INTO weight_tracking 
                    (user, date, weight, belly_cm, chest_cm, arms_cm, thighs_cm, hips_cm, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (user, today_str, weight, belly, chest, arms, thighs, hips, notes))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erreur: {e}")
        return False

def get_weight_history(user):
    return pd.read_sql_query(
        f"SELECT * FROM weight_tracking WHERE user = ? ORDER BY date",
        conn, params=(user,)
    )

def add_exercise_progress(user, exercise, weight_kg, reps, sets):
    c = conn.cursor()
    c.execute("""INSERT INTO exercise_progress (user, date, exercise_name, weight_kg, reps, sets)
                VALUES (?, ?, ?, ?, ?, ?)""",
             (user, date.today().isoformat(), exercise, weight_kg, reps, sets))
    conn.commit()

def get_exercise_progress(user, exercise):
    return pd.read_sql_query(
        "SELECT * FROM exercise_progress WHERE user = ? AND exercise_name = ? ORDER BY date",
        conn, params=(user, exercise)
    )

def add_workout_log(user, workout_type, duration, exercises, performance, feeling, notes):
    c = conn.cursor()
    c.execute("""INSERT INTO workouts (user, date, workout_type, duration, exercises, performance, feeling, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
             (user, date.today().isoformat(), workout_type, duration, 
              json.dumps(exercises), json.dumps(performance), feeling, notes))
    conn.commit()

def get_workout_history(user, limit=10):
    return pd.read_sql_query(
        f"SELECT * FROM workouts WHERE user = ? ORDER BY date DESC LIMIT ?",
        conn, params=(user, limit)
    )

def calculate_progress(df, column):
    """Calcule le progrès entre la première et dernière mesure"""
    if len(df) < 2:
        return 0, 0
    first = df[column].iloc[0]
    last = df[column].iloc[-1]
    diff = last - first
    pct = (diff / first) * 100 if first != 0 else 0
    return diff, pct

# ==================== COMPOSANTS UI ====================
def render_calendar(program, user):
    """Affiche le calendrier de la semaine avec le programme"""
    st.markdown("### 📅 Programme de la semaine")
    
    week_dates = get_week_dates()
    today = date.today()
    
    # Afficher la semaine
    cols = st.columns(7)
    
    for i, (jour_date, jour_nom) in enumerate(zip(week_dates, JOURS_SEMAINE)):
        with cols[i]:
            is_today = jour_date == today
            program_day = program.get(i, {})
            
            # Style conditionnel
            bg_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if is_today else "#f8f9fa"
            text_color = "white" if is_today else "#333"
            
            st.markdown(f"""
            <div style="background: {bg_color}; color: {text_color}; 
                        padding: 0.8rem; border-radius: 12px; text-align: center;
                        min-height: 120px; margin-bottom: 0.5rem;">
                <div style="font-weight: 600; font-size: 0.9rem;">{jour_nom}</div>
                <div style="font-size: 0.75rem; opacity: 0.8;">{jour_date.strftime('%d/%m')}</div>
                <hr style="margin: 0.5rem 0; opacity: 0.3;">
                <div style="font-size: 0.75rem; font-weight: 500;">
                    {program_day.get('nom', 'Repos')[:20]}
                </div>
                <div style="font-size: 0.65rem; opacity: 0.8;">
                    {program_day.get('duree', 0)} min
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    return today.weekday()

def render_todays_workout(program, day_index, user):
    """Affiche le détail de l'entraînement du jour"""
    workout = program.get(day_index, {})
    
    st.markdown(f"### 🎯 Entraînement du jour: **{workout.get('nom', 'Repos')}**")
    
    if workout.get('type') == 'Repos':
        st.info("💤 Jour de repos - Profitez-en pour récupérer !")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Type", workout.get('type', '-'))
    with col2:
        st.metric("Durée", f"{workout.get('duree', 0)} min")
    with col3:
        st.metric("Exercices", len(workout.get('exercices', [])))
    
    st.markdown("---")
    st.markdown("#### 📝 Liste des exercices")
    
    exercises = workout.get('exercices', [])
    performance_data = {}
    
    for i, ex in enumerate(exercises):
        with st.expander(f"**{i+1}. {ex['nom']}** - {ex['series']}x{ex['reps']}", expanded=(i==0)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                - **Séries:** {ex['series']}
                - **Répétitions:** {ex['reps']}
                - **Repos:** {ex['repos']}s
                - **Charge de départ:** {ex['kg_depart']} kg
                """)
                
                # Lien vidéo
                video_url = EXERCISE_VIDEOS.get(ex['nom'])
                if video_url:
                    st.markdown(f"""
                    <a href="{video_url}" target="_blank" style="
                        display: inline-flex; align-items: center; gap: 5px;
                        background: #ff0000; color: white; padding: 8px 12px;
                        border-radius: 6px; text-decoration: none; font-size: 0.85rem;">
                        ▶️ Voir la vidéo
                    </a>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Enregistrement de la performance
                st.markdown("**Enregistrer:**")
                kg = st.number_input("Charge (kg)", min_value=0.0, value=float(ex['kg_depart']), 
                                    step=0.5, key=f"kg_{user}_{i}")
                reps_done = st.number_input("Reps", min_value=0, value=10, key=f"reps_{user}_{i}")
                performance_data[ex['nom']] = {"kg": kg, "reps": reps_done}
    
    st.markdown("---")
    
    # Bouton pour enregistrer la séance
    col1, col2 = st.columns([2, 1])
    with col1:
        feeling = st.slider("😊 Comment vous sentez-vous ?", 1, 5, 3, 
                           help="1=Difficile, 5=Excellent")
    with col2:
        notes = st.text_input("📝 Notes", placeholder="Commentaires...")
    
    if st.button("✅ Enregistrer la séance", type="primary", use_container_width=True):
        # Sauvegarder chaque exercice
        for ex_name, perf in performance_data.items():
            add_exercise_progress(user, ex_name, perf['kg'], perf['reps'], 1)
        
        # Sauvegarder la séance
        add_workout_log(user, workout['type'], workout['duree'], 
                       [ex['nom'] for ex in exercises], performance_data, feeling, notes)
        st.success("🎉 Séance enregistrée avec succès !")
        st.balloons()

def render_progress_charts(user, target_weight, is_loss=True):
    """Affiche les graphiques de progression"""
    st.markdown("### 📈 Suivi de la progression")
    
    df = get_weight_history(user)
    
    if df.empty:
        st.info("📊 Aucune donnée enregistrée. Commencez votre suivi !")
        return
    
    # Graphique principal - Poids
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Evolution du Poids', 'Tour de Ventre', 'Tour de Bras', 'Tour de Cuisses'),
        vertical_spacing=0.12
    )
    
    # Poids
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['weight'], mode='lines+markers',
                  name='Poids', line=dict(color='#667eea', width=3)),
        row=1, col=1
    )
    fig.add_hline(y=target_weight, line_dash="dash", line_color="green",
                 annotation_text=f"Objectif: {target_weight}kg", row=1, col=1)
    
    # Tour de ventre
    if 'belly_cm' in df.columns:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['belly_cm'], mode='lines+markers',
                      name='Ventre', line=dict(color='#e91e63', width=3)),
            row=1, col=2
        )
    
    # Tour de bras
    if 'arms_cm' in df.columns and df['arms_cm'].notna().any():
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['arms_cm'], mode='lines+markers',
                      name='Bras', line=dict(color='#4caf50', width=3)),
            row=2, col=1
        )
    
    # Tour de cuisses
    if 'thighs_cm' in df.columns and df['thighs_cm'].notna().any():
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['thighs_cm'], mode='lines+markers',
                      name='Cuisses', line=dict(color='#ff9800', width=3)),
            row=2, col=2
        )
    
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Stats de progression
    st.markdown("#### 📊 Statistiques de progression")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if len(df) >= 1:
            first_w = df['weight'].iloc[0]
            last_w = df['weight'].iloc[-1]
            diff = last_w - first_w
            color = "progress-good" if (is_loss and diff < 0) or (not is_loss and diff > 0) else "progress-bad"
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 0.8rem; color: #666;">Poids de départ</div>
                <div style="font-size: 1.5rem; font-weight: 600;">{first_w:.1f} kg</div>
                <div style="font-size: 0.9rem;" class="{color}">{diff:+.1f} kg</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Poids actuel</div>
            <div style="font-size: 1.5rem; font-weight: 600;">{df['weight'].iloc[-1]:.1f} kg</div>
            <div style="font-size: 0.9rem; color: #666;">Objectif: {target_weight} kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        remaining = abs(df['weight'].iloc[-1] - target_weight)
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Restant</div>
            <div style="font-size: 1.5rem; font-weight: 600;">{remaining:.1f} kg</div>
            <div style="font-size: 0.9rem; color: #666;">{'\u00e0 perdre' if is_loss else '\u00e0 prendre'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if len(df) >= 2:
            days = (pd.to_datetime(df['date'].iloc[-1]) - pd.to_datetime(df['date'].iloc[0])).days
            days = max(days, 1)
            rate = abs(diff) / (days / 7)  # kg par semaine
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 0.8rem; color: #666;">Rythme</div>
                <div style="font-size: 1.5rem; font-weight: 600;">{rate:.2f} kg</div>
                <div style="font-size: 0.9rem; color: #666;">par semaine</div>
            </div>
            """, unsafe_allow_html=True)

def render_measurement_form(user):
    """Formulaire d'enregistrement des mensurations"""
    st.markdown("### 📏 Enregistrer mes mensurations")
    
    with st.form(f"measurements_{user}"):
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("⚖️ Poids (kg)", min_value=30.0, max_value=200.0, 
                                    value=88.0 if user=="Luca" else 78.0, step=0.1)
            belly = st.number_input("📍 Tour de ventre (cm)", min_value=50.0, max_value=150.0, 
                                   value=90.0, step=0.5)
            chest = st.number_input("📍 Tour de poitrine (cm)", min_value=50.0, max_value=150.0, 
                                   value=100.0, step=0.5)
        
        with col2:
            arms = st.number_input("💪 Tour de bras (cm)", min_value=20.0, max_value=60.0, 
                                  value=35.0, step=0.5)
            thighs = st.number_input("🦵 Tour de cuisses (cm)", min_value=30.0, max_value=100.0, 
                                    value=55.0, step=0.5)
            hips = st.number_input("🍑 Tour de hanches (cm)", min_value=50.0, max_value=150.0, 
                                  value=95.0, step=0.5)
        
        notes = st.text_input("📝 Notes", placeholder="Comment vous sentez-vous ?")
        
        if st.form_submit_button("✅ Enregistrer", type="primary", use_container_width=True):
            if add_weight_entry(user, weight, belly, chest, arms, thighs, hips, notes):
                st.success("🎉 Mensurations enregistrées !")
                st.rerun()

def render_exercise_performance(user, exercises):
    """Affiche la progression sur les exercices"""
    st.markdown("### 📈 Progression par exercice")
    
    exercise_names = list(set([ex['nom'] for day in exercises.values() for ex in day.get('exercices', [])]))
    selected_ex = st.selectbox("Choisir un exercice", exercise_names)
    
    df = get_exercise_progress(user, selected_ex)
    
    if df.empty:
        st.info(f"Aucune donnée pour {selected_ex}. Enregistrez vos performances !")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df, x='date', y='weight_kg', markers=True,
                     title=f"Charge sur {selected_ex}")
        fig.update_traces(line_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calculer le progrès
        if len(df) >= 2:
            first = df['weight_kg'].iloc[0]
            last = df['weight_kg'].iloc[-1]
            progress = last - first
            pct = (progress / first * 100) if first > 0 else 0
            
            st.metric("Charge initiale", f"{first:.1f} kg")
            st.metric("Charge actuelle", f"{last:.1f} kg", f"{progress:+.1f} kg ({pct:+.1f}%)")
            st.metric("Nombre de séances", len(df))

# ==================== RECETTES ====================
def init_recipes():
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recipes")
    if c.fetchone()[0] == 0:
        recipes = [
            ("Porridge Protéiné", "Petit-déjeuner", 380, 28, 45, 10,
             json.dumps(["80g flocons d'avoine", "30g whey", "250ml lait", "1 banane", "10g miel"]),
             "Cuire les flocons, ajouter whey hors feu, garnir", ""),
            ("Bowl Poulet Quinoa", "Déjeuner", 520, 45, 42, 18,
             json.dumps(["200g poulet", "100g quinoa", "Légumes", "Avocat", "Sauce"]),
             "Griller poulet, cuire quinoa, assembler", ""),
            ("Saumon Grillé Légumes", "Dîner", 420, 38, 20, 22,
             json.dumps(["180g saumon", "200g légumes verts", "Citron", "Herbes"]),
             "Griller saumon, cuire légumes vapeur", ""),
            ("Shake Récupération", "Collation", 250, 35, 20, 5,
             json.dumps(["40g whey", "300ml lait", "1 banane"]),
             "Mixer le tout", ""),
            ("Salade Protéinée", "Déjeuner", 380, 32, 15, 22,
             json.dumps(["150g thon", "2 oeufs", "Salade verte", "Tomates", "Vinaigrette légère"]),
             "Assembler tous les ingrédients", ""),
            ("Omelette Légumes", "Petit-déjeuner", 320, 25, 8, 22,
             json.dumps(["3 oeufs", "Poivrons", "Champignons", "Fromage allégé"]),
             "Battre oeufs, cuire avec légumes", ""),
        ]
        c.executemany("INSERT INTO recipes (name, category, calories, protein, carbs, fat, ingredients, instructions, image_url) VALUES (?,?,?,?,?,?,?,?,?)", recipes)
        conn.commit()

init_recipes()

def render_nutrition_section():
    """Section nutrition complète"""
    
    sub_tab = st.radio("", ["📖 Recettes", "🧮 Calculateur", "🍽️ Plans"], horizontal=True)
    
    if sub_tab == "📖 Recettes":
        recipes_df = pd.read_sql_query("SELECT * FROM recipes", conn)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            category = st.selectbox("Catégorie", ["Toutes", "Petit-déjeuner", "Déjeuner", "Dîner", "Collation"])
            portions = st.number_input("Portions", 1, 10, 2)
        
        if category != "Toutes":
            recipes_df = recipes_df[recipes_df['category'] == category]
        
        with col2:
            for _, r in recipes_df.iterrows():
                with st.expander(f"**{r['name']}** | {r['calories']:.0f} kcal | P:{r['protein']:.0f}g"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown("**Ingrédients:**")
                        for ing in json.loads(r['ingredients']):
                            st.write(f"• {ing}")
                        st.markdown(f"**Instructions:** {r['instructions']}")
                    with col_b:
                        st.markdown(f"**Pour {portions} pers:**")
                        st.metric("Calories", f"{r['calories']*portions:.0f}")
                        st.metric("Protéines", f"{r['protein']*portions:.0f}g")
    
    elif sub_tab == "🧮 Calculateur":
        st.markdown("### Calculateur de besoins")
        
        col1, col2 = st.columns(2)
        with col1:
            user = st.selectbox("Profil", ["Luca", "Sonia"])
            activity = st.select_slider("Activité", ["Sédentaire", "Léger", "Modéré", "Actif", "Très actif"])
        
        activity_mult = {"Sédentaire": 1.2, "Léger": 1.375, "Modéré": 1.55, "Actif": 1.725, "Très actif": 1.9}
        
        if user == "Luca":
            bmr = 10 * 88 + 6.25 * 195 - 5 * 30 + 5
            target_cal = bmr * activity_mult[activity] + 200
            protein = 88 * 2
        else:
            bmr = 10 * 78 + 6.25 * 150 - 5 * 30 - 161
            target_cal = bmr * activity_mult[activity] - 500
            protein = 78 * 1.8
        
        with col2:
            st.metric("Calories/jour", f"{target_cal:.0f} kcal")
            st.metric("Protéines", f"{protein:.0f}g")
            st.metric("Glucides", f"{target_cal * 0.4 / 4:.0f}g")
            st.metric("Lipides", f"{target_cal * 0.3 / 9:.0f}g")
    
    else:  # Plans
        st.markdown("### Plans alimentaires types")
        
        user = st.selectbox("Profil", ["Luca", "Sonia"], key="plan_user")
        
        if user == "Luca":
            plan = {
                "7h - Petit-déj": "Porridge protéiné + banane (380 kcal)",
                "10h - Collation": "Shake protéiné (250 kcal)",
                "12h30 - Déjeuner": "Poulet + riz + légumes (550 kcal)",
                "16h - Collation": "Yaourt grec + amandes (200 kcal)",
                "19h30 - Dîner": "Saumon + patate douce + légumes (500 kcal)",
                "Post-training": "Shake récupération (250 kcal)"
            }
            total = 2130
        else:
            plan = {
                "8h - Petit-déj": "Omelette 2 oeufs + pain complet (280 kcal)",
                "10h30 - Collation": "Yaourt 0% + fruits (120 kcal)",
                "12h30 - Déjeuner": "Salade protéinée (380 kcal)",
                "16h - Collation": "Poignée d'amandes (100 kcal)",
                "19h - Dîner": "Poisson + légumes vapeur (350 kcal)"
            }
            total = 1230
        
        for meal, content in plan.items():
            st.markdown(f"**{meal}:** {content}")
        
        st.markdown(f"---\n**Total: {total} kcal**")

# ==================== MAIN APP ====================
st.markdown('<div class="main-header">💪 FitCouple - Luca & Sonia</div>', unsafe_allow_html=True)

# Navigation principale
tab1, tab2, tab3 = st.tabs(["🏋️ Luca", "🧘 Sonia", "🥗 Nutrition"])

with tab1:
    st.markdown("""<div class="profile-card">
    <h3>👤 Profil de Luca</h3>
    <p><b>Objectif:</b> Prise de masse sèche + Perte de ventre</p>
    <p><b>Poids:</b> 88 kg → 90 kg | <b>Taille:</b> 1m95 | <b>IMC:</b> 23.1</p>
    </div>""", unsafe_allow_html=True)
    
    luca_tab = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression", "🏆 Performances"], 
                        horizontal=True, key="luca_nav")
    
    if luca_tab == "📅 Programme":
        day_idx = render_calendar(PROGRAM_LUCA, "Luca")
        st.markdown("---")
        render_todays_workout(PROGRAM_LUCA, day_idx, "Luca")
    
    elif luca_tab == "📏 Mensurations":
        render_measurement_form("Luca")
    
    elif luca_tab == "📈 Progression":
        render_progress_charts("Luca", target_weight=90, is_loss=False)
    
    else:
        render_exercise_performance("Luca", PROGRAM_LUCA)

with tab2:
    st.markdown("""<div class="profile-card">
    <h3>👤 Profil de Sonia</h3>
    <p><b>Objectif:</b> Perte de poids + Tonification</p>
    <p><b>Poids:</b> 78 kg → 65 kg | <b>Taille:</b> 1m50 | <b>IMC:</b> 34.7</p>
    </div>""", unsafe_allow_html=True)
    
    sonia_tab = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression", "🏆 Performances"], 
                         horizontal=True, key="sonia_nav")
    
    if sonia_tab == "📅 Programme":
        day_idx = render_calendar(PROGRAM_SONIA, "Sonia")
        st.markdown("---")
        render_todays_workout(PROGRAM_SONIA, day_idx, "Sonia")
    
    elif sonia_tab == "📏 Mensurations":
        render_measurement_form("Sonia")
    
    elif sonia_tab == "📈 Progression":
        render_progress_charts("Sonia", target_weight=65, is_loss=True)
    
    else:
        render_exercise_performance("Sonia", PROGRAM_SONIA)

with tab3:
    render_nutrition_section()

# Footer
st.markdown("""<div style="text-align: center; padding: 2rem; color: #666; font-size: 0.85rem;">
    💪 FitCouple App | Version 2.0 Pro | 
    <em>La persévérance est la clé du succès !</em>
</div>""", unsafe_allow_html=True)
