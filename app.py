import streamlit as st
import pandas as pd
from datetime import date
import plotly.graph_objects as go

st.set_page_config(
    page_title="FitCouple",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Pro Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

* { font-family: 'Poppins', sans-serif; }

.main-header {
    font-size: 2.5rem; font-weight: 700; text-align: center; padding: 2rem;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    color: white; border-radius: 20px; margin-bottom: 2rem;
    box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
}

.profile-card {
    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    color: white; padding: 1.5rem; border-radius: 16px;
    margin-bottom: 1.5rem;
}

/* EXERCISE CARDS */
.exercise-card-new {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 20px; padding: 0; margin: 1rem 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(99, 102, 241, 0.1);
    overflow: hidden; transition: all 0.3s ease;
}
.exercise-card-new:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(99, 102, 241, 0.15);
}

.exercise-video-container {
    position: relative; width: 100%; height: 200px; overflow: hidden;
}
.exercise-video-container img {
    width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;
}
.exercise-card-new:hover .exercise-video-container img { transform: scale(1.05); }
.play-button {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 70px; height: 70px; background: rgba(255,255,255,0.95);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: all 0.3s ease;
}
.exercise-card-new:hover .play-button {
    transform: translate(-50%, -50%) scale(1.1); background: #6366f1; color: white;
}

.exercise-info { padding: 1.2rem; }
.exercise-title { font-size: 1.1rem; font-weight: 700; color: #1e1e2e; margin: 0 0 0.5rem 0; }
.exercise-sets {
    display: inline-block; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white; padding: 0.4rem 1rem; border-radius: 25px;
    font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;
}
.exercise-muscle {
    display: inline-block; background: #f1f5f9; color: #64748b;
    padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem;
    font-weight: 500; margin-left: 0.5rem;
}
.exercise-desc { color: #64748b; font-size: 0.85rem; margin-top: 0.5rem; }

.exercise-icon-box {
    width: 100%; height: 150px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    display: flex; align-items: center; justify-content: center; font-size: 4rem;
}

/* MEAL CALENDAR */
.meal-day-header {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white; padding: 1rem; border-radius: 12px 12px 0 0;
    font-weight: 700; font-size: 1.1rem; text-align: center;
}
.meal-day-content {
    background: white; border: 1px solid #e2e8f0; border-top: none;
    border-radius: 0 0 12px 12px; padding: 1rem;
}
.meal-item {
    padding: 0.8rem; margin: 0.5rem 0; border-radius: 10px;
    border-left: 4px solid #6366f1; background: #f8fafc;
}
.meal-item-title { font-weight: 600; color: #1e1e2e; font-size: 0.85rem; }
.meal-item-food { color: #64748b; font-size: 0.8rem; margin-top: 0.3rem; }
.meal-item-kcal { 
    display: inline-block; background: #fef3c7; color: #d97706;
    padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.7rem; font-weight: 600;
}

.day-card {
    padding: 0.8rem; border-radius: 12px; text-align: center;
    margin: 0.2rem; min-height: 80px; transition: all 0.2s; cursor: pointer;
}
.day-today {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white; transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}
.day-selected {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    color: white; transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4);
}
.day-normal { background: #f8fafc; color: #334155; border: 1px solid #e2e8f0; }
.day-abdos { border: 2px solid #f97316; }

.abdos-banner {
    background: linear-gradient(135deg, #f97316 0%, #ef4444 100%);
    color: white; padding: 1.2rem; border-radius: 16px;
    margin: 1.5rem 0; text-align: center;
}

.nutrition-header-luca {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white; padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;
}
.nutrition-header-sonia {
    background: linear-gradient(135deg, #be185d 0%, #ec4899 100%);
    color: white; padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;
}

.recipe-card {
    background: white; border-radius: 20px; overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 1rem 0;
    transition: transform 0.2s;
}
.recipe-card:hover { transform: translateY(-5px); }
.recipe-img { width: 100%; height: 180px; object-fit: cover; }
.recipe-content { padding: 1rem; }
.recipe-video-btn {
    display: inline-block; background: #ef4444; color: white !important;
    padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none;
    font-weight: 600; font-size: 0.85rem; margin-top: 0.5rem;
}

.macro-badge {
    display: inline-block; padding: 0.3rem 0.6rem;
    border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin: 0.1rem;
}
.macro-cal { background: #fef3c7; color: #d97706; }
.macro-prot { background: #dbeafe; color: #2563eb; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: #f1f5f9; padding: 8px; border-radius: 16px;
}
.stTabs [data-baseweb="tab"] { padding: 12px 24px; border-radius: 12px; font-weight: 600; }
.stTabs [aria-selected="true"] { background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# Session state
if 'weight_luca' not in st.session_state:
    st.session_state.weight_luca = []
if 'weight_sonia' not in st.session_state:
    st.session_state.weight_sonia = []

# ==================== EXERCICES ====================
EXERCICES = {
    "Pompes classiques": {"video": "IODxDxX7oi4", "muscle": "Pectoraux", "desc": "Le basique pour des pecs en béton", "icon": "💪"},
    "Pompes inclinées": {"video": "cfns5VDVVvk", "muscle": "Haut des pecs", "desc": "Cible le haut de la poitrine", "icon": "💪"},
    "Pompes serrées": {"video": "J0DnG1_S92I", "muscle": "Triceps", "desc": "Focus triceps", "icon": "💪"},
    "Pike push-ups": {"video": "sposDXWEB0A", "muscle": "Épaules", "desc": "Excellent pour les épaules", "icon": "🏋️"},
    "Dips sur chaise": {"video": "0326dy_-CzM", "muscle": "Triceps", "desc": "Triceps avec une chaise", "icon": "🪑"},
    "Développé haltères": {"video": "VmB1G1K7v94", "muscle": "Épaules", "desc": "Masse pour les épaules", "icon": "🏋️"},
    "Élévations latérales": {"video": "3VcKaXpzqRo", "muscle": "Épaules", "desc": "Épaules larges", "icon": "🏋️"},
    "Extension triceps": {"video": "nRiJVZDpdL0", "muscle": "Triceps", "desc": "Isolation triceps", "icon": "💪"},
    "Rowing haltère": {"video": "roCP6wCXPqo", "muscle": "Dos", "desc": "Dos épais", "icon": "🔙"},
    "Superman": {"video": "z6PJMT2y8GQ", "muscle": "Lombaires", "desc": "Renforce le bas du dos", "icon": "🦸"},
    "Oiseau": {"video": "EA7u4Q_8HQ0", "muscle": "Arrière épaule", "desc": "Arrière d'épaule", "icon": "🐦"},
    "Curl biceps": {"video": "ykJmrZ5v0Oo", "muscle": "Biceps", "desc": "Gros biceps", "icon": "💪"},
    "Curl marteau": {"video": "zC3nLlEvin4", "muscle": "Biceps", "desc": "Biceps + avant-bras", "icon": "🔨"},
    "Squats": {"video": "YaXPRqUwItQ", "muscle": "Quadriceps", "desc": "Le roi des jambes", "icon": "🦵"},
    "Squats sumo": {"video": "9ZuXKqRbT9k", "muscle": "Adducteurs", "desc": "Intérieur cuisses", "icon": "🦵"},
    "Fentes": {"video": "QOVaHwm-Q6U", "muscle": "Quadriceps/Fessiers", "desc": "Jambes sculptées", "icon": "🦵"},
    "Hip thrust": {"video": "SEdqd1n0cvg", "muscle": "Fessiers", "desc": "Meilleur exo fessiers", "icon": "🍑"},
    "Glute bridge": {"video": "OUgsJ8-Vi0E", "muscle": "Fessiers", "desc": "Activation fessiers", "icon": "🍑"},
    "Donkey kicks": {"video": "SJ1Xuz9D-ZQ", "muscle": "Fessiers", "desc": "Galbe fessiers", "icon": "🍑"},
    "Fire hydrants": {"video": "La3xrTxLXSE", "muscle": "Fessiers", "desc": "Fessiers latéraux", "icon": "🔥"},
    "Jumping jacks": {"video": "c4DAnQ6DtF8", "muscle": "Cardio", "desc": "Échauffement", "icon": "⭐"},
    "Burpees": {"video": "TU8QYVW0gDU", "muscle": "Full body", "desc": "Brûleur de calories", "icon": "🔥"},
    "High knees": {"video": "D0bLJnSBNI8", "muscle": "Cardio", "desc": "Cardio intense", "icon": "🏃"},
    "Squat jumps": {"video": "A-cFYWvaHr0", "muscle": "Jambes/Cardio", "desc": "Explosivité", "icon": "🦘"},
    "Mountain climbers": {"video": "nmwgirgXLYM", "muscle": "Core/Cardio", "desc": "Abdos + cardio", "icon": "⛰️"},
    "Gainage (Planche)": {"video": "ASdvN_XEl_c", "muscle": "Core", "desc": "Core solide", "icon": "🧘"},
    "Gainage latéral": {"video": "K2VljzCC16g", "muscle": "Obliques", "desc": "Obliques", "icon": "🧘"},
    "Crunch": {"video": "Xyd_fa5zoEU", "muscle": "Abdos", "desc": "Le classique", "icon": "🔥"},
    "Russian twist": {"video": "wkD8rjkodUI", "muscle": "Obliques", "desc": "Taille fine", "icon": "🌀"},
    "Scissor kicks": {"video": "WoNCIBVLbgY", "muscle": "Bas abdos", "desc": "Bas du ventre", "icon": "✂️"},
    "V-ups": {"video": "iP2fjvG0g3w", "muscle": "Abdos", "desc": "Abdos intense", "icon": "🔥"},
    "Bicycle crunch": {"video": "9FGilxCbdz8", "muscle": "Obliques", "desc": "Abdos + obliques", "icon": "🚴"},
    "Marche/Vélo léger": {"video": "", "muscle": "Cardio léger", "desc": "Récupération active", "icon": "🚶"},
    "Marche rapide/Vélo": {"video": "", "muscle": "Cardio", "desc": "Cardio modéré", "icon": "🚴"},
    "Vélo ou Course": {"video": "", "muscle": "Cardio", "desc": "Endurance", "icon": "🏃"},
    "Étirements": {"video": "", "muscle": "Flexibilité", "desc": "Récupération", "icon": "🧘"},
}

# ==================== CALENDRIER REPAS LUCA (Prise de masse ~2500 kcal) ====================
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

MENU_LUCA = {
    0: {  # Lundi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "3 oeufs brouillés + 2 tranches pain complet + 1 banane + café", "kcal": 550},
        "dejeuner": {"nom": "Déjeuner", "plat": "200g poulet grillé + 150g riz + haricots verts + huile d'olive", "kcal": 650},
        "collation": {"nom": "Collation", "plat": "Shake: 40g whey + lait + 1 banane + beurre de cacahuète", "kcal": 450},
        "diner": {"nom": "Dîner", "plat": "200g saumon + 200g patate douce + brocoli", "kcal": 580},
    },
    1: {  # Mardi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "100g flocons avoine + lait + 30g whey + fruits rouges", "kcal": 520},
        "dejeuner": {"nom": "Déjeuner", "plat": "200g steak haché 5% + 150g pâtes complètes + sauce tomate", "kcal": 680},
        "collation": {"nom": "Collation", "plat": "250g fromage blanc + 30g amandes + miel", "kcal": 380},
        "diner": {"nom": "Dîner", "plat": "2 filets de poulet + quinoa 150g + légumes grillés", "kcal": 550},
    },
    2: {  # Mercredi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "Omelette 4 oeufs + fromage + 2 tranches pain complet", "kcal": 580},
        "dejeuner": {"nom": "Déjeuner", "plat": "Wrap: 2 tortillas + 180g poulet + avocat + crudités", "kcal": 650},
        "collation": {"nom": "Collation", "plat": "2 bananes + 40g beurre de cacahuète", "kcal": 420},
        "diner": {"nom": "Dîner", "plat": "220g cabillaud + riz 150g + épinards", "kcal": 520},
    },
    3: {  # Jeudi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "3 oeufs au plat + 2 tranches bacon + pain complet", "kcal": 560},
        "dejeuner": {"nom": "Déjeuner", "plat": "Buddha bowl: 180g poulet + quinoa + pois chiches + avocat", "kcal": 680},
        "collation": {"nom": "Collation", "plat": "Shake protéiné + 1 poignée noix de cajou", "kcal": 400},
        "diner": {"nom": "Dîner", "plat": "Curry poulet 200g + riz basmati 150g + lait coco", "kcal": 620},
    },
    4: {  # Vendredi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "Porridge 80g avoine + whey + banane + beurre cacahuète", "kcal": 580},
        "dejeuner": {"nom": "Déjeuner", "plat": "Poke bowl: 180g saumon + riz + avocat + edamame", "kcal": 650},
        "collation": {"nom": "Collation", "plat": "300g yaourt grec + granola + fruits", "kcal": 380},
        "diner": {"nom": "Dîner", "plat": "Pâtes bolognaise: 150g pâtes + 200g viande hachée", "kcal": 650},
    },
    5: {  # Samedi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "4 oeufs brouillés + avocat + 2 toasts + jus d'orange", "kcal": 620},
        "dejeuner": {"nom": "Déjeuner", "plat": "Burger maison: steak 180g + pain complet + frites patate douce", "kcal": 750},
        "collation": {"nom": "Collation", "plat": "Smoothie: lait + whey + flocons avoine + banane", "kcal": 450},
        "diner": {"nom": "Dîner", "plat": "Entrecôte 200g + purée maison + haricots verts", "kcal": 650},
    },
    6: {  # Dimanche
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "Omelette complète: 4 oeufs + jambon + fromage + pain", "kcal": 600},
        "dejeuner": {"nom": "Déjeuner", "plat": "Poulet rôti 250g + pommes de terre + légumes rôtis", "kcal": 700},
        "collation": {"nom": "Collation", "plat": "Fromage blanc 250g + miel + amandes", "kcal": 350},
        "diner": {"nom": "Dîner", "plat": "Saumon teriyaki 200g + riz + légumes sautés", "kcal": 580},
    },
}

# ==================== CALENDRIER REPAS SONIA (Perte de poids ~1300-1400 kcal) ====================
MENU_SONIA = {
    0: {  # Lundi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "2 oeufs durs + 1 tranche pain complet + thé vert", "kcal": 280},
        "dejeuner": {"nom": "Déjeuner", "plat": "Salade: 120g poulet grillé + quinoa 50g + légumes + vinaigrette légère", "kcal": 380},
        "collation": {"nom": "Collation", "plat": "1 pomme + 10 amandes", "kcal": 150},
        "diner": {"nom": "Dîner", "plat": "150g poisson blanc + courgettes grillées + citron (SANS féculents)", "kcal": 280},
    },
    1: {  # Mardi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "150g yaourt grec 0% + 30g flocons avoine + fruits rouges", "kcal": 250},
        "dejeuner": {"nom": "Déjeuner", "plat": "Wrap léger: 1 tortilla + 100g dinde + crudités + sauce yaourt", "kcal": 350},
        "collation": {"nom": "Collation", "plat": "1 banane", "kcal": 100},
        "diner": {"nom": "Dîner", "plat": "Soupe de légumes maison + 1 oeuf poché + salade verte", "kcal": 250},
    },
    2: {  # Mercredi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "1 oeuf + 1 blanc d'oeuf brouillés + 1/2 avocat + café", "kcal": 280},
        "dejeuner": {"nom": "Déjeuner", "plat": "Salade niçoise: thon 100g + haricots verts + oeuf + olives", "kcal": 400},
        "collation": {"nom": "Collation", "plat": "100g fromage blanc 0% + cannelle", "kcal": 80},
        "diner": {"nom": "Dîner", "plat": "Blanc de poulet 130g + ratatouille maison (SANS féculents)", "kcal": 300},
    },
    3: {  # Jeudi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "Smoothie: lait amande + 20g whey + épinards + 1/2 banane", "kcal": 220},
        "dejeuner": {"nom": "Déjeuner", "plat": "Bol: 100g crevettes + riz 60g + concombre + sauce soja", "kcal": 350},
        "collation": {"nom": "Collation", "plat": "Bâtonnets de carottes + houmous 30g", "kcal": 120},
        "diner": {"nom": "Dîner", "plat": "Papillote saumon 130g + brocoli + citron (SANS féculents)", "kcal": 320},
    },
    4: {  # Vendredi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "2 tranches pain complet + 1 oeuf poché + tomate", "kcal": 270},
        "dejeuner": {"nom": "Déjeuner", "plat": "Salade César light: 120g poulet + salade + parmesan + sauce légère", "kcal": 380},
        "collation": {"nom": "Collation", "plat": "150g yaourt grec 0% nature", "kcal": 90},
        "diner": {"nom": "Dîner", "plat": "Wok crevettes 150g + légumes (brocoli, poivrons, champignons)", "kcal": 280},
    },
    5: {  # Samedi
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "Omelette 2 oeufs + épinards + feta + thé", "kcal": 300},
        "dejeuner": {"nom": "Déjeuner", "plat": "Poke bowl light: 100g saumon + riz 50g + avocat 1/4 + edamame", "kcal": 400},
        "collation": {"nom": "Collation", "plat": "1 poire + quelques noix", "kcal": 130},
        "diner": {"nom": "Dîner", "plat": "Filet de poulet 130g + salade composée + vinaigrette maison", "kcal": 280},
    },
    6: {  # Dimanche (repas plaisir modéré)
        "petit_dej": {"nom": "Petit-déjeuner", "plat": "2 oeufs brouillés + 1 tranche pain complet + 1/2 avocat", "kcal": 350},
        "dejeuner": {"nom": "Déjeuner", "plat": "Poulet grillé 150g + légumes rôtis + 1 petite portion riz", "kcal": 450},
        "collation": {"nom": "Collation", "plat": "2 carrés chocolat noir 70% + thé", "kcal": 100},
        "diner": {"nom": "Dîner", "plat": "Soupe légumes + salade de tomates mozzarella (portion légère)", "kcal": 300},
    },
}

# ==================== PROGRAMMES SPORT ====================
PROGRAM_LUCA = {
    0: {"nom": "PUSH", "emoji": "💪", "type": "Pecs/Épaules/Triceps", "duree": 50, "abdos": True,
        "exercices": [
            ("Pompes classiques", "4 x 12-15"),
            ("Pompes inclinées", "3 x 12"),
            ("Pike push-ups", "3 x 10"),
            ("Développé haltères", "3 x 12"),
            ("Élévations latérales", "3 x 15"),
            ("Pompes serrées", "3 x 12"),
            ("Dips sur chaise", "3 x 12"),
        ]},
    1: {"nom": "PULL", "emoji": "🔙", "type": "Dos/Biceps", "duree": 45, "abdos": False,
        "exercices": [
            ("Rowing haltère", "4 x 10-12/bras"),
            ("Superman", "3 x 15"),
            ("Oiseau", "3 x 15"),
            ("Curl biceps", "4 x 12"),
            ("Curl marteau", "3 x 12"),
        ]},
    2: {"nom": "LEGS + HIIT", "emoji": "🦵", "type": "Jambes/Cardio", "duree": 55, "abdos": True,
        "exercices": [
            ("Squats", "4 x 15"),
            ("Squats sumo", "3 x 15"),
            ("Fentes", "3 x 12/jambe"),
            ("Jumping jacks", "3 x 45sec"),
            ("High knees", "3 x 45sec"),
            ("Burpees", "3 x 10"),
        ]},
    3: {"nom": "REPOS", "emoji": "💤", "type": "Récupération", "duree": 30, "abdos": False,
        "exercices": [("Marche/Vélo léger", "20-30 min"), ("Étirements", "10 min")]},
    4: {"nom": "FULL BODY", "emoji": "🔥", "type": "Complet", "duree": 55, "abdos": True,
        "exercices": [
            ("Squats", "4 x 12"),
            ("Pompes classiques", "4 x 15"),
            ("Rowing haltère", "4 x 12/bras"),
            ("Fentes", "3 x 10/jambe"),
            ("Développé haltères", "3 x 12"),
            ("Curl biceps", "3 x 12"),
        ]},
    5: {"nom": "CARDIO", "emoji": "🏃", "type": "Endurance", "duree": 40, "abdos": False,
        "exercices": [("Vélo ou Course", "30-40 min")]},
    6: {"nom": "REPOS", "emoji": "💤", "type": "Repos complet", "duree": 0, "abdos": False, "exercices": []},
}

PROGRAM_SONIA = {
    0: {"nom": "BAS DU CORPS", "emoji": "🍑", "type": "Fessiers/Cuisses", "duree": 45, "abdos": True,
        "exercices": [
            ("Squats", "4 x 15"),
            ("Hip thrust", "4 x 15"),
            ("Fentes", "3 x 12/jambe"),
            ("Glute bridge", "3 x 20"),
            ("Donkey kicks", "3 x 20/côté"),
            ("Fire hydrants", "3 x 20/côté"),
        ]},
    1: {"nom": "HIIT", "emoji": "🔥", "type": "Cardio Brûle-graisse", "duree": 30, "abdos": False,
        "exercices": [
            ("Jumping jacks", "4 x 30sec"),
            ("Squat jumps", "4 x 30sec"),
            ("Mountain climbers", "4 x 30sec"),
            ("Burpees", "4 x 30sec"),
            ("High knees", "4 x 30sec"),
        ]},
    2: {"nom": "HAUT + CORE", "emoji": "💪", "type": "Bras/Abdos", "duree": 40, "abdos": True,
        "exercices": [
            ("Pompes classiques", "3 x 12"),
            ("Rowing haltère", "3 x 12/bras"),
            ("Élévations latérales", "3 x 15"),
            ("Curl biceps", "3 x 15"),
            ("Dips sur chaise", "3 x 10"),
        ]},
    3: {"nom": "CARDIO", "emoji": "🚶", "type": "Modéré", "duree": 40, "abdos": False,
        "exercices": [("Marche rapide/Vélo", "35 min"), ("Étirements", "10 min")]},
    4: {"nom": "CIRCUIT", "emoji": "🔄", "type": "Full Body", "duree": 40, "abdos": True,
        "exercices": [
            ("Squats", "3 x 15"),
            ("Pompes classiques", "3 x 10"),
            ("Fentes", "3 x 10/jambe"),
            ("Rowing haltère", "3 x 10/bras"),
            ("Glute bridge", "3 x 15"),
        ]},
    5: {"nom": "FESSIERS", "emoji": "🍑", "type": "Focus Fessiers", "duree": 40, "abdos": False,
        "exercices": [
            ("Hip thrust", "4 x 20"),
            ("Squats sumo", "4 x 15"),
            ("Donkey kicks", "4 x 20/côté"),
            ("Fire hydrants", "4 x 20/côté"),
            ("Glute bridge", "50 reps"),
        ]},
    6: {"nom": "REPOS", "emoji": "🧘", "type": "Yoga/Étirements", "duree": 30, "abdos": False, "exercices": []},
}

CIRCUIT_ABDOS = [
    ("Gainage (Planche)", "45 sec"),
    ("Gainage latéral", "30 sec/côté"),
    ("Russian twist", "20 reps"),
    ("Scissor kicks", "20 reps"),
    ("V-ups", "15 reps"),
    ("Crunch", "20 reps"),
    ("Bicycle crunch", "20 reps"),
]

# ==================== FONCTIONS ====================
def render_calendar(program, user_key):
    today_idx = date.today().weekday()
    
    selected_day = st.selectbox(
        "📅 Choisir le jour",
        options=list(range(7)),
        format_func=lambda x: f"{'👉 ' if x == today_idx else ''}{JOURS[x]} - {program.get(x, {}).get('nom', 'Repos')}",
        index=today_idx,
        key=f"day_select_{user_key}"
    )
    
    cols = st.columns(7)
    for i, jour in enumerate(JOURS):
        with cols[i]:
            p = program.get(i, {})
            is_today = (i == today_idx)
            is_selected = (i == selected_day)
            has_abdos = p.get('abdos', False)
            
            if is_selected and is_today:
                css = "day-today"
            elif is_selected:
                css = "day-selected"
            else:
                css = "day-normal"
            
            if has_abdos and not is_selected:
                css += " day-abdos"
            
            emoji = p.get('emoji', '')
            marker = "✓" if is_selected else ""
            
            st.markdown(f"""
            <div class="day-card {css}">
                <div style="font-size: 1.3rem;">{emoji}</div>
                <b>{jour[:3]}</b><br>
                <small>{p.get('nom', 'Repos')[:8]}</small>
                <div style="font-size: 0.8rem;">{marker}</div>
            </div>
            """, unsafe_allow_html=True)
    
    return selected_day

def render_exercise_card_new(nom, sets):
    ex = EXERCICES.get(nom, {"video": "", "muscle": "", "desc": "", "icon": "🏋️"})
    video_id = ex.get('video', '')
    muscle = ex.get('muscle', '')
    desc = ex.get('desc', '')
    icon = ex.get('icon', '🏋️')
    
    if not video_id:
        st.markdown(f"""
        <div class="exercise-card-new">
            <div class="exercise-icon-box">{icon}</div>
            <div class="exercise-info">
                <div class="exercise-title">{nom}</div>
                <span class="exercise-sets">{sets}</span>
                <span class="exercise-muscle">{muscle}</span>
                <div class="exercise-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    link = f"https://youtube.com/watch?v={video_id}"
    
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration: none;">
        <div class="exercise-card-new">
            <div class="exercise-video-container">
                <img src="{thumb}" alt="{nom}">
                <div class="play-button">▶</div>
            </div>
            <div class="exercise-info">
                <div class="exercise-title">{nom}</div>
                <span class="exercise-sets">{sets}</span>
                <span class="exercise-muscle">{muscle}</span>
                <div class="exercise-desc">{desc}</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

def render_workout(program, day_idx, user_key):
    workout = program.get(day_idx, {})
    
    st.markdown(f"## {workout.get('emoji', '')} {workout.get('nom', 'REPOS')}")
    st.markdown(f"**{workout.get('type', '')}** • {workout.get('duree', 0)} minutes")
    
    if not workout.get('exercices'):
        st.success("💤 Jour de repos ! Profitez-en pour récupérer.")
        return
    
    st.markdown("---")
    
    exercices = workout.get('exercices', [])
    for i in range(0, len(exercices), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(exercices):
                nom, sets = exercices[i + j]
                with col:
                    render_exercise_card_new(nom, sets)
    
    if workout.get('abdos'):
        st.markdown("""<div class="abdos-banner">
            <h3 style="margin: 0;">🔥 CIRCUIT ABDOS</h3>
            <p style="margin: 0.5rem 0 0 0;">2 tours • 30 sec repos entre les tours</p>
        </div>""", unsafe_allow_html=True)
        
        for i in range(0, len(CIRCUIT_ABDOS), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(CIRCUIT_ABDOS):
                    nom, reps = CIRCUIT_ABDOS[i + j]
                    with col:
                        render_exercise_card_new(nom, reps)
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.slider("Comment était ta séance ?", 1, 5, 3, key=f"feel_{user_key}_{day_idx}")
    with col2:
        if st.button("✅ Terminé !", key=f"btn_{user_key}_{day_idx}", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Bravo !")

def render_meal_calendar_luca():
    st.markdown("""
    <div class="nutrition-header-luca">
        <h2 style="margin: 0;">🏋️ PLANNING REPAS LUCA</h2>
        <p style="margin: 0.5rem 0 0 0;">Prise de masse • ~2500 kcal/jour • Protéines élevées</p>
    </div>
    """, unsafe_allow_html=True)
    
    today_idx = date.today().weekday()
    
    # Sélecteur de jour
    selected_day = st.selectbox(
        "📅 Voir le menu du jour",
        options=list(range(7)),
        format_func=lambda x: f"{'👉 Aujourd'hui - ' if x == today_idx else ''}{JOURS[x]}",
        index=today_idx,
        key="meal_day_luca"
    )
    
    menu = MENU_LUCA[selected_day]
    
    st.markdown(f"""
    <div class="meal-day-header">📆 {JOURS[selected_day]}</div>
    <div class="meal-day-content">
    """, unsafe_allow_html=True)
    
    total_kcal = 0
    for key in ["petit_dej", "dejeuner", "collation", "diner"]:
        meal = menu[key]
        total_kcal += meal["kcal"]
        st.markdown(f"""
        <div class="meal-item">
            <div class="meal-item-title">🍽️ {meal['nom']}</div>
            <div class="meal-item-food">{meal['plat']}</div>
            <span class="meal-item-kcal">{meal['kcal']} kcal</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Total journée
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
                color: white; padding: 1.5rem; border-radius: 16px; text-align: center; margin-top: 1rem;">
        <h3 style="margin: 0;">📊 TOTAL JOURNÉE</h3>
        <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: 700;">{total_kcal} kcal</p>
        <p style="margin: 0; opacity: 0.9;">Objectif: ~2500 kcal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Vue semaine complète
    with st.expander("📅 Voir toute la semaine"):
        for day_idx in range(7):
            menu = MENU_LUCA[day_idx]
            total = sum(menu[k]["kcal"] for k in ["petit_dej", "dejeuner", "collation", "diner"])
            st.markdown(f"**{JOURS[day_idx]}** - {total} kcal")
            for key in ["petit_dej", "dejeuner", "collation", "diner"]:
                st.caption(f"  • {menu[key]['nom']}: {menu[key]['plat']}")
            st.markdown("---")

def render_meal_calendar_sonia():
    st.markdown("""
    <div class="nutrition-header-sonia">
        <h2 style="margin: 0;">🧘 PLANNING REPAS SONIA</h2>
        <p style="margin: 0.5rem 0 0 0;">Perte de poids • ~1300-1400 kcal/jour • Peu de féculents le soir</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Règle d'or**: Pas de féculents le soir pour maximiser la perte de poids !")
    
    today_idx = date.today().weekday()
    
    selected_day = st.selectbox(
        "📅 Voir le menu du jour",
        options=list(range(7)),
        format_func=lambda x: f"{'👉 Aujourd'hui - ' if x == today_idx else ''}{JOURS[x]}",
        index=today_idx,
        key="meal_day_sonia"
    )
    
    menu = MENU_SONIA[selected_day]
    
    st.markdown(f"""
    <div class="meal-day-header" style="background: linear-gradient(135deg, #be185d 0%, #ec4899 100%);">
        📆 {JOURS[selected_day]}
    </div>
    <div class="meal-day-content">
    """, unsafe_allow_html=True)
    
    total_kcal = 0
    for key in ["petit_dej", "dejeuner", "collation", "diner"]:
        meal = menu[key]
        total_kcal += meal["kcal"]
        st.markdown(f"""
        <div class="meal-item" style="border-left-color: #ec4899;">
            <div class="meal-item-title">🍽️ {meal['nom']}</div>
            <div class="meal-item-food">{meal['plat']}</div>
            <span class="meal-item-kcal">{meal['kcal']} kcal</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Total journée
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #be185d 0%, #ec4899 100%);
                color: white; padding: 1.5rem; border-radius: 16px; text-align: center; margin-top: 1rem;">
        <h3 style="margin: 0;">📊 TOTAL JOURNÉE</h3>
        <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: 700;">{total_kcal} kcal</p>
        <p style="margin: 0; opacity: 0.9;">Objectif: ~1300-1400 kcal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Conseils
    st.markdown("### 💡 Conseils pour Sonia")
    st.markdown("""
    - ✅ **Boire 2L d'eau** par jour minimum
    - ✅ **Pas de grignotage** entre les repas
    - ✅ **Manger lentement** (20 min minimum)
    - ✅ **Légumes à volonté** (sauf féculents)
    - ❌ **Éviter**: sucre, alcool, pain blanc, fritures
    """)
    
    # Vue semaine complète
    with st.expander("📅 Voir toute la semaine"):
        for day_idx in range(7):
            menu = MENU_SONIA[day_idx]
            total = sum(menu[k]["kcal"] for k in ["petit_dej", "dejeuner", "collation", "diner"])
            st.markdown(f"**{JOURS[day_idx]}** - {total} kcal")
            for key in ["petit_dej", "dejeuner", "collation", "diner"]:
                st.caption(f"  • {menu[key]['nom']}: {menu[key]['plat']}")
            st.markdown("---")

def render_measurements(user_key, default_weight):
    st.markdown("### 📏 Suivi")
    
    with st.form(key=f"form_{user_key}"):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Poids (kg)", 30.0, 200.0, float(default_weight), 0.1)
            belly = st.number_input("Tour de ventre (cm)", 50.0, 150.0, 90.0, 0.5)
        with col2:
            arms = st.number_input("Tour de bras (cm)", 20.0, 60.0, 35.0, 0.5)
            thighs = st.number_input("Tour de cuisses (cm)", 30.0, 100.0, 55.0, 0.5)
        
        if st.form_submit_button("✅ Enregistrer", use_container_width=True):
            data = {'date': str(date.today()), 'weight': weight, 'belly': belly, 'arms': arms, 'thighs': thighs}
            if user_key == "luca":
                st.session_state.weight_luca.append(data)
            else:
                st.session_state.weight_sonia.append(data)
            st.success("✅ Enregistré !")
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
        col3.metric("Actuel", f"{current:.1f} kg", f"{diff:+.1f} kg")
        
        df = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['weight'], mode='lines+markers',
                                line=dict(color='#6366f1', width=3),
                                marker=dict(size=10)))
        fig.add_hline(y=target, line_dash="dash", line_color="#22c55e")
        fig.update_layout(height=300, title="Évolution du poids")
        st.plotly_chart(fig, use_container_width=True)
    else:
        col3.metric("Actuel", "-")
        st.info("📊 Enregistrez vos mensurations pour voir votre progression !")

# ==================== MAIN ====================
st.markdown('<div class="main-header">💪 FitCouple</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🍽️ REPAS LUCA", "🍽️ REPAS SONIA"])

with tab1:
    st.markdown("""<div class="profile-card">
        <h2 style="margin: 0;">👤 Luca</h2>
        <p style="margin: 0.5rem 0;">88 kg → 90 kg • 1m95 • Prise de masse + Perte ventre</p>
        <p style="margin: 0; opacity: 0.8;">🔥 Abdos: Lundi, Mercredi, Vendredi</p>
    </div>""", unsafe_allow_html=True)
    
    nav = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression"], 
                   horizontal=True, key="nav_luca", label_visibility="collapsed")
    
    if nav == "📅 Programme":
        day_idx = render_calendar(PROGRAM_LUCA, "luca")
        st.markdown("---")
        render_workout(PROGRAM_LUCA, day_idx, "luca")
    elif nav == "📏 Mensurations":
        render_measurements("luca", 88)
    else:
        render_progress("luca", 90, 88)

with tab2:
    st.markdown("""<div class="profile-card">
        <h2 style="margin: 0;">👤 Sonia</h2>
        <p style="margin: 0.5rem 0;">78 kg → 65 kg • 1m50 • Perte de poids + Tonification</p>
        <p style="margin: 0; opacity: 0.8;">🔥 Abdos: Lundi, Mercredi, Vendredi</p>
    </div>""", unsafe_allow_html=True)
    
    nav = st.radio("", ["📅 Programme", "📏 Mensurations", "📈 Progression"], 
                   horizontal=True, key="nav_sonia", label_visibility="collapsed")
    
    if nav == "📅 Programme":
        day_idx = render_calendar(PROGRAM_SONIA, "sonia")
        st.markdown("---")
        render_workout(PROGRAM_SONIA, day_idx, "sonia")
    elif nav == "📏 Mensurations":
        render_measurements("sonia", 78)
    else:
        render_progress("sonia", 65, 78)

with tab3:
    render_meal_calendar_luca()

with tab4:
    render_meal_calendar_sonia()

st.markdown("---")
st.caption("💪 FitCouple v4.2 - Planning repas optimisé")
