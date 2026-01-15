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
</head>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
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
    
    .abdos-circuit {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .exercise-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 3px solid #28a745;
    }
    
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
    
    @media (max-width: 768px) {
        .main-header { font-size: 1.5rem; padding: 1rem; }
        .stTabs [data-baseweb="tab"] { padding: 8px 12px; font-size: 0.9rem; }
    }
    
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
    # === ABDOS / CORE ===
    "Crunch classique": "https://www.youtube.com/watch?v=Xyd_fa5zoEU",
    "Crunch mains au ciel": "https://www.youtube.com/watch?v=9XUI0zNrgbE",
    "Obliques crunch": "https://www.youtube.com/watch?v=pDTHSnoGoEc",
    "Russian twist": "https://www.youtube.com/watch?v=wkD8rjkodUI",
    "Scissor kicks": "https://www.youtube.com/watch?v=WoNCIBVLbgY",
    "Portefeuille (V-ups)": "https://www.youtube.com/watch?v=iP2fjvG0g3w",
    "Gainage coudes (Planche)": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
    "Gainage latéral coude": "https://www.youtube.com/watch?v=K2VljzCC16g",
    "Mountain climbers": "https://www.youtube.com/watch?v=nmwgirgXLYM",
    "Relevé de jambes": "https://www.youtube.com/watch?v=JB2oyawG9KI",
    "Bicycle crunch": "https://www.youtube.com/watch?v=9FGilxCbdz8",
    "Dead bug": "https://www.youtube.com/watch?v=I5xbsA71v1A",
    "Planche dynamique": "https://www.youtube.com/watch?v=xbYhHYdJRYk",
    "Toe touches": "https://www.youtube.com/watch?v=9jU8rldVLjE",
    
    # === HAUT DU CORPS (MAISON) ===
    "Pompes classiques": "https://www.youtube.com/watch?v=IODxDxX7oi4",
    "Pompes serrées (triceps)": "https://www.youtube.com/watch?v=J0DnG1_S92I",
    "Pompes larges": "https://www.youtube.com/watch?v=x9y10HIzEng",
    "Pompes inclinées": "https://www.youtube.com/watch?v=4dF1DOWzf20",
    "Pompes déclinées": "https://www.youtube.com/watch?v=SKPab2YC8BE",
    "Pompes diamant": "https://www.youtube.com/watch?v=J0DnG1_S92I",
    "Pompes sur genoux": "https://www.youtube.com/watch?v=jWxvty2KROs",
    "Dips sur chaise": "https://www.youtube.com/watch?v=0326dy_-CzM",
    "Pike push-ups": "https://www.youtube.com/watch?v=sposDXWEB0A",
    "Curl biceps haltères": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
    "Curl marteau": "https://www.youtube.com/watch?v=zC3nLlEvin4",
    "Extension triceps haltère": "https://www.youtube.com/watch?v=_gsUck-7M74",
    "Rowing haltère": "https://www.youtube.com/watch?v=roCP6wCXPqo",
    "Élévations latérales": "https://www.youtube.com/watch?v=3VcKaXpzqRo",
    "Élévations frontales": "https://www.youtube.com/watch?v=gzDe-ELqwnQ",
    "Développé haltères": "https://www.youtube.com/watch?v=qEwKCR5JCog",
    "Oiseau (rear delt)": "https://www.youtube.com/watch?v=EA7u4Q_8HQ0",
    "Superman": "https://www.youtube.com/watch?v=z6PJMT2y8GQ",
    "Rowing inversé (table)": "https://www.youtube.com/watch?v=hXTc1mDnZCw",
    
    # === BAS DU CORPS ===
    "Squats": "https://www.youtube.com/watch?v=ultWZbUMPL8",
    "Squats sumo": "https://www.youtube.com/watch?v=9ZuXKqRbT9k",
    "Squats goblet": "https://www.youtube.com/watch?v=MeIiIdhvXT4",
    "Fentes avant": "https://www.youtube.com/watch?v=QOVaHwm-Q6U",
    "Fentes arrière": "https://www.youtube.com/watch?v=xrPteyQLGAo",
    "Fentes latérales": "https://www.youtube.com/watch?v=gwWv7aPcD88",
    "Fentes marchées": "https://www.youtube.com/watch?v=L8fvypPrzzs",
    "Hip thrust": "https://www.youtube.com/watch?v=SEdqd1n0cvg",
    "Glute bridge": "https://www.youtube.com/watch?v=OUgsJ8-Vi0E",
    "Single leg glute bridge": "https://www.youtube.com/watch?v=AVAXhy6pl7o",
    "Donkey kicks": "https://www.youtube.com/watch?v=SJ1Xuz9D-ZQ",
    "Fire hydrants": "https://www.youtube.com/watch?v=La3xrTxLXSE",
    "Clamshells": "https://www.youtube.com/watch?v=re8dHxKhfEs",
    "Step-ups": "https://www.youtube.com/watch?v=WCFCdxzFBa4",
    "Bulgarian split squat": "https://www.youtube.com/watch?v=2C-uNgKwPLE",
    "Wall sit": "https://www.youtube.com/watch?v=y-wV4Venusw",
    "Mollets debout": "https://www.youtube.com/watch?v=gwLzBJYoWlI",
    "Soudané de terre roumain": "https://www.youtube.com/watch?v=2SHsk9AzdjA",
    
    # === CARDIO ===
    "Jumping jacks": "https://www.youtube.com/watch?v=c4DAnQ6DtF8",
    "Burpees": "https://www.youtube.com/watch?v=TU8QYVW0gDU",
    "Burpees modifiés": "https://www.youtube.com/watch?v=0pL1UibGjbY",
    "High knees": "https://www.youtube.com/watch?v=D0bLJnSBNI8",
    "Squat jumps": "https://www.youtube.com/watch?v=A-cFYWvaHr0",
    "Fentes sautées": "https://www.youtube.com/watch?v=y7Iug7eC0dk",
    "Skaters": "https://www.youtube.com/watch?v=d1J3_Jlwtpw",
    "Box jumps (chaise)": "https://www.youtube.com/watch?v=52r_Ul5k03g",
    "Climbers rapides": "https://www.youtube.com/watch?v=nmwgirgXLYM",
}

# ==================== CIRCUIT ABDOS LUCA (OBLIGATOIRE) ====================
CIRCUIT_ABDOS_LUCA = {
    "nom": "🔥 CIRCUIT ABDOS FINAL (OBLIGATOIRE)",
    "description": "A faire à CHAQUE fin de séance - Sans repos entre exercices, 30s repos entre tours",
    "tours": 2,
    "exercices": [
        {"nom": "Obliques crunch", "reps": "20/côté", "tempo": "Contrôlé"},
        {"nom": "Gainage coudes (Planche)", "reps": "45 sec", "tempo": "Tenir"},
        {"nom": "Gainage latéral coude", "reps": "30 sec/côté", "tempo": "Tenir"},
        {"nom": "Russian twist", "reps": "20 total", "tempo": "Explosif"},
        {"nom": "Scissor kicks", "reps": "20", "tempo": "Contrôlé"},
        {"nom": "Portefeuille (V-ups)", "reps": "15", "tempo": "Explosif"},
        {"nom": "Crunch mains au ciel", "reps": "20", "tempo": "Contrôlé"},
        {"nom": "Bicycle crunch", "reps": "20 total", "tempo": "Contrôlé"},
    ]
}

# ==================== PROGRAMMES OPTIMISÉS MAISON ====================

# PROGRAMME LUCA - Push/Pull/Legs + Full Body adapté maison
# Basé sur les programmes reconnus: PPL, PHUL, et circuit training
PROGRAM_LUCA = {
    0: {  # Lundi - PUSH (Pecs, Épaules, Triceps)
        "nom": "PUSH - Pectoraux/Épaules/Triceps",
        "type": "Musculation Haut",
        "duree": 50,
        "focus": "Développer poitrine, épaules et triceps",
        "exercices": [
            {"nom": "Pompes larges", "series": 4, "reps": "12-15", "repos": 60, "kg_depart": 0, "muscle": "Pectoraux"},
            {"nom": "Pompes inclinées", "series": 3, "reps": "12", "repos": 60, "kg_depart": 0, "muscle": "Haut pecs"},
            {"nom": "Pike push-ups", "series": 3, "reps": "10-12", "repos": 60, "kg_depart": 0, "muscle": "Épaules"},
            {"nom": "Développé haltères", "series": 3, "reps": "12", "repos": 60, "kg_depart": 8, "muscle": "Épaules"},
            {"nom": "Élévations latérales", "series": 3, "reps": "15", "repos": 45, "kg_depart": 5, "muscle": "Épaules"},
            {"nom": "Pompes serrées (triceps)", "series": 3, "reps": "12", "repos": 60, "kg_depart": 0, "muscle": "Triceps"},
            {"nom": "Dips sur chaise", "series": 3, "reps": "12-15", "repos": 60, "kg_depart": 0, "muscle": "Triceps"},
            {"nom": "Extension triceps haltère", "series": 3, "reps": "12", "repos": 45, "kg_depart": 6, "muscle": "Triceps"},
        ],
        "circuit_abdos": True
    },
    1: {  # Mardi - PULL (Dos, Biceps)
        "nom": "PULL - Dos/Biceps",
        "type": "Musculation Haut",
        "duree": 50,
        "focus": "Développer dos et biceps pour un V-shape",
        "exercices": [
            {"nom": "Rowing haltère", "series": 4, "reps": "10-12/bras", "repos": 60, "kg_depart": 12, "muscle": "Dos"},
            {"nom": "Rowing inversé (table)", "series": 3, "reps": "12", "repos": 60, "kg_depart": 0, "muscle": "Dos"},
            {"nom": "Superman", "series": 3, "reps": "15", "repos": 45, "kg_depart": 0, "muscle": "Lombaires"},
            {"nom": "Oiseau (rear delt)", "series": 3, "reps": "15", "repos": 45, "kg_depart": 4, "muscle": "Arrière épaule"},
            {"nom": "Curl biceps haltères", "series": 4, "reps": "12", "repos": 60, "kg_depart": 8, "muscle": "Biceps"},
            {"nom": "Curl marteau", "series": 3, "reps": "12", "repos": 45, "kg_depart": 8, "muscle": "Biceps"},
        ],
        "circuit_abdos": True
    },
    2: {  # Mercredi - LEGS + Cardio
        "nom": "LEGS + Cardio HIIT",
        "type": "Jambes + Cardio",
        "duree": 55,
        "focus": "Jambes puissantes + brûlage graisse ventre",
        "exercices": [
            {"nom": "Squats", "series": 4, "reps": "15", "repos": 60, "kg_depart": 0, "muscle": "Quadriceps"},
            {"nom": "Squats sumo", "series": 3, "reps": "15", "repos": 60, "kg_depart": 10, "muscle": "Adducteurs"},
            {"nom": "Fentes marchées", "series": 3, "reps": "12/jambe", "repos": 60, "kg_depart": 0, "muscle": "Quadriceps"},
            {"nom": "Soudané de terre roumain", "series": 3, "reps": "12", "repos": 60, "kg_depart": 10, "muscle": "Ischio-jambiers"},
            {"nom": "Mollets debout", "series": 4, "reps": "20", "repos": 45, "kg_depart": 10, "muscle": "Mollets"},
            {"nom": "--- HIIT 15 min ---", "series": 1, "reps": "Circuit", "repos": 0, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Jumping jacks", "series": 3, "reps": "45 sec", "repos": 15, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "High knees", "series": 3, "reps": "45 sec", "repos": 15, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Burpees modifiés", "series": 3, "reps": "10", "repos": 15, "kg_depart": 0, "muscle": "Cardio"},
        ],
        "circuit_abdos": True
    },
    3: {  # Jeudi - Repos actif + Mobilité
        "nom": "REPOS ACTIF + Mobilité",
        "type": "Récupération",
        "duree": 30,
        "focus": "Récupération active et mobilité",
        "exercices": [
            {"nom": "Marche rapide ou vélo léger", "series": 1, "reps": "20 min", "repos": 0, "kg_depart": 0, "muscle": "Cardio léger"},
            {"nom": "Étirements dynamiques", "series": 1, "reps": "10 min", "repos": 0, "kg_depart": 0, "muscle": "Mobilité"},
            {"nom": "Foam rolling (si dispo)", "series": 1, "reps": "5 min", "repos": 0, "kg_depart": 0, "muscle": "Récupération"},
        ],
        "circuit_abdos": False
    },
    4: {  # Vendredi - FULL BODY Intensif
        "nom": "FULL BODY Intensif",
        "type": "Full Body",
        "duree": 60,
        "focus": "Travailler tout le corps en intensité",
        "exercices": [
            {"nom": "Squats goblet", "series": 4, "reps": "12", "repos": 60, "kg_depart": 12, "muscle": "Jambes"},
            {"nom": "Pompes classiques", "series": 4, "reps": "15", "repos": 60, "kg_depart": 0, "muscle": "Pectoraux"},
            {"nom": "Rowing haltère", "series": 4, "reps": "12/bras", "repos": 60, "kg_depart": 12, "muscle": "Dos"},
            {"nom": "Fentes arrière", "series": 3, "reps": "10/jambe", "repos": 60, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "Développé haltères", "series": 3, "reps": "12", "repos": 60, "kg_depart": 8, "muscle": "Épaules"},
            {"nom": "Curl biceps haltères", "series": 3, "reps": "12", "repos": 45, "kg_depart": 8, "muscle": "Biceps"},
            {"nom": "Dips sur chaise", "series": 3, "reps": "12", "repos": 45, "kg_depart": 0, "muscle": "Triceps"},
        ],
        "circuit_abdos": True
    },
    5: {  # Samedi - Cardio + Abdos Focus
        "nom": "CARDIO BRÛLE-GRAISSE + Abdos",
        "type": "Cardio HIIT",
        "duree": 45,
        "focus": "Maximum de brûlage de graisse abdominale",
        "exercices": [
            {"nom": "--- CIRCUIT HIIT x3 ---", "series": 1, "reps": "Circuit", "repos": 0, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Burpees", "series": 3, "reps": "10", "repos": 20, "kg_depart": 0, "muscle": "Full body"},
            {"nom": "Squat jumps", "series": 3, "reps": "15", "repos": 20, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "Mountain climbers", "series": 3, "reps": "30", "repos": 20, "kg_depart": 0, "muscle": "Core"},
            {"nom": "Skaters", "series": 3, "reps": "20", "repos": 20, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "High knees", "series": 3, "reps": "30 sec", "repos": 20, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Fentes sautées", "series": 3, "reps": "10/jambe", "repos": 20, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "--- Repos 2 min entre tours ---", "series": 1, "reps": "-", "repos": 120, "kg_depart": 0, "muscle": "-"},
        ],
        "circuit_abdos": True
    },
    6: {  # Dimanche - Repos
        "nom": "REPOS COMPLET",
        "type": "Repos",
        "duree": 0,
        "focus": "Récupération et croissance musculaire",
        "exercices": [
            {"nom": "Étirements légers (optionnel)", "series": 1, "reps": "15 min", "repos": 0, "kg_depart": 0, "muscle": "Récupération"},
        ],
        "circuit_abdos": False
    }
}

# PROGRAMME SONIA - Spécialisé perte de poids + tonification
# Basé sur: HIIT, circuit training, et renforcement ciblé
PROGRAM_SONIA = {
    0: {  # Lundi - Bas du corps focus fessiers
        "nom": "BAS DU CORPS - Fessiers & Cuisses",
        "type": "Renforcement",
        "duree": 45,
        "focus": "Sculpter fessiers et affiner cuisses",
        "exercices": [
            {"nom": "Squats", "series": 4, "reps": "15", "repos": 45, "kg_depart": 0, "muscle": "Quadriceps/Fessiers"},
            {"nom": "Hip thrust", "series": 4, "reps": "15", "repos": 45, "kg_depart": 10, "muscle": "Fessiers"},
            {"nom": "Fentes arrière", "series": 3, "reps": "12/jambe", "repos": 45, "kg_depart": 0, "muscle": "Fessiers/Cuisses"},
            {"nom": "Glute bridge", "series": 3, "reps": "20", "repos": 30, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Donkey kicks", "series": 3, "reps": "20/côté", "repos": 30, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Fire hydrants", "series": 3, "reps": "20/côté", "repos": 30, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Clamshells", "series": 3, "reps": "20/côté", "repos": 30, "kg_depart": 0, "muscle": "Abducteurs"},
            {"nom": "Wall sit", "series": 3, "reps": "30 sec", "repos": 30, "kg_depart": 0, "muscle": "Cuisses"},
        ],
        "circuit_abdos": True
    },
    1: {  # Mardi - HIIT Brûle-graisse
        "nom": "HIIT BRÛLE-GRAISSE",
        "type": "Cardio HIIT",
        "duree": 30,
        "focus": "Maximum de calories brûlées en minimum de temps",
        "exercices": [
            {"nom": "--- Échauffement 3 min ---", "series": 1, "reps": "-", "repos": 0, "kg_depart": 0, "muscle": "-"},
            {"nom": "Jumping jacks", "series": 1, "reps": "1 min", "repos": 0, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "--- CIRCUIT x4 tours ---", "series": 1, "reps": "-", "repos": 0, "kg_depart": 0, "muscle": "-"},
            {"nom": "Squat jumps", "series": 4, "reps": "30 sec", "repos": 15, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "Mountain climbers", "series": 4, "reps": "30 sec", "repos": 15, "kg_depart": 0, "muscle": "Core"},
            {"nom": "Burpees modifiés", "series": 4, "reps": "30 sec", "repos": 15, "kg_depart": 0, "muscle": "Full body"},
            {"nom": "High knees", "series": 4, "reps": "30 sec", "repos": 15, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Skaters", "series": 4, "reps": "30 sec", "repos": 15, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "--- Repos 1 min entre tours ---", "series": 1, "reps": "-", "repos": 60, "kg_depart": 0, "muscle": "-"},
        ],
        "circuit_abdos": True
    },
    2: {  # Mercredi - Haut du corps + Core
        "nom": "HAUT DU CORPS + CORE",
        "type": "Renforcement",
        "duree": 40,
        "focus": "Tonifier bras, épaules et renforcer core",
        "exercices": [
            {"nom": "Pompes sur genoux", "series": 3, "reps": "12", "repos": 45, "kg_depart": 0, "muscle": "Pectoraux"},
            {"nom": "Rowing haltère", "series": 3, "reps": "12/bras", "repos": 45, "kg_depart": 4, "muscle": "Dos"},
            {"nom": "Élévations latérales", "series": 3, "reps": "15", "repos": 30, "kg_depart": 2, "muscle": "Épaules"},
            {"nom": "Élévations frontales", "series": 3, "reps": "12", "repos": 30, "kg_depart": 2, "muscle": "Épaules"},
            {"nom": "Curl biceps haltères", "series": 3, "reps": "15", "repos": 30, "kg_depart": 3, "muscle": "Biceps"},
            {"nom": "Extension triceps haltère", "series": 3, "reps": "15", "repos": 30, "kg_depart": 3, "muscle": "Triceps"},
            {"nom": "Dips sur chaise", "series": 3, "reps": "10", "repos": 45, "kg_depart": 0, "muscle": "Triceps"},
            {"nom": "Superman", "series": 3, "reps": "15", "repos": 30, "kg_depart": 0, "muscle": "Dos"},
        ],
        "circuit_abdos": True
    },
    3: {  # Jeudi - Cardio modéré
        "nom": "CARDIO MODÉRÉ",
        "type": "Cardio",
        "duree": 40,
        "focus": "Cardio zone brûle-graisse",
        "exercices": [
            {"nom": "Marche rapide ou vélo", "series": 1, "reps": "35 min", "repos": 0, "kg_depart": 0, "muscle": "Cardio"},
            {"nom": "Étirements", "series": 1, "reps": "10 min", "repos": 0, "kg_depart": 0, "muscle": "Récupération"},
        ],
        "circuit_abdos": False
    },
    4: {  # Vendredi - Circuit Full Body
        "nom": "CIRCUIT FULL BODY",
        "type": "Circuit Training",
        "duree": 40,
        "focus": "Tonification complète + cardio",
        "exercices": [
            {"nom": "--- Circuit x3 tours - Peu de repos ---", "series": 1, "reps": "-", "repos": 0, "kg_depart": 0, "muscle": "-"},
            {"nom": "Squats", "series": 3, "reps": "15", "repos": 20, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "Pompes sur genoux", "series": 3, "reps": "10", "repos": 20, "kg_depart": 0, "muscle": "Pectoraux"},
            {"nom": "Fentes avant", "series": 3, "reps": "10/jambe", "repos": 20, "kg_depart": 0, "muscle": "Jambes"},
            {"nom": "Rowing haltère", "series": 3, "reps": "10/bras", "repos": 20, "kg_depart": 4, "muscle": "Dos"},
            {"nom": "Glute bridge", "series": 3, "reps": "15", "repos": 20, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Gainage coudes (Planche)", "series": 3, "reps": "30 sec", "repos": 20, "kg_depart": 0, "muscle": "Core"},
            {"nom": "--- Repos 1 min entre tours ---", "series": 1, "reps": "-", "repos": 60, "kg_depart": 0, "muscle": "-"},
        ],
        "circuit_abdos": True
    },
    5: {  # Samedi - Fessiers Focus
        "nom": "FESSIERS INTENSIF",
        "type": "Renforcement",
        "duree": 40,
        "focus": "Sculpter et galber les fessiers",
        "exercices": [
            {"nom": "Hip thrust", "series": 4, "reps": "20", "repos": 45, "kg_depart": 15, "muscle": "Fessiers"},
            {"nom": "Single leg glute bridge", "series": 3, "reps": "15/jambe", "repos": 30, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Squats sumo", "series": 4, "reps": "15", "repos": 45, "kg_depart": 8, "muscle": "Fessiers/Adducteurs"},
            {"nom": "Donkey kicks", "series": 4, "reps": "20/côté", "repos": 20, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Fire hydrants", "series": 4, "reps": "20/côté", "repos": 20, "kg_depart": 0, "muscle": "Fessiers"},
            {"nom": "Clamshells", "series": 3, "reps": "25/côté", "repos": 20, "kg_depart": 0, "muscle": "Abducteurs"},
            {"nom": "Fentes latérales", "series": 3, "reps": "12/côté", "repos": 30, "kg_depart": 0, "muscle": "Cuisses"},
            {"nom": "--- Finisher: 50 Glute bridges ---", "series": 1, "reps": "50", "repos": 0, "kg_depart": 0, "muscle": "Fessiers"},
        ],
        "circuit_abdos": True
    },
    6: {  # Dimanche - Repos actif
        "nom": "REPOS ACTIF / YOGA",
        "type": "Récupération",
        "duree": 30,
        "focus": "Récupération et détente",
        "exercices": [
            {"nom": "Yoga ou étirements", "series": 1, "reps": "20-30 min", "repos": 0, "kg_depart": 0, "muscle": "Mobilité"},
            {"nom": "Marche légère (optionnel)", "series": 1, "reps": "15 min", "repos": 0, "kg_depart": 0, "muscle": "Récupération"},
        ],
        "circuit_abdos": False
    }
}

# Circuit abdos pour Sonia (adapté)
CIRCUIT_ABDOS_SONIA = {
    "nom": "🔥 CIRCUIT ABDOS VENTRE PLAT",
    "description": "A faire à la fin des séances - 2 tours avec 30s repos entre tours",
    "tours": 2,
    "exercices": [
        {"nom": "Crunch classique", "reps": "20", "tempo": "Contrôlé"},
        {"nom": "Gainage coudes (Planche)", "reps": "30 sec", "tempo": "Tenir"},
        {"nom": "Bicycle crunch", "reps": "20 total", "tempo": "Contrôlé"},
        {"nom": "Dead bug", "reps": "10/côté", "tempo": "Lent"},
        {"nom": "Mountain climbers", "reps": "20", "tempo": "Modéré"},
        {"nom": "Relevé de jambes", "reps": "15", "tempo": "Contrôlé"},
    ]
}

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# ==================== FONCTIONS UTILITAIRES ====================
def get_week_dates():
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
        "SELECT * FROM weight_tracking WHERE user = ? ORDER BY date",
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
        "SELECT * FROM workouts WHERE user = ? ORDER BY date DESC LIMIT ?",
        conn, params=(user, limit)
    )

# ==================== COMPOSANTS UI ====================
def render_calendar(program, user):
    st.markdown("### 📅 Programme de la semaine")
    
    week_dates = get_week_dates()
    today = date.today()
    
    cols = st.columns(7)
    
    for i, (jour_date, jour_nom) in enumerate(zip(week_dates, JOURS_SEMAINE)):
        with cols[i]:
            is_today = jour_date == today
            program_day = program.get(i, {})
            
            bg_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if is_today else "#f8f9fa"
            text_color = "white" if is_today else "#333"
            border = "3px solid #ffd700" if is_today else "1px solid #ddd"
            
            st.markdown(f"""
            <div style="background: {bg_color}; color: {text_color}; 
                        padding: 0.8rem; border-radius: 12px; text-align: center;
                        min-height: 130px; margin-bottom: 0.5rem; border: {border};">
                <div style="font-weight: 700; font-size: 0.85rem;">{jour_nom}</div>
                <div style="font-size: 0.75rem; opacity: 0.8;">{jour_date.strftime('%d/%m')}</div>
                <hr style="margin: 0.4rem 0; opacity: 0.3;">
                <div style="font-size: 0.7rem; font-weight: 600;">
                    {program_day.get('nom', 'Repos')[:25]}
                </div>
                <div style="font-size: 0.65rem; opacity: 0.9; margin-top: 4px;">
                    {program_day.get('type', '')} | {program_day.get('duree', 0)}min
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    return today.weekday()

def render_circuit_abdos(circuit, user):
    """Affiche le circuit abdos obligatoire"""
    st.markdown(f"""
    <div class="abdos-circuit">
        <h4>{circuit['nom']}</h4>
        <p style="font-size: 0.85rem; margin: 0;">{circuit['description']}</p>
        <p style="font-size: 0.85rem; margin: 0;"><b>{circuit['tours']} tours</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, ex in enumerate(circuit['exercices']):
        with cols[i % 2]:
            video_url = EXERCISE_VIDEOS.get(ex['nom'], "")
            video_btn = f'<a href="{video_url}" target="_blank" style="color: #ff4444; font-size: 0.8rem;">▶️ Vidéo</a>' if video_url else ""
            st.markdown(f"""
            <div style="background: #fff3f3; padding: 0.6rem; border-radius: 8px; margin: 0.3rem 0; border-left: 3px solid #ff6b6b;">
                <b>{ex['nom']}</b> - {ex['reps']}<br>
                <span style="font-size: 0.8rem; color: #666;">Tempo: {ex['tempo']}</span>
                {video_btn}
            </div>
            """, unsafe_allow_html=True)

def render_todays_workout(program, day_index, user, circuit_abdos):
    workout = program.get(day_index, {})
    
    st.markdown(f"### 🎯 Entraînement du jour")
    st.markdown(f"## {workout.get('nom', 'Repos')}")
    
    if workout.get('type') == 'Repos':
        st.info("💤 Jour de repos complet - Profitez-en pour récupérer !")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Type", workout.get('type', '-'))
    with col2:
        st.metric("Durée", f"{workout.get('duree', 0)} min")
    with col3:
        st.metric("Exercices", len([e for e in workout.get('exercices', []) if not e['nom'].startswith('---')]))
    with col4:
        st.metric("+ Abdos", "✅" if workout.get('circuit_abdos') else "❌")
    
    st.markdown(f"**Focus:** {workout.get('focus', '')}")
    st.markdown("---")
    
    st.markdown("#### 📝 Exercices")
    
    exercises = workout.get('exercices', [])
    performance_data = {}
    
    for i, ex in enumerate(exercises):
        # Skip les séparateurs
        if ex['nom'].startswith('---'):
            st.markdown(f"**{ex['nom']}**")
            continue
            
        with st.expander(f"▶️ {ex['nom']} | {ex['series']}x{ex['reps']} | Repos: {ex['repos']}s", expanded=(i < 3)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                - **Muscle:** {ex.get('muscle', '-')}
                - **Séries:** {ex['series']}
                - **Répétitions:** {ex['reps']}
                - **Repos:** {ex['repos']} secondes
                - **Charge de départ:** {ex['kg_depart']} kg
                """)
                
                video_url = EXERCISE_VIDEOS.get(ex['nom'])
                if video_url:
                    st.markdown(f"""
                    <a href="{video_url}" target="_blank" style="
                        display: inline-flex; align-items: center; gap: 5px;
                        background: #ff0000; color: white; padding: 10px 15px;
                        border-radius: 8px; text-decoration: none; font-size: 0.9rem;
                        font-weight: 500;">
                        ▶️ Voir la vidéo technique
                    </a>
                    """, unsafe_allow_html=True)
            
            with col2:
                if ex['kg_depart'] >= 0 and ex['series'] > 0:
                    st.markdown("**📊 Enregistrer:**")
                    kg = st.number_input("Charge (kg)", min_value=0.0, value=float(ex['kg_depart']), 
                                        step=0.5, key=f"kg_{user}_{i}")
                    reps_done = st.number_input("Reps", min_value=0, value=12, key=f"reps_{user}_{i}")
                    performance_data[ex['nom']] = {"kg": kg, "reps": reps_done}
    
    # Circuit abdos si applicable
    if workout.get('circuit_abdos'):
        st.markdown("---")
        render_circuit_abdos(circuit_abdos, user)
    
    st.markdown("---")
    
    # Enregistrement
    col1, col2 = st.columns([2, 1])
    with col1:
        feeling = st.slider("💪 Comment était la séance ?", 1, 5, 3, 
                           help="1=Très difficile, 5=Excellente forme")
    with col2:
        notes = st.text_input("📝 Notes", placeholder="Commentaires...")
    
    if st.button("✅ Séance terminée - Enregistrer", type="primary", use_container_width=True):
        for ex_name, perf in performance_data.items():
            if perf['kg'] > 0 or perf['reps'] > 0:
                add_exercise_progress(user, ex_name, perf['kg'], perf['reps'], 1)
        
        add_workout_log(user, workout['type'], workout['duree'], 
                       [ex['nom'] for ex in exercises if not ex['nom'].startswith('---')], 
                       performance_data, feeling, notes)
        st.success("🎉 Séance enregistrée ! Bravo !")
        st.balloons()

def render_progress_charts(user, target_weight, start_weight, is_loss=True):
    st.markdown("### 📈 Suivi de la progression")
    
    df = get_weight_history(user)
    
    if df.empty:
        st.info("📊 Aucune donnée enregistrée. Commencez votre suivi !")
        
        # Afficher quand même les objectifs
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Poids de départ", f"{start_weight} kg")
        with col2:
            st.metric("Objectif", f"{target_weight} kg")
        with col3:
            diff = abs(target_weight - start_weight)
            st.metric("À {'perdre' if is_loss else 'prendre'}", f"{diff} kg")
        return
    
    # Graphique principal
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Évolution du Poids', 'Tour de Ventre', 'Tour de Bras', 'Tour de Cuisses'),
        vertical_spacing=0.15
    )
    
    # Poids
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['weight'], mode='lines+markers',
                  name='Poids', line=dict(color='#667eea', width=3), marker=dict(size=8)),
        row=1, col=1
    )
    fig.add_hline(y=target_weight, line_dash="dash", line_color="green",
                 annotation_text=f"Objectif: {target_weight}kg", row=1, col=1)
    fig.add_hline(y=start_weight, line_dash="dot", line_color="red",
                 annotation_text=f"Départ: {start_weight}kg", row=1, col=1)
    
    # Tour de ventre
    if 'belly_cm' in df.columns and df['belly_cm'].notna().any():
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
    
    # Stats
    st.markdown("#### 🏆 Statistiques")
    
    col1, col2, col3, col4 = st.columns(4)
    
    first_w = df['weight'].iloc[0] if len(df) > 0 else start_weight
    last_w = df['weight'].iloc[-1] if len(df) > 0 else start_weight
    diff = last_w - first_w
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Départ</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{start_weight} kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        color = "#28a745" if (is_loss and diff < 0) or (not is_loss and diff > 0) else "#dc3545"
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Actuel</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{last_w:.1f} kg</div>
            <div style="font-size: 0.9rem; color: {color};">{diff:+.1f} kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        remaining = abs(last_w - target_weight)
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Objectif</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{target_weight} kg</div>
            <div style="font-size: 0.9rem; color: #666;">Reste: {remaining:.1f} kg</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        progress_pct = abs(diff) / abs(target_weight - start_weight) * 100 if abs(target_weight - start_weight) > 0 else 0
        progress_pct = min(progress_pct, 100)
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #666;">Progression</div>
            <div style="font-size: 1.5rem; font-weight: 700;">{progress_pct:.0f}%</div>
            <div style="font-size: 0.9rem; color: #666;">de l'objectif</div>
        </div>
        """, unsafe_allow_html=True)

def render_measurement_form(user, default_weight):
    st.markdown("### 📏 Enregistrer mes mensurations")
    
    with st.form(f"measurements_{user}"):
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("⚖️ Poids (kg)", min_value=30.0, max_value=200.0, 
                                    value=float(default_weight), step=0.1)
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

def render_exercise_performance(user, program):
    st.markdown("### 📈 Progression par exercice")
    
    # Collecter tous les exercices uniques du programme
    exercise_names = []
    for day in program.values():
        for ex in day.get('exercices', []):
            if not ex['nom'].startswith('---') and ex['nom'] not in exercise_names:
                exercise_names.append(ex['nom'])
    
    selected_ex = st.selectbox("Choisir un exercice", sorted(exercise_names))
    
    df = get_exercise_progress(user, selected_ex)
    
    if df.empty:
        st.info(f"Aucune donnée pour {selected_ex}. Enregistrez vos performances pendant vos séances !")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df, x='date', y='weight_kg', markers=True,
                     title=f"Progression de charge - {selected_ex}")
        fig.update_traces(line_color='#667eea', line_width=3, marker_size=10)
        fig.update_layout(xaxis_title="Date", yaxis_title="Charge (kg)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if len(df) >= 2:
            first = df['weight_kg'].iloc[0]
            last = df['weight_kg'].iloc[-1]
            progress = last - first
            pct = (progress / first * 100) if first > 0 else 0
            
            st.metric("Charge initiale", f"{first:.1f} kg")
            st.metric("Charge actuelle", f"{last:.1f} kg", f"{progress:+.1f} kg")
            st.metric("Progression", f"{pct:+.1f}%")
            st.metric("Nombre de séances", len(df))
        else:
            st.info("Continuez à vous entraîner pour voir votre progression !")

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
             json.dumps(["200g poulet", "100g quinoa", "Légumes", "Avocat"]),
             "Griller poulet, cuire quinoa, assembler", ""),
            ("Saumon Grillé Légumes", "Dîner", 420, 38, 20, 22,
             json.dumps(["180g saumon", "200g légumes verts", "Citron"]),
             "Griller saumon, cuire légumes vapeur", ""),
            ("Shake Récupération", "Collation", 250, 35, 20, 5,
             json.dumps(["40g whey", "300ml lait", "1 banane"]),
             "Mixer le tout", ""),
            ("Salade Protéinée", "Déjeuner", 380, 32, 15, 22,
             json.dumps(["150g thon", "2 oeufs", "Salade verte", "Tomates"]),
             "Assembler tous les ingrédients", ""),
            ("Omelette Légumes", "Petit-déjeuner", 320, 25, 8, 22,
             json.dumps(["3 oeufs", "Poivrons", "Champignons"]),
             "Battre oeufs, cuire avec légumes", ""),
        ]
        c.executemany("INSERT INTO recipes (name, category, calories, protein, carbs, fat, ingredients, instructions, image_url) VALUES (?,?,?,?,?,?,?,?,?)", recipes)
        conn.commit()

init_recipes()

def render_nutrition_section():
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
        st.markdown("### Calculateur de besoins caloriques")
        
        col1, col2 = st.columns(2)
        with col1:
            user = st.selectbox("Profil", ["Luca", "Sonia"])
            activity = st.select_slider("Niveau d'activité", ["Sédentaire", "Léger", "Modéré", "Actif", "Très actif"])
        
        activity_mult = {"Sédentaire": 1.2, "Léger": 1.375, "Modéré": 1.55, "Actif": 1.725, "Très actif": 1.9}
        
        if user == "Luca":
            bmr = 10 * 88 + 6.25 * 195 - 5 * 30 + 5
            target_cal = bmr * activity_mult[activity] + 200  # Léger surplus
            protein = 88 * 2  # 2g/kg
        else:
            bmr = 10 * 78 + 6.25 * 150 - 5 * 30 - 161
            target_cal = bmr * activity_mult[activity] - 500  # Déficit
            protein = 78 * 1.8  # 1.8g/kg
        
        with col2:
            st.metric("Calories/jour", f"{target_cal:.0f} kcal")
            st.metric("Protéines", f"{protein:.0f}g")
            st.metric("Glucides", f"{target_cal * 0.4 / 4:.0f}g")
            st.metric("Lipides", f"{target_cal * 0.3 / 9:.0f}g")
    
    else:
        st.markdown("### Plans alimentaires")
        user = st.selectbox("Profil", ["Luca", "Sonia"], key="plan_user")
        
        if user == "Luca":
            st.markdown("#### Plan Prise de masse sèche (~2300 kcal)")
            plan = {
                "7h - Petit-déj": "Porridge protéiné + banane (380 kcal)",
                "10h - Collation": "Shake protéiné (250 kcal)",
                "12h30 - Déjeuner": "Poulet + riz + légumes (550 kcal)",
                "16h - Collation": "Yaourt grec + amandes (200 kcal)",
                "19h30 - Dîner": "Saumon + patate douce (500 kcal)",
                "Post-training": "Shake (250 kcal)"
            }
        else:
            st.markdown("#### Plan Perte de poids (~1400 kcal)")
            plan = {
                "8h - Petit-déj": "Omelette 2 oeufs + pain complet (280 kcal)",
                "10h30 - Collation": "Yaourt 0% + fruits (120 kcal)",
                "12h30 - Déjeuner": "Salade protéinée (380 kcal)",
                "16h - Collation": "Poignée d'amandes (100 kcal)",
                "19h - Dîner": "Poisson + légumes vapeur (350 kcal)"
            }
        
        for meal, content in plan.items():
            st.markdown(f"**{meal}:** {content}")

# ==================== MAIN APP ====================
st.markdown('<div class="main-header">💪 FitCouple - Luca & Sonia</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🥗 NUTRITION"])

with tab1:
    st.markdown("""<div class="profile-card">
    <h3>👤 Profil de Luca</h3>
    <p><b>Objectif:</b> Prise de masse sèche + Perte de ventre + Développement Bras/Dos/Abdos</p>
    <p><b>Poids:</b> 88 kg → 90 kg | <b>Taille:</b> 1m95 | <b>IMC:</b> 23.1</p>
    <p><b>Équipement:</b> Tapis + Haltères | <b>Circuit Abdos:</b> OBLIGATOIRE à chaque séance</p>
    </div>""", unsafe_allow_html=True)
    
    luca_tab = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression", "🏆 Performances"], 
                        horizontal=True, key="luca_nav")
    
    if luca_tab == "📅 Programme":
        day_idx = render_calendar(PROGRAM_LUCA, "Luca")
        st.markdown("---")
        render_todays_workout(PROGRAM_LUCA, day_idx, "Luca", CIRCUIT_ABDOS_LUCA)
    elif luca_tab == "📏 Mensurations":
        render_measurement_form("Luca", 88)
    elif luca_tab == "📈 Progression":
        render_progress_charts("Luca", target_weight=90, start_weight=88, is_loss=False)
    else:
        render_exercise_performance("Luca", PROGRAM_LUCA)

with tab2:
    st.markdown("""<div class="profile-card">
    <h3>👤 Profil de Sonia</h3>
    <p><b>Objectif:</b> Perte de poids (-10 à 15 kg) + Tonification Ventre/Bras/Cuisses + Renforcement Fessiers</p>
    <p><b>Poids:</b> 78 kg → 63-68 kg | <b>Taille:</b> 1m50 | <b>IMC:</b> 34.7</p>
    <p><b>Équipement:</b> Tapis + Haltères</p>
    </div>""", unsafe_allow_html=True)
    
    sonia_tab = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression", "🏆 Performances"], 
                         horizontal=True, key="sonia_nav")
    
    if sonia_tab == "📅 Programme":
        day_idx = render_calendar(PROGRAM_SONIA, "Sonia")
        st.markdown("---")
        render_todays_workout(PROGRAM_SONIA, day_idx, "Sonia", CIRCUIT_ABDOS_SONIA)
    elif sonia_tab == "📏 Mensurations":
        render_measurement_form("Sonia", 78)
    elif sonia_tab == "📈 Progression":
        render_progress_charts("Sonia", target_weight=65, start_weight=78, is_loss=True)
    else:
        render_exercise_performance("Sonia", PROGRAM_SONIA)

with tab3:
    render_nutrition_section()

st.markdown("""<div style="text-align: center; padding: 2rem; color: #666; font-size: 0.85rem;">
    💪 FitCouple App v2.0 | Entraînement Maison | 
    <em>La régularité bat l'intensité !</em>
</div>""", unsafe_allow_html=True)
