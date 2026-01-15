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

/* NEW EXERCISE CARD DESIGN */
.exercise-card-new {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 20px;
    padding: 0;
    margin: 1rem 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(99, 102, 241, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
}
.exercise-card-new:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(99, 102, 241, 0.15);
}

.exercise-video-container {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
}
.exercise-video-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}
.exercise-card-new:hover .exercise-video-container img {
    transform: scale(1.05);
}
.play-button {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 70px;
    height: 70px;
    background: rgba(255,255,255,0.95);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
.exercise-card-new:hover .play-button {
    transform: translate(-50%, -50%) scale(1.1);
    background: #6366f1;
    color: white;
}

.exercise-info {
    padding: 1.2rem;
}
.exercise-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e1e2e;
    margin: 0 0 0.5rem 0;
}
.exercise-sets {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 0.4rem 1rem;
    border-radius: 25px;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
.exercise-muscle {
    display: inline-block;
    background: #f1f5f9;
    color: #64748b;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-left: 0.5rem;
}
.exercise-desc {
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

/* Card sans vidéo */
.exercise-icon-box {
    width: 100%;
    height: 150px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}

/* Recipe cards */
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

/* Nutrition user cards */
.nutrition-user-card {
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}
.nutrition-luca {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white;
}
.nutrition-sonia {
    background: linear-gradient(135deg, #be185d 0%, #ec4899 100%);
    color: white;
}

.portion-tag {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    margin: 0.3rem 0;
}
.portion-luca { background: #dbeafe; color: #1e40af; }
.portion-sonia { background: #fce7f3; color: #be185d; }

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

# ==================== EXERCICES (Vidéos vérifiées) ====================
EXERCICES = {
    # PUSH
    "Pompes classiques": {"video": "IODxDxX7oi4", "muscle": "Pectoraux", "desc": "Le basique pour des pecs en béton", "icon": "💪"},
    "Pompes inclinées": {"video": "cfns5VDVVvk", "muscle": "Haut des pecs", "desc": "Cible le haut de la poitrine", "icon": "💪"},
    "Pompes serrées": {"video": "J0DnG1_S92I", "muscle": "Triceps", "desc": "Focus triceps", "icon": "💪"},
    "Pike push-ups": {"video": "sposDXWEB0A", "muscle": "Épaules", "desc": "Excellent pour les épaules", "icon": "🏋️"},
    "Dips sur chaise": {"video": "0326dy_-CzM", "muscle": "Triceps", "desc": "Triceps avec une chaise", "icon": "🪑"},
    "Développé haltères": {"video": "VmB1G1K7v94", "muscle": "Épaules", "desc": "Masse pour les épaules", "icon": "🏋️"},
    "Élévations latérales": {"video": "3VcKaXpzqRo", "muscle": "Épaules", "desc": "Épaules larges", "icon": "🏋️"},
    "Extension triceps": {"video": "nRiJVZDpdL0", "muscle": "Triceps", "desc": "Isolation triceps", "icon": "💪"},
    # PULL
    "Rowing haltère": {"video": "roCP6wCXPqo", "muscle": "Dos", "desc": "Dos épais", "icon": "🔙"},
    "Superman": {"video": "z6PJMT2y8GQ", "muscle": "Lombaires", "desc": "Renforce le bas du dos", "icon": "🦸"},
    "Oiseau": {"video": "EA7u4Q_8HQ0", "muscle": "Arrière épaule", "desc": "Arrière d'épaule", "icon": "🐦"},
    "Curl biceps": {"video": "ykJmrZ5v0Oo", "muscle": "Biceps", "desc": "Gros biceps", "icon": "💪"},
    "Curl marteau": {"video": "zC3nLlEvin4", "muscle": "Biceps", "desc": "Biceps + avant-bras", "icon": "🔨"},
    # LEGS
    "Squats": {"video": "YaXPRqUwItQ", "muscle": "Quadriceps", "desc": "Le roi des jambes", "icon": "🦵"},
    "Squats sumo": {"video": "9ZuXKqRbT9k", "muscle": "Adducteurs", "desc": "Intérieur cuisses", "icon": "🦵"},
    "Fentes": {"video": "QOVaHwm-Q6U", "muscle": "Quadriceps/Fessiers", "desc": "Jambes sculptées", "icon": "🦵"},
    "Hip thrust": {"video": "SEdqd1n0cvg", "muscle": "Fessiers", "desc": "Meilleur exo fessiers", "icon": "🍑"},
    "Glute bridge": {"video": "OUgsJ8-Vi0E", "muscle": "Fessiers", "desc": "Activation fessiers", "icon": "🍑"},
    "Donkey kicks": {"video": "SJ1Xuz9D-ZQ", "muscle": "Fessiers", "desc": "Galbe fessiers", "icon": "🍑"},
    "Fire hydrants": {"video": "La3xrTxLXSE", "muscle": "Fessiers", "desc": "Fessiers latéraux", "icon": "🔥"},
    # CARDIO
    "Jumping jacks": {"video": "c4DAnQ6DtF8", "muscle": "Cardio", "desc": "Échauffement", "icon": "⭐"},
    "Burpees": {"video": "TU8QYVW0gDU", "muscle": "Full body", "desc": "Brûleur de calories", "icon": "🔥"},
    "High knees": {"video": "D0bLJnSBNI8", "muscle": "Cardio", "desc": "Cardio intense", "icon": "🏃"},
    "Squat jumps": {"video": "A-cFYWvaHr0", "muscle": "Jambes/Cardio", "desc": "Explosivité", "icon": "🦘"},
    "Mountain climbers": {"video": "nmwgirgXLYM", "muscle": "Core/Cardio", "desc": "Abdos + cardio", "icon": "⛰️"},
    # CORE
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

# ==================== RECETTES LUCA (Prise de masse ~2400 kcal) ====================
RECETTES_LUCA = {
    "petit_dejeuner": [
        {
            "nom": "🥞 Pancakes Protéinés XL",
            "img": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400",
            "video": "https://www.youtube.com/watch?v=N8iUYICFkvI",
            "kcal": 550, "prot": 40,
            "ingredients": ["2 bananes", "3 oeufs", "60g flocons d'avoine", "40g whey vanille", "1 c.c levure", "Beurre de cacahuète"],
            "prep": "Mixer tout. Cuire 4-5 gros pancakes. Servir avec beurre de cacahuète et fruits.",
        },
        {
            "nom": "🥑 Double Toast Avocat",
            "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400",
            "video": "https://www.youtube.com/watch?v=66btvAWmp7g",
            "kcal": 580, "prot": 28,
            "ingredients": ["2 tranches pain complet", "1 avocat entier", "2 oeufs", "Saumon fumé 50g", "Citron"],
            "prep": "Toaster le pain. Écraser l'avocat. Pocher les oeufs. Ajouter saumon.",
        },
        {
            "nom": "🫐 Overnight Oats Masse",
            "img": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=400",
            "video": "https://www.youtube.com/watch?v=O9Hf_8WvSKE",
            "kcal": 520, "prot": 35,
            "ingredients": ["80g flocons d'avoine", "200ml lait entier", "200g yaourt grec", "30g whey", "Fruits", "Amandes"],
            "prep": "Mélanger tout la veille. Ajouter fruits et amandes le matin.",
        },
    ],
    "dejeuner": [
        {
            "nom": "🍛 Buddha Bowl XL Poulet",
            "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
            "video": "https://www.youtube.com/watch?v=Yz-x10gXRCI",
            "kcal": 680, "prot": 55,
            "ingredients": ["220g poulet", "150g quinoa cuit", "1 avocat", "100g pois chiches", "Légumes variés", "Sauce tahini"],
            "prep": "Cuire quinoa et poulet. Assembler le bowl. Sauce généreuse.",
        },
        {
            "nom": "🌮 Double Wrap Poulet",
            "img": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400",
            "video": "https://www.youtube.com/watch?v=5GqbKMxb7x0",
            "kcal": 650, "prot": 52,
            "ingredients": ["2 tortillas complètes", "200g poulet", "Riz 100g", "Haricots noirs", "Fromage", "Sauce"],
            "prep": "Griller poulet. Préparer garniture. Rouler les 2 wraps.",
        },
        {
            "nom": "🍝 Poke Bowl Saumon XL",
            "img": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=400",
            "video": "https://www.youtube.com/watch?v=c_5LP3k9cHs",
            "kcal": 620, "prot": 45,
            "ingredients": ["200g saumon frais", "150g riz", "1 avocat", "Edamame 100g", "Mangue", "Sauce soja"],
            "prep": "Cuire riz. Couper saumon. Assembler avec toppings généreux.",
        },
    ],
    "diner": [
        {
            "nom": "🍛 Curry Poulet Complet",
            "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
            "video": "https://www.youtube.com/watch?v=iFTlWbo8ZQk",
            "kcal": 580, "prot": 50,
            "ingredients": ["250g poulet", "Lait de coco", "Curry", "Légumes", "150g riz basmati"],
            "prep": "Revenir poulet et légumes. Ajouter curry et coco. Servir avec riz.",
        },
        {
            "nom": "🐟 Pavé Saumon + Patate Douce",
            "img": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400",
            "video": "https://www.youtube.com/watch?v=4TfwtSqXhHo",
            "kcal": 550, "prot": 45,
            "ingredients": ["220g saumon", "200g patate douce", "Brocoli", "Citron", "Huile d'olive"],
            "prep": "Four: saumon 20min, patate douce 35min. Brocoli vapeur.",
        },
        {
            "nom": "🍝 Pasta Poulet Pesto",
            "img": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=400",
            "video": "https://www.youtube.com/watch?v=bJUiWdM__Qw",
            "kcal": 650, "prot": 48,
            "ingredients": ["150g pâtes complètes", "200g poulet", "Pesto", "Tomates cerises", "Parmesan"],
            "prep": "Cuire pâtes. Griller poulet. Mélanger avec pesto. Parmesan.",
        },
    ],
    "collation": [
        {
            "nom": "🥤 Shake Masse Chocolat",
            "img": "https://images.unsplash.com/photo-1553530666-ba11a90a0868?w=400",
            "video": "https://www.youtube.com/watch?v=eMxY0xLrHd0",
            "kcal": 450, "prot": 40,
            "ingredients": ["40g whey chocolat", "300ml lait entier", "1 banane", "2 c.s beurre cacahuète", "Avoine 30g"],
            "prep": "Mixer tout jusqu'à consistance lisse.",
        },
        {
            "nom": "🥜 Mix Énergétique",
            "img": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400",
            "video": "https://www.youtube.com/watch?v=jpKjz8vfKb8",
            "kcal": 350, "prot": 15,
            "ingredients": ["50g amandes", "30g noix de cajou", "30g raisins secs", "Chocolat noir 20g"],
            "prep": "Mélanger et portionner. Snack parfait.",
        },
        {
            "nom": "🍌 Bowl Protéiné",
            "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
            "video": "https://www.youtube.com/watch?v=_2eqlzCo3kU",
            "kcal": 380, "prot": 30,
            "ingredients": ["300g yaourt grec", "50g granola", "Miel", "Banane", "Amandes"],
            "prep": "Yaourt + toppings. Simple et efficace.",
        },
    ]
}

# ==================== RECETTES SONIA (Perte de poids ~1400 kcal) ====================
RECETTES_SONIA = {
    "petit_dejeuner": [
        {
            "nom": "🥞 Mini Pancakes Light",
            "img": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400",
            "video": "https://www.youtube.com/watch?v=N8iUYICFkvI",
            "kcal": 280, "prot": 20,
            "ingredients": ["1 banane", "2 blancs d'oeuf + 1 entier", "25g flocons d'avoine", "20g whey", "Cannelle"],
            "prep": "Mixer. Cuire 2-3 petits pancakes. Servir avec fruits rouges.",
        },
        {
            "nom": "🥑 Toast Avocat Light",
            "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=400",
            "video": "https://www.youtube.com/watch?v=66btvAWmp7g",
            "kcal": 300, "prot": 15,
            "ingredients": ["1 tranche pain complet", "1/2 avocat", "1 oeuf poché", "Citron", "Graines de chia"],
            "prep": "Toast léger. Avocat écrasé. Oeuf poché. Graines.",
        },
        {
            "nom": "🫐 Overnight Oats Light",
            "img": "https://images.unsplash.com/photo-1517673400267-0251440c45dc?w=400",
            "video": "https://www.youtube.com/watch?v=O9Hf_8WvSKE",
            "kcal": 260, "prot": 18,
            "ingredients": ["40g flocons d'avoine", "150ml lait d'amande", "100g yaourt grec 0%", "Fruits rouges", "Stevia"],
            "prep": "Mélanger la veille. Fruits frais le matin.",
        },
    ],
    "dejeuner": [
        {
            "nom": "🥗 Salade Buddha Light",
            "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",
            "video": "https://www.youtube.com/watch?v=Yz-x10gXRCI",
            "kcal": 380, "prot": 35,
            "ingredients": ["120g poulet grillé", "Quinoa 60g", "1/4 avocat", "Légumes variés", "Vinaigrette légère"],
            "prep": "Griller poulet. Cuire quinoa. Assembler salade colorée.",
        },
        {
            "nom": "🌮 Wrap Léger",
            "img": "https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400",
            "video": "https://www.youtube.com/watch?v=5GqbKMxb7x0",
            "kcal": 350, "prot": 30,
            "ingredients": ["1 tortilla complète", "120g poulet", "Salade", "Tomates", "Sauce yaourt 0%"],
            "prep": "Poulet grillé. Légumes frais. Rouler.",
        },
        {
            "nom": "🍣 Poke Light",
            "img": "https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?w=400",
            "video": "https://www.youtube.com/watch?v=c_5LP3k9cHs",
            "kcal": 360, "prot": 30,
            "ingredients": ["130g saumon", "Riz 60g", "Concombre", "Edamame 50g", "Sauce soja allégée"],
            "prep": "Portion légère de riz. Saumon frais. Légumes croquants.",
        },
    ],
    "diner": [
        {
            "nom": "🍛 Curry Poulet Ultra Light",
            "img": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
            "video": "https://www.youtube.com/watch?v=iFTlWbo8ZQk",
            "kcal": 320, "prot": 35,
            "ingredients": ["150g poulet", "Lait de coco light", "Curry", "Légumes variés", "PAS de riz"],
            "prep": "Poulet et légumes. Curry + coco light. Servir sans féculent.",
        },
        {
            "nom": "🐟 Papillote Saumon Légumes",
            "img": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400",
            "video": "https://www.youtube.com/watch?v=4TfwtSqXhHo",
            "kcal": 300, "prot": 32,
            "ingredients": ["150g saumon", "Courgettes", "Tomates", "Citron", "Herbes fraîches"],
            "prep": "Papillote au four 20min. Zéro matière grasse ajoutée.",
        },
        {
            "nom": "🍜 Wok Crevettes Light",
            "img": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=400",
            "video": "https://www.youtube.com/watch?v=MeD8bDgYy2s",
            "kcal": 280, "prot": 28,
            "ingredients": ["180g crevettes", "Brocoli", "Poivrons", "Champignons", "Sauce soja légère"],
            "prep": "Wok à sec. Crevettes + légumes. Sauce soja en fin.",
        },
    ],
    "collation": [
        {
            "nom": "🥤 Smoothie Light",
            "img": "https://images.unsplash.com/photo-1553530666-ba11a90a0868?w=400",
            "video": "https://www.youtube.com/watch?v=eMxY0xLrHd0",
            "kcal": 180, "prot": 20,
            "ingredients": ["20g whey vanille", "200ml lait d'amande", "Fruits rouges", "Glaçons"],
            "prep": "Mixer. Rafraîchissant et léger.",
        },
        {
            "nom": "🍫 2 Energy Balls",
            "img": "https://images.unsplash.com/photo-1604329760661-e71dc83f8f26?w=400",
            "video": "https://www.youtube.com/watch?v=jpKjz8vfKb8",
            "kcal": 120, "prot": 5,
            "ingredients": ["Dattes", "Amandes", "Cacao", "Seulement 2 boules!"],
            "prep": "Portion contrôlée: 2 boules max.",
        },
        {
            "nom": "🍌 Yaourt Grec Simple",
            "img": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400",
            "video": "https://www.youtube.com/watch?v=_2eqlzCo3kU",
            "kcal": 140, "prot": 15,
            "ingredients": ["150g yaourt grec 0%", "Quelques fruits", "Cannelle", "Pas de granola!"],
            "prep": "Simple: yaourt + fruits + cannelle.",
        },
    ]
}

# ==================== PLANNING REPAS ====================
MEAL_PLAN = {
    0: {"petit_dej": 0, "dejeuner": 0, "diner": 0, "collation": 0},
    1: {"petit_dej": 1, "dejeuner": 1, "diner": 1, "collation": 1},
    2: {"petit_dej": 2, "dejeuner": 2, "diner": 2, "collation": 2},
    3: {"petit_dej": 0, "dejeuner": 0, "diner": 1, "collation": 0},
    4: {"petit_dej": 1, "dejeuner": 1, "diner": 0, "collation": 1},
    5: {"petit_dej": 2, "dejeuner": 2, "diner": 2, "collation": 2},
    6: {"petit_dej": 0, "dejeuner": 0, "diner": 1, "collation": 0},
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
        # Card sans vidéo - avec icône
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
    
    # Affichage en grille 2 colonnes
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
        feeling = st.slider("Comment était ta séance ?", 1, 5, 3, key=f"feel_{user_key}_{day_idx}")
    with col2:
        if st.button("✅ Terminé !", key=f"btn_{user_key}_{day_idx}", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Bravo !")

def render_recipe_card(recipe):
    st.markdown(f"""
    <div class="recipe-card">
        <img src="{recipe['img']}" class="recipe-img" alt="{recipe['nom']}">
        <div class="recipe-content">
            <h4 style="margin: 0 0 0.3rem 0;">{recipe['nom']}</h4>
            <div style="margin-bottom: 0.5rem;">
                <span class="macro-badge macro-cal">{recipe['kcal']} kcal</span>
                <span class="macro-badge macro-prot">{recipe['prot']}g prot</span>
            </div>
            <a href="{recipe['video']}" target="_blank" class="recipe-video-btn">▶️ Vidéo recette</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📝 Ingrédients & Préparation"):
        st.markdown("**Ingrédients:**")
        for ing in recipe['ingredients']:
            st.markdown(f"• {ing}")
        st.markdown(f"\n**Préparation:** {recipe['prep']}")

def render_nutrition_luca():
    st.markdown("""
    <div class="nutrition-user-card nutrition-luca">
        <h2 style="margin: 0;">🏋️ Alimentation LUCA</h2>
        <p style="margin: 0.5rem 0 0 0;">Prise de masse • ~2400 kcal/jour • Protéines ++</p>
    </div>
    """, unsafe_allow_html=True)
    
    category = st.selectbox(
        "Quel repas ?",
        ["🍳 Petit-déjeuner", "🍝 Déjeuner", "🌙 Dîner", "🍪 Collation"],
        key="cat_luca"
    )
    
    cat_map = {
        "🍳 Petit-déjeuner": "petit_dejeuner",
        "🍝 Déjeuner": "dejeuner",
        "🌙 Dîner": "diner",
        "🍪 Collation": "collation"
    }
    
    recipes = RECETTES_LUCA.get(cat_map[category], [])
    
    cols = st.columns(3)
    for idx, recipe in enumerate(recipes):
        with cols[idx % 3]:
            render_recipe_card(recipe)

def render_nutrition_sonia():
    st.markdown("""
    <div class="nutrition-user-card nutrition-sonia">
        <h2 style="margin: 0;">🧘 Alimentation SONIA</h2>
        <p style="margin: 0.5rem 0 0 0;">Perte de poids • ~1400 kcal/jour • Light & Healthy</p>
    </div>
    """, unsafe_allow_html=True)
    
    category = st.selectbox(
        "Quel repas ?",
        ["🍳 Petit-déjeuner", "🍝 Déjeuner", "🌙 Dîner", "🍪 Collation"],
        key="cat_sonia"
    )
    
    cat_map = {
        "🍳 Petit-déjeuner": "petit_dejeuner",
        "🍝 Déjeuner": "dejeuner",
        "🌙 Dîner": "diner",
        "🍪 Collation": "collation"
    }
    
    recipes = RECETTES_SONIA.get(cat_map[category], [])
    
    cols = st.columns(3)
    for idx, recipe in enumerate(recipes):
        with cols[idx % 3]:
            render_recipe_card(recipe)

def render_meal_plan():
    st.markdown("## 📅 Planning Repas Semaine")
    
    who = st.radio("Pour qui ?", ["🏋️ Luca", "🧘 Sonia"], horizontal=True, key="meal_who")
    
    selected_day = st.selectbox(
        "📅 Jour",
        options=list(range(7)),
        format_func=lambda x: JOURS[x],
        index=date.today().weekday(),
        key="meal_day"
    )
    
    plan = MEAL_PLAN.get(selected_day, {})
    recettes = RECETTES_LUCA if who == "🏋️ Luca" else RECETTES_SONIA
    
    st.markdown(f"### Menu {JOURS[selected_day]}")
    
    meals = [
        ("🍳 Petit-déjeuner", "petit_dejeuner", "petit_dej"),
        ("🍝 Déjeuner", "dejeuner", "dejeuner"),
        ("🍪 Collation", "collation", "collation"),
        ("🌙 Dîner", "diner", "diner"),
    ]
    
    for title, cat, plan_key in meals:
        recipe = recettes[cat][plan.get(plan_key, 0)]
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(recipe['img'], use_container_width=True)
        with col2:
            st.markdown(f"**{title}**")
            st.markdown(f"### {recipe['nom']}")
            st.markdown(f"🔥 {recipe['kcal']} kcal | 💪 {recipe['prot']}g protéines")
        st.markdown("---")
    
    # Total
    total_kcal = sum(recettes[cat][plan.get(plan_key, 0)]['kcal'] for _, cat, plan_key in meals)
    total_prot = sum(recettes[cat][plan.get(plan_key, 0)]['prot'] for _, cat, plan_key in meals)
    
    color = "#1e40af" if who == "🏋️ Luca" else "#be185d"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {color} 0%, {color}99 100%); 
                color: white; padding: 1.5rem; border-radius: 16px; text-align: center;">
        <h3 style="margin: 0;">📊 Total Journée</h3>
        <p style="font-size: 2rem; margin: 0.5rem 0; font-weight: 700;">{total_kcal} kcal</p>
        <p style="margin: 0;">{total_prot}g protéines</p>
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏋️ LUCA", "🧘 SONIA", "🥗 NUTRITION LUCA", "🥗 NUTRITION SONIA", "📅 PLANNING"])

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
    render_nutrition_luca()

with tab4:
    render_nutrition_sonia()

with tab5:
    render_meal_plan()

st.markdown("---")
st.caption("💪 FitCouple v4.1")
