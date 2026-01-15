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

# CSS Pro
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

.exercise-card {
    background: white; border-radius: 16px; padding: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 0.8rem 0;
    border: 1px solid #f0f0f0; transition: transform 0.2s;
}
.exercise-card:hover { transform: translateY(-2px); }

.exercise-icon {
    width: 100%; height: 80px; border-radius: 12px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem;
}

.video-thumb {
    width: 100%; border-radius: 12px; cursor: pointer;
    transition: transform 0.2s;
}
.video-thumb:hover { transform: scale(1.02); }

.recipe-card {
    background: white; border-radius: 20px; overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin: 1rem 0;
    transition: transform 0.2s;
}
.recipe-card:hover { transform: translateY(-5px); }
.recipe-img {
    width: 100%; height: 180px; object-fit: cover;
}
.recipe-content {
    padding: 1rem;
}
.recipe-video-btn {
    display: inline-block; background: #ef4444; color: white !important;
    padding: 0.5rem 1rem; border-radius: 8px; text-decoration: none;
    font-weight: 600; font-size: 0.85rem; margin-top: 0.5rem;
}
.recipe-video-btn:hover { background: #dc2626; }

.macro-badge {
    display: inline-block; padding: 0.3rem 0.6rem;
    border-radius: 20px; font-size: 0.75rem; font-weight: 600;
    margin: 0.1rem;
}
.macro-cal { background: #fef3c7; color: #d97706; }
.macro-prot { background: #dbeafe; color: #2563eb; }

.day-card {
    padding: 0.8rem; border-radius: 12px; text-align: center;
    margin: 0.2rem; min-height: 80px; transition: all 0.2s;
    cursor: pointer;
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

.meal-plan-card {
    background: white; border-radius: 16px; padding: 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 0.5rem 0;
    border-left: 4px solid #6366f1;
}

.portion-luca {
    background: #dbeafe; color: #1e40af; padding: 0.3rem 0.6rem;
    border-radius: 8px; font-size: 0.8rem; font-weight: 600;
}
.portion-sonia {
    background: #fce7f3; color: #be185d; padding: 0.3rem 0.6rem;
    border-radius: 8px; font-size: 0.8rem; font-weight: 600;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px; background: #f1f5f9; padding: 8px; border-radius: 16px;
}
.stTabs [data-baseweb="tab"] {
    padding: 12px 24px; border-radius: 12px; font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
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
    "Pompes inclinées": {"video": "4dF1DOWzf20", "muscle": "Haut des pecs", "desc": "Cible le haut de la poitrine", "icon": "💪"},
    "Pompes serrées": {"video": "J0DnG1_S92I", "muscle": "Triceps", "desc": "Focus triceps", "icon": "💪"},
    "Pike push-ups": {"video": "sposDXWEB0A", "muscle": "Épaules", "desc": "Excellent pour les épaules", "icon": "🏋️"},
    "Dips sur chaise": {"video": "0326dy_-CzM", "muscle": "Triceps", "desc": "Triceps avec une chaise", "icon": "🪑"},
    "Développé haltères": {"video": "qEwKCR5JCog", "muscle": "Épaules", "desc": "Masse pour les épaules", "icon": "🏋️"},
    "Élévations latérales": {"video": "3VcKaXpzqRo", "muscle": "Épaules", "desc": "Épaules larges", "icon": "🏋️"},
    "Extension triceps": {"video": "_gsUck-7M74", "muscle": "Triceps", "desc": "Isolation triceps", "icon": "💪"},
    "Rowing haltère": {"video": "roCP6wCXPqo", "muscle": "Dos", "desc": "Dos épais", "icon": "🔙"},
    "Superman": {"video": "z6PJMT2y8GQ", "muscle": "Lombaires", "desc": "Renforce le bas du dos", "icon": "🦸"},
    "Oiseau": {"video": "EA7u4Q_8HQ0", "muscle": "Arrière épaule", "desc": "Arrière d'épaule", "icon": "🐦"},
    "Curl biceps": {"video": "ykJmrZ5v0Oo", "muscle": "Biceps", "desc": "Gros biceps", "icon": "💪"},
    "Curl marteau": {"video": "zC3nLlEvin4", "muscle": "Biceps", "desc": "Biceps + avant-bras", "icon": "🔨"},
    "Squats": {"video": "ultWZbUMPL8", "muscle": "Quadriceps", "desc": "Le roi des jambes", "icon": "🦵"},
    "Squats sumo": {"video": "9ZuXKqRbT9k", "muscle": "Adducteurs", "desc": "Intérieur cuisses", "icon": "🦵"},
    "Fentes": {"video": "QOVaHwm-Q6U", "muscle": "Quadriceps/Fessiers", "desc": "Jambes sculptées", "icon": "🦵"},
    "Hip thrust": {"video": "SEdqd1n0cvg", "muscle": "Fessiers", "desc": "Meilleur exo fessiers", "icon": "🍑"},
    "Glute bridge": {"video": "OUgsJ8-Vi0E", "muscle": "Fessiers", "desc": "Activation fessiers", "icon": "🍑"},
    "Donkey kicks": {"video": "SJ1Xuz9D-ZQ", "muscle": "Fessiers", "desc": "Galbe fessiers", "icon": "🍑"},
    "Fire hydrants": {"video": "La3xrTxLXSE", "muscle": "Fessiers", "desc": "Fessiers latéraux", "icon": "🔥"},
    "Jumping jacks": {"video": "c4DAnQ6DtF8", "muscle": "Cardio", "desc": "Cardio", "icon": "⭐"},
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
    # Exercices sans vidéo (repos/cardio simple)
    "Marche/Vélo léger": {"video": "", "muscle": "Cardio léger", "desc": "Récupération active", "icon": "🚶"},
    "Marche rapide/Vélo": {"video": "", "muscle": "Cardio", "desc": "Cardio modéré", "icon": "🚴"},
    "Vélo ou Course": {"video": "", "muscle": "Cardio", "desc": "Endurance", "icon": "🏃"},
    "Étirements": {"video": "", "muscle": "Flexibilité", "desc": "Récupération", "icon": "🧘"},
}

# ==================== RECETTES HEALTHY & GOURMANDES ====================
RECETTES = {
    "petit_dejeuner": [
        {
            "nom": "🥞 Pancakes Protéinés Banane",
            "img": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400",
            "video": "https://www.youtube.com/watch?v=N8iUYICFkvI",
            "kcal": 350, "prot": 25,
            "ingredients": ["1 banane mûre", "2 oeufs", "30g flocons d'avoine", "30g whey vanille", "1 c.c levure"],
            "prep": "Mixer tout. Cuire à la poêle comme des pancakes. Servir avec fruits frais.",
            "why": "Délicieux, rassasiant et plein de protéines !",
            "portions": {"luca": "3 pancakes + 40g whey", "sonia": "2 pancakes + 20g whey"}
        },
        {
            "nom": "🥑 Toast Avocat Oeuf Poché",
            "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400",
            "video": "https://www.youtube.com/watch?v=66btvAWmp7g",
            "kcal": 380, "prot": 18,
            "ingredients": ["1 tranche pain complet", "1/2 avocat", "1 oeuf", "Citron", "Piment (option)"],
            "prep": "Toaster le pain. Écraser l'avocat avec citron. Pocher l'oeuf. Assembler.",
            "why": "Bon gras + protéines = énergie longue durée",
            "portions": {"luca": "2 toasts + 2 oeufs", "sonia": "1 toast + 1 oeuf"}
        },
        {
            "nom": "🫐 Overnight Oats Fruits Rouges",
            "img": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=400",
            "video": "https://www.youtube.com/watch?v=O9Hf_8WvSKE",
            "kcal": 320, "prot": 22,
            "ingredients": ["50g flocons d'avoine", "150ml lait", "100g yaourt grec", "Fruits rouges", "Miel"],
            "prep": "Mélanger avoine, lait, yaourt. Réfrigérer une nuit. Ajouter fruits et miel.",
            "why": "Zéro effort le matin, super healthy",
            "portions": {"luca": "70g avoine + 200g yaourt", "sonia": "40g avoine + 100g yaourt"}
        },
    ],
    "dejeuner": [
        {
            "nom": "🍛 Buddha Bowl Poulet",
            "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
            "video": "https://www.youtube.com/watch?v=Yz-x10gXRCI",
            "kcal": 480, "prot": 42,
            "ingredients": ["150g poulet", "100g quinoa", "Avocat", "Pois chiches", "Légumes", "Sauce tahini"],
            "prep": "Cuire quinoa et poulet. Disposer tous les ingrédients en bowl. Sauce tahini.",
            "why": "Complet, coloré, délicieux et ultra rassasiant",
            "portions": {"luca": "200g poulet + 150g quinoa", "sonia": "120g poulet + 80g quinoa"}
        },
        {
            "nom": "🌮 Wrap Poulet Caesar Light",
            "img": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400",
            "video": "https://www.youtube.com/watch?v=5GqbKMxb7x0",
            "kcal": 420, "prot": 38,
            "ingredients": ["1 tortilla complète", "150g poulet", "Salade romaine", "Parmesan", "Sauce yaourt-citron"],
            "prep": "Griller le poulet. Préparer sauce yaourt+citron+ail. Garnir et rouler.",
            "why": "Le goût d'un Caesar sans les calories",
            "portions": {"luca": "2 wraps", "sonia": "1 wrap"}
        },
        {
            "nom": "🍝 Poke Bowl Saumon",
            "img": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=400",
            "video": "https://www.youtube.com/watch?v=c_5LP3k9cHs",
            "kcal": 450, "prot": 35,
            "ingredients": ["150g saumon frais", "100g riz", "Avocat", "Edamame", "Mangue", "Sauce soja"],
            "prep": "Cuire le riz. Couper saumon en cubes. Assembler avec tous les toppings.",
            "why": "Oméga-3 + fraîcheur = combo gagnant",
            "portions": {"luca": "180g saumon + 150g riz", "sonia": "120g saumon + 80g riz"}
        },
    ],
    "diner": [
        {
            "nom": "🍛 Curry Poulet Léger",
            "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
            "video": "https://www.youtube.com/watch?v=iFTlWbo8ZQk",
            "kcal": 380, "prot": 40,
            "ingredients": ["200g poulet", "Lait de coco light", "Curry", "Poivrons", "Oignon", "Riz basmati"],
            "prep": "Faire revenir poulet et légumes. Ajouter curry et lait coco. Mijoter. Servir avec riz.",
            "why": "Saveurs intenses, peu de calories",
            "portions": {"luca": "250g poulet + 120g riz", "sonia": "150g poulet + 60g riz"}
        },
        {
            "nom": "🐟 Papillote Saumon Citron",
            "img": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400",
            "video": "https://www.youtube.com/watch?v=4TfwtSqXhHo",
            "kcal": 350, "prot": 38,
            "ingredients": ["180g saumon", "Citron", "Aneth", "Courgettes", "Tomates cerises"],
            "prep": "Mettre saumon et légumes en papillote. Citron et aneth. Four 20min à 180°C.",
            "why": "Cuisson sans gras, maximum de goût",
            "portions": {"luca": "220g saumon + légumes à volonté", "sonia": "150g saumon + légumes à volonté"}
        },
        {
            "nom": "🍜 Wok Crevettes Légumes",
            "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400",
            "video": "https://www.youtube.com/watch?v=MeD8bDgYy2s",
            "kcal": 320, "prot": 32,
            "ingredients": ["200g crevettes", "Brocoli", "Poivrons", "Champignons", "Sauce soja", "Gingembre"],
            "prep": "Sauter les crevettes. Ajouter légumes. Assaisonner sauce soja et gingembre.",
            "why": "Rapide, léger et plein de saveurs asiatiques",
            "portions": {"luca": "250g crevettes + nouilles", "sonia": "180g crevettes seules"}
        },
    ],
    "collation": [
        {
            "nom": "🥤 Smoothie Protéiné Chocolat",
            "img": "https://images.unsplash.com/photo-1553530666-ba11a90a0868?w=400",
            "video": "https://www.youtube.com/watch?v=eMxY0xLrHd0",
            "kcal": 280, "prot": 30,
            "ingredients": ["30g whey chocolat", "250ml lait d'amande", "1 banane", "1 c.s beurre cacahuète"],
            "prep": "Mixer tous les ingrédients jusqu'à consistance lisse.",
            "why": "Goût dessert, macros parfaites",
            "portions": {"luca": "40g whey + beurre cacahuète", "sonia": "20g whey sans beurre"}
        },
        {
            "nom": "🍫 Energy Balls Cacao",
            "img": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400",
            "video": "https://www.youtube.com/watch?v=jpKjz8vfKb8",
            "kcal": 180, "prot": 8,
            "ingredients": ["100g dattes", "50g amandes", "2 c.s cacao", "1 c.s miel"],
            "prep": "Mixer dattes et amandes. Ajouter cacao et miel. Former des boules. Réfrigérer.",
            "why": "Sucré naturellement, énergie immédiate",
            "portions": {"luca": "4 balls", "sonia": "2 balls"}
        },
        {
            "nom": "🍌 Yaourt Grec Gourmand",
            "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
            "video": "https://www.youtube.com/watch?v=_2eqlzCo3kU",
            "kcal": 200, "prot": 18,
            "ingredients": ["200g yaourt grec 0%", "Granola", "Miel", "Fruits frais"],
            "prep": "Mettre yaourt dans un bol. Ajouter granola, fruits et filet de miel.",
            "why": "Protéiné, gourmand et rassasiant",
            "portions": {"luca": "250g yaourt + 40g granola", "sonia": "150g yaourt + 20g granola"}
        },
    ]
}

# ==================== PLANNING REPAS SEMAINE ====================
MEAL_PLAN = {
    0: {"petit_dej": 0, "dejeuner": 0, "diner": 0, "collation": 0},  # Lundi
    1: {"petit_dej": 1, "dejeuner": 1, "diner": 1, "collation": 1},  # Mardi
    2: {"petit_dej": 2, "dejeuner": 2, "diner": 2, "collation": 2},  # Mercredi
    3: {"petit_dej": 0, "dejeuner": 0, "diner": 1, "collation": 0},  # Jeudi
    4: {"petit_dej": 1, "dejeuner": 1, "diner": 0, "collation": 1},  # Vendredi
    5: {"petit_dej": 2, "dejeuner": 2, "diner": 2, "collation": 2},  # Samedi
    6: {"petit_dej": 0, "dejeuner": 0, "diner": 1, "collation": 0},  # Dimanche
}

# ==================== PROGRAMMES ====================
JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

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
    
    # Sélecteur de jour
    selected_day = st.selectbox(
        "📅 Choisir le jour",
        options=list(range(7)),
        format_func=lambda x: f"{'👉 ' if x == today_idx else ''}{JOURS[x]} - {program.get(x, {}).get('nom', 'Repos')}",
        index=today_idx,
        key=f"day_select_{user_key}"
    )
    
    # Affichage du calendrier visuel
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

def render_exercise_card(nom, sets):
    ex = EXERCICES.get(nom, {"video": "", "muscle": "", "desc": "", "icon": "🏋️"})
    video_id = ex.get('video', '')
    muscle = ex.get('muscle', '')
    desc = ex.get('desc', '')
    icon = ex.get('icon', '🏋️')
    
    # Si pas de vidéo, afficher une carte avec icône
    if not video_id:
        st.markdown(f"""
        <div class="exercise-card">
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div style="flex: 0 0 80px;">
                    <div class="exercise-icon">{icon}</div>
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: #1e1e2e;">{nom}</h4>
                    <p style="margin: 0.2rem 0; color: #6366f1; font-weight: 600;">{sets}</p>
                    <p style="margin: 0; font-size: 0.8rem; color: #64748b;">{desc}</p>
                    <span style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.7rem;">{muscle}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    thumb = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    link = f"https://youtube.com/watch?v={video_id}"
    
    st.markdown(f"""
    <div class="exercise-card">
        <div style="display: flex; gap: 1rem; align-items: center;">
            <div style="flex: 0 0 140px;">
                <a href="{link}" target="_blank">
                    <img src="{thumb}" class="video-thumb" alt="{nom}">
                </a>
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; color: #1e1e2e;">{nom}</h4>
                <p style="margin: 0.2rem 0; color: #6366f1; font-weight: 600;">{sets}</p>
                <p style="margin: 0; font-size: 0.8rem; color: #64748b;">{desc}</p>
                <span style="background: #f1f5f9; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.7rem;">{muscle}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_workout(program, day_idx, user_key):
    workout = program.get(day_idx, {})
    
    st.markdown(f"## {workout.get('emoji', '')} {workout.get('nom', 'REPOS')}")
    st.markdown(f"**{workout.get('type', '')}** • {workout.get('duree', 0)} minutes")
    
    if not workout.get('exercices'):
        st.success("💤 Jour de repos ! Profitez-en pour récupérer.")
        return
    
    st.markdown("---")
    
    for nom, sets in workout.get('exercices', []):
        render_exercise_card(nom, sets)
    
    if workout.get('abdos'):
        st.markdown("""<div class="abdos-banner">
            <h3 style="margin: 0;">🔥 CIRCUIT ABDOS</h3>
            <p style="margin: 0.5rem 0 0 0;">2 tours • 30 sec repos entre les tours</p>
        </div>""", unsafe_allow_html=True)
        
        for nom, reps in CIRCUIT_ABDOS:
            render_exercise_card(nom, reps)
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        feeling = st.slider("Comment était ta séance ?", 1, 5, 3, key=f"feel_{user_key}_{day_idx}")
    with col2:
        if st.button("✅ Terminé !", key=f"btn_{user_key}_{day_idx}", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Bravo !")

def render_recipe_card(recipe, show_portions=False):
    st.markdown(f"""
    <div class="recipe-card">
        <img src="{recipe['img']}" class="recipe-img" alt="{recipe['nom']}">
        <div class="recipe-content">
            <h4 style="margin: 0 0 0.3rem 0;">{recipe['nom']}</h4>
            <div style="margin-bottom: 0.5rem;">
                <span class="macro-badge macro-cal">{recipe['kcal']} kcal</span>
                <span class="macro-badge macro-prot">{recipe['prot']}g prot</span>
            </div>
            <p style="font-size: 0.8rem; color: #64748b; margin: 0;">{recipe['why']}</p>
            <a href="{recipe['video']}" target="_blank" class="recipe-video-btn">▶️ Voir la recette</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if show_portions and 'portions' in recipe:
        st.markdown(f"""
        <div style="margin-top: 0.5rem;">
            <span class="portion-luca">🏋️ Luca: {recipe['portions']['luca']}</span>
            <span class="portion-sonia">🧘 Sonia: {recipe['portions']['sonia']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📝 Ingrédients & Préparation"):
        st.markdown("**Ingrédients:**")
        for ing in recipe['ingredients']:
            st.markdown(f"• {ing}")
        st.markdown(f"\n**Préparation:** {recipe['prep']}")

def render_nutrition():
    st.markdown("## 🍽️ Recettes Healthy & Gourmandes")
    st.markdown("*Des plats délicieux qui font perdre du poids*")
    
    category = st.selectbox(
        "Quel repas ?",
        ["🍳 Petit-déjeuner", "🍝 Déjeuner", "🌙 Dîner", "🍪 Collation"],
        key="cat_select"
    )
    
    cat_map = {
        "🍳 Petit-déjeuner": "petit_dejeuner",
        "🍝 Déjeuner": "dejeuner",
        "🌙 Dîner": "diner",
        "🍪 Collation": "collation"
    }
    
    recipes = RECETTES.get(cat_map[category], [])
    
    cols = st.columns(3)
    for idx, recipe in enumerate(recipes):
        with cols[idx % 3]:
            render_recipe_card(recipe, show_portions=True)

def render_meal_plan():
    st.markdown("## 📅 Planning Repas de la Semaine")
    st.markdown("*Mêmes plats, portions adaptées à chaque objectif*")
    
    # Sélecteur de jour pour le planning repas
    selected_day = st.selectbox(
        "📅 Voir le menu du jour",
        options=list(range(7)),
        format_func=lambda x: JOURS[x],
        index=date.today().weekday(),
        key="meal_day_select"
    )
    
    plan = MEAL_PLAN.get(selected_day, {})
    
    st.markdown(f"### 📆 Menu du {JOURS[selected_day]}")
    
    # Petit-déjeuner
    st.markdown("#### 🍳 Petit-déjeuner")
    recipe = RECETTES["petit_dejeuner"][plan.get("petit_dej", 0)]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(recipe['img'], use_container_width=True)
    with col2:
        st.markdown(f"**{recipe['nom']}**")
        st.markdown(f"""
        <span class="portion-luca">🏋️ Luca: {recipe['portions']['luca']}</span><br>
        <span class="portion-sonia">🧘 Sonia: {recipe['portions']['sonia']}</span>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Déjeuner
    st.markdown("#### 🍝 Déjeuner")
    recipe = RECETTES["dejeuner"][plan.get("dejeuner", 0)]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(recipe['img'], use_container_width=True)
    with col2:
        st.markdown(f"**{recipe['nom']}**")
        st.markdown(f"""
        <span class="portion-luca">🏋️ Luca: {recipe['portions']['luca']}</span><br>
        <span class="portion-sonia">🧘 Sonia: {recipe['portions']['sonia']}</span>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Collation
    st.markdown("#### 🍪 Collation")
    recipe = RECETTES["collation"][plan.get("collation", 0)]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(recipe['img'], use_container_width=True)
    with col2:
        st.markdown(f"**{recipe['nom']}**")
        st.markdown(f"""
        <span class="portion-luca">🏋️ Luca: {recipe['portions']['luca']}</span><br>
        <span class="portion-sonia">🧘 Sonia: {recipe['portions']['sonia']}</span>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dîner
    st.markdown("#### 🌙 Dîner")
    recipe = RECETTES["diner"][plan.get("diner", 0)]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(recipe['img'], use_container_width=True)
    with col2:
        st.markdown(f"**{recipe['nom']}**")
        st.markdown(f"""
        <span class="portion-luca">🏋️ Luca: {recipe['portions']['luca']}</span><br>
        <span class="portion-sonia">🧘 Sonia: {recipe['portions']['sonia']}</span>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Résumé calories
    st.markdown("### 📊 Résumé Journalier")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: #dbeafe; padding: 1rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; color: #1e40af;">🏋️ Luca</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; font-weight: 700; color: #1e40af;">~2400 kcal</p>
            <p style="margin: 0; color: #3b82f6;">Prise de masse</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: #fce7f3; padding: 1rem; border-radius: 12px; text-align: center;">
            <h3 style="margin: 0; color: #be185d;">🧘 Sonia</h3>
            <p style="font-size: 2rem; margin: 0.5rem 0; font-weight: 700; color: #be185d;">~1400 kcal</p>
            <p style="margin: 0; color: #ec4899;">Perte de poids</p>
        </div>
        """, unsafe_allow_html=True)

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

tab1, tab2, tab3, tab4 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🥗 RECETTES", "📅 PLANNING REPAS"])

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
    render_nutrition()

with tab4:
    render_meal_plan()

st.markdown("---")
st.caption("💪 FitCouple v4.0")
