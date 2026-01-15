import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import json

# Configuration de la page
st.set_page_config(
    page_title="Fitness Luca & Sonia",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour mobile
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 10px;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect('fitness_data.db')
    c = conn.cursor()
    
    # Table pour le suivi du poids
    c.execute('''CREATE TABLE IF NOT EXISTS weight_tracking
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT,
                  weight REAL,
                  belly_cm REAL,
                  notes TEXT)''')
    
    # Table pour les entraînements
    c.execute('''CREATE TABLE IF NOT EXISTS workouts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT,
                  workout_type TEXT,
                  duration INTEGER,
                  exercises TEXT,
                  notes TEXT)''')
    
    # Table pour les recettes
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  category TEXT,
                  calories_per_serving REAL,
                  protein REAL,
                  carbs REAL,
                  fat REAL,
                  ingredients TEXT,
                  instructions TEXT,
                  servings INTEGER)''')
    
    # Table pour le suivi alimentaire
    c.execute('''CREATE TABLE IF NOT EXISTS meal_tracking
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  date TEXT,
                  meal_type TEXT,
                  recipe_id INTEGER,
                  servings REAL)''')
    
    conn.commit()
    conn.close()

# Initialiser les recettes par défaut si vide
def init_default_recipes():
    conn = sqlite3.connect('fitness_data.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recipes")
    if c.fetchone()[0] == 0:
        default_recipes = [
            # Petit-déjeuner
            ("Porridge protéiné", "Petit-déjeuner", 350, 25, 45, 8,
             json.dumps(["80g flocons d'avoine", "250ml lait écrémé", "30g whey protéine", "1 banane", "10g miel"]),
             "1. Cuire les flocons avec le lait\n2. Ajouter la whey hors du feu\n3. Garnir de banane et miel", 1),
            
            ("Oeufs brouillés avocat", "Petit-déjeuner", 420, 28, 15, 30,
             json.dumps(["3 oeufs entiers", "1/2 avocat", "2 tranches pain complet", "Sel, poivre"]),
             "1. Brouiller les oeufs à feu doux\n2. Toaster le pain\n3. Écraser l'avocat sur le pain\n4. Servir ensemble", 1),
            
            ("Smoothie bowl", "Petit-déjeuner", 380, 22, 55, 10,
             json.dumps(["200g fruits rouges surgelés", "1 banane", "200ml lait d'amande", "30g whey", "30g granola"]),
             "1. Mixer fruits, banane, lait et whey\n2. Verser dans un bol\n3. Garnir de granola", 1),
            
            # Déjeuner
            ("Poulet grillé légumes", "Déjeuner", 450, 45, 25, 18,
             json.dumps(["200g blanc de poulet", "200g brocoli", "150g patate douce", "1 c.s huile d'olive", "Épices"]),
             "1. Griller le poulet assaisonné\n2. Cuire patate douce au four 25min\n3. Vapeur pour brocoli\n4. Assembler", 1),
            
            ("Bowl saumon quinoa", "Déjeuner", 520, 38, 42, 22,
             json.dumps(["150g saumon", "100g quinoa cuit", "100g edamame", "1/2 avocat", "Sauce soja", "Graines de sésame"]),
             "1. Cuire le quinoa\n2. Griller le saumon\n3. Assembler avec edamame et avocat\n4. Assaisonner", 1),
            
            ("Wrap dinde crudités", "Déjeuner", 380, 32, 35, 12,
             json.dumps(["1 tortilla complète", "120g blanc de dinde", "Laitue", "Tomate", "Concombre", "2 c.s houmous"]),
             "1. Étaler houmous sur tortilla\n2. Ajouter dinde et crudités\n3. Rouler serré", 1),
            
            # Dîner
            ("Cabillaud haricots verts", "Dîner", 320, 35, 18, 12,
             json.dumps(["180g cabillaud", "200g haricots verts", "100g riz basmati", "Citron", "Herbes"]),
             "1. Cuire le riz\n2. Poêler le cabillaud avec citron\n3. Vapeur pour haricots\n4. Servir", 1),
            
            ("Salade composée protéinée", "Dîner", 350, 30, 20, 18,
             json.dumps(["150g thon en conserve", "2 oeufs durs", "Salade verte", "Tomates cerises", "Olives", "Vinaigrette légère"]),
             "1. Cuire les oeufs\n2. Assembler la salade\n3. Émietter le thon\n4. Assaisonner", 1),
            
            ("Soupe lentilles légumes", "Dîner", 280, 18, 38, 6,
             json.dumps(["150g lentilles corail", "2 carottes", "1 oignon", "2 tomates", "Cumin", "Bouillon"]),
             "1. Faire revenir oignon\n2. Ajouter légumes coupés\n3. Ajouter lentilles et bouillon\n4. Cuire 25min", 2),
            
            # Collations
            ("Yaourt grec fruits", "Collation", 180, 15, 20, 5,
             json.dumps(["200g yaourt grec 0%", "100g fruits frais", "10g miel"]),
             "Mélanger le tout", 1),
            
            ("Shake protéiné", "Collation", 200, 30, 15, 3,
             json.dumps(["30g whey protéine", "300ml lait écrémé", "1/2 banane"]),
             "Mixer tous les ingrédients", 1),
            
            ("Amandes et fruits secs", "Collation", 180, 6, 15, 12,
             json.dumps(["20g amandes", "20g noix", "30g raisins secs"]),
             "Mélanger et déguster", 1),
        ]
        
        c.executemany('''INSERT INTO recipes 
                        (name, category, calories_per_serving, protein, carbs, fat, ingredients, instructions, servings)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', default_recipes)
        conn.commit()
    conn.close()

# Fonctions CRUD
def add_weight(user, weight, belly_cm, notes):
    conn = sqlite3.connect('fitness_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO weight_tracking (user, date, weight, belly_cm, notes) VALUES (?, ?, ?, ?, ?)",
              (user, date.today().isoformat(), weight, belly_cm, notes))
    conn.commit()
    conn.close()

def get_weight_history(user):
    conn = sqlite3.connect('fitness_data.db')
    df = pd.read_sql_query(f"SELECT * FROM weight_tracking WHERE user = '{user}' ORDER BY date", conn)
    conn.close()
    return df

def add_workout(user, workout_type, duration, exercises, notes):
    conn = sqlite3.connect('fitness_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO workouts (user, date, workout_type, duration, exercises, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (user, date.today().isoformat(), workout_type, duration, json.dumps(exercises), notes))
    conn.commit()
    conn.close()

def get_workout_history(user):
    conn = sqlite3.connect('fitness_data.db')
    df = pd.read_sql_query(f"SELECT * FROM workouts WHERE user = '{user}' ORDER BY date DESC", conn)
    conn.close()
    return df

def get_recipes():
    conn = sqlite3.connect('fitness_data.db')
    df = pd.read_sql_query("SELECT * FROM recipes", conn)
    conn.close()
    return df

def add_recipe(name, category, calories, protein, carbs, fat, ingredients, instructions, servings):
    conn = sqlite3.connect('fitness_data.db')
    c = conn.cursor()
    c.execute("""INSERT INTO recipes 
                (name, category, calories_per_serving, protein, carbs, fat, ingredients, instructions, servings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (name, category, calories, protein, carbs, fat, json.dumps(ingredients), instructions, servings))
    conn.commit()
    conn.close()

# Initialisation
init_db()
init_default_recipes()

# Header
st.markdown('<div class="main-header">💪 Fitness Tracker - Luca & Sonia 💪</div>', unsafe_allow_html=True)

# Navigation principale
tab1, tab2, tab3 = st.tabs(["🏋️ Luca", "🧘 Sonia", "🥗 Nutrition"])

# ===================== ONGLET LUCA =====================
with tab1:
    st.header("Programme de Luca")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Poids actuel", "88 kg", "Objectif: 90 kg")
    with col2:
        st.metric("Taille", "1m95", "")
    with col3:
        st.metric("IMC", f"{88/(1.95**2):.1f}", "Normal")
    
    st.markdown("---")
    
    # Objectifs de Luca
    st.subheader("🎯 Objectifs")
    objectives = {
        "Perdre du ventre": "🔥",
        "Développer les bras": "💪",
        "Renforcer les abdos": "🏆",
        "Muscler le dos": "🎯",
        "Cardio (vélo/course)": "🚴"
    }
    
    cols = st.columns(5)
    for i, (obj, icon) in enumerate(objectives.items()):
        with cols[i]:
            st.markdown(f"**{icon} {obj}**")
    
    st.markdown("---")
    
    # Programme d'entraînement
    st.subheader("📋 Programme hebdomadaire")
    
    program_luca = {
        "Lundi": {"type": "Push (Pecs/Épaules/Triceps)", "exercices": [
            "Développé couché 4x10", "Développé militaire 3x12", "Dips 3x12", 
            "Élévations latérales 3x15", "Extensions triceps 3x12"]},
        "Mardi": {"type": "Cardio + Abdos", "exercices": [
            "Vélo 30min HIIT", "Crunch 4x20", "Planche 3x60s", 
            "Russian twist 3x20", "Mountain climbers 3x30"]},
        "Mercredi": {"type": "Pull (Dos/Biceps)", "exercices": [
            "Tractions 4x8", "Rowing barre 4x10", "Tirage vertical 3x12",
            "Curl biceps 3x12", "Curl marteau 3x12"]},
        "Jeudi": {"type": "Repos actif", "exercices": [
            "Marche 30min", "Étirements 20min"]},
        "Vendredi": {"type": "Full body + Cardio", "exercices": [
            "Squats 3x12", "Soulevé de terre 3x10", "Pompes 3x15",
            "Course 20min", "Gainage 3x45s"]},
        "Samedi": {"type": "Cardio long", "exercices": [
            "Vélo 45-60min endurance", "ou Course 30-40min"]},
        "Dimanche": {"type": "Repos", "exercices": ["Récupération complète"]}
    }
    
    for jour, details in program_luca.items():
        with st.expander(f"**{jour}** - {details['type']}"):
            for ex in details['exercices']:
                st.write(f"• {ex}")
    
    st.markdown("---")
    
    # Suivi du poids
    st.subheader("📊 Suivi du poids")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("weight_form_luca"):
            new_weight = st.number_input("Poids (kg)", min_value=50.0, max_value=150.0, value=88.0, step=0.1)
            belly = st.number_input("Tour de ventre (cm)", min_value=50.0, max_value=150.0, value=90.0, step=0.5)
            notes = st.text_input("Notes")
            submitted = st.form_submit_button("Enregistrer")
            if submitted:
                add_weight("Luca", new_weight, belly, notes)
                st.success("Enregistré !")
                st.rerun()
    
    with col2:
        weight_df = get_weight_history("Luca")
        if not weight_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=weight_df['date'], y=weight_df['weight'], 
                                    mode='lines+markers', name='Poids',
                                    line=dict(color='#667eea', width=3)))
            fig.add_hline(y=90, line_dash="dash", line_color="green", 
                         annotation_text="Objectif: 90kg")
            fig.update_layout(title="Évolution du poids", xaxis_title="Date", yaxis_title="Poids (kg)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de poids enregistrée. Commencez votre suivi !")
    
    st.markdown("---")
    
    # Enregistrer un entraînement
    st.subheader("✅ Enregistrer un entraînement")
    
    with st.form("workout_form_luca"):
        col1, col2 = st.columns(2)
        with col1:
            workout_type = st.selectbox("Type d'entraînement", 
                                       ["Push", "Pull", "Cardio", "Full body", "Abdos", "Repos actif"])
        with col2:
            duration = st.number_input("Durée (minutes)", min_value=10, max_value=180, value=60)
        
        exercises_done = st.multiselect("Exercices effectués", 
                                        ["Développé couché", "Tractions", "Dips", "Vélo", "Course",
                                         "Crunch", "Planche", "Squats", "Rowing", "Curl biceps"])
        workout_notes = st.text_area("Notes sur la séance")
        
        if st.form_submit_button("Enregistrer la séance"):
            add_workout("Luca", workout_type, duration, exercises_done, workout_notes)
            st.success("Séance enregistrée !")
            st.rerun()
    
    # Historique
    workout_history = get_workout_history("Luca")
    if not workout_history.empty:
        st.subheader("📜 Historique des séances")
        st.dataframe(workout_history[['date', 'workout_type', 'duration', 'notes']].head(10), 
                    use_container_width=True)

# ===================== ONGLET SONIA =====================
with tab2:
    st.header("Programme de Sonia")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Poids actuel", "78 kg", "Objectif: 63-68 kg")
    with col2:
        st.metric("Taille", "1m50", "")
    with col3:
        imc_sonia = 78/(1.50**2)
        st.metric("IMC", f"{imc_sonia:.1f}", "À réduire")
    
    st.markdown("---")
    
    # Objectifs de Sonia
    st.subheader("🎯 Objectifs")
    objectives_sonia = {
        "Perdre 10-15 kg": "⚖️",
        "Affiner le ventre": "🔥",
        "Tonifier les bras": "💪",
        "Affiner les cuisses": "🦵",
        "Renforcer le fessier": "🍑"
    }
    
    cols = st.columns(5)
    for i, (obj, icon) in enumerate(objectives_sonia.items()):
        with cols[i]:
            st.markdown(f"**{icon} {obj}**")
    
    st.markdown("---")
    
    # Calcul des besoins caloriques
    st.subheader("🔢 Besoins caloriques estimés")
    
    # Métabolisme de base (formule Mifflin-St Jeor)
    bmr_sonia = 10 * 78 + 6.25 * 150 - 5 * 30 - 161  # Estimation âge 30 ans
    maintenance = bmr_sonia * 1.4  # Activité légère à modérée
    deficit = maintenance - 500  # Déficit pour perdre ~0.5kg/semaine
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Métabolisme de base", f"{bmr_sonia:.0f} kcal")
    with col2:
        st.metric("Maintenance", f"{maintenance:.0f} kcal")
    with col3:
        st.metric("Objectif perte", f"{deficit:.0f} kcal", "-500 kcal/jour")
    
    st.markdown("---")
    
    # Programme d'entraînement
    st.subheader("📋 Programme hebdomadaire")
    
    program_sonia = {
        "Lundi": {"type": "Bas du corps + Fessiers", "exercices": [
            "Squats 4x15", "Fentes marchées 3x12/jambe", "Hip thrust 4x15",
            "Abducteurs 3x20", "Montées de genoux 3x30"]},
        "Mardi": {"type": "Cardio HIIT", "exercices": [
            "HIIT 25min (30s effort/30s repos)", "Jumping jacks", "Burpees modifiés",
            "Mountain climbers", "Squat jumps"]},
        "Mercredi": {"type": "Haut du corps + Core", "exercices": [
            "Pompes sur genoux 3x12", "Rowing haltères 3x12", "Curl biceps 3x15",
            "Dips sur chaise 3x10", "Planche 3x30s"]},
        "Jeudi": {"type": "Cardio modéré", "exercices": [
            "Marche rapide 45min", "ou Vélo 30min", "Étirements 15min"]},
        "Vendredi": {"type": "Full body circuit", "exercices": [
            "Circuit 3 tours:", "15 squats", "10 pompes", "20 crunch",
            "15 fentes", "30s planche", "1min repos entre tours"]},
        "Samedi": {"type": "Fessiers focus + Cardio", "exercices": [
            "Donkey kicks 4x20/côté", "Fire hydrants 4x20/côté", "Glute bridge 4x20",
            "Marche/vélo 30min"]},
        "Dimanche": {"type": "Repos actif", "exercices": [
            "Yoga/étirements 30min", "Marche légère"]}
    }
    
    for jour, details in program_sonia.items():
        with st.expander(f"**{jour}** - {details['type']}"):
            for ex in details['exercices']:
                st.write(f"• {ex}")
    
    st.markdown("---")
    
    # Suivi du poids
    st.subheader("📊 Suivi du poids")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("weight_form_sonia"):
            new_weight_s = st.number_input("Poids (kg)", min_value=40.0, max_value=120.0, value=78.0, step=0.1, key="weight_sonia")
            belly_s = st.number_input("Tour de ventre (cm)", min_value=50.0, max_value=130.0, value=85.0, step=0.5, key="belly_sonia")
            notes_s = st.text_input("Notes", key="notes_sonia")
            submitted_s = st.form_submit_button("Enregistrer")
            if submitted_s:
                add_weight("Sonia", new_weight_s, belly_s, notes_s)
                st.success("Enregistré !")
                st.rerun()
    
    with col2:
        weight_df_s = get_weight_history("Sonia")
        if not weight_df_s.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=weight_df_s['date'], y=weight_df_s['weight'],
                                    mode='lines+markers', name='Poids',
                                    line=dict(color='#e91e63', width=3)))
            fig.add_hline(y=65, line_dash="dash", line_color="green",
                         annotation_text="Objectif: ~65kg")
            fig.update_layout(title="Évolution du poids", xaxis_title="Date", yaxis_title="Poids (kg)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune donnée de poids enregistrée. Commencez votre suivi !")
    
    st.markdown("---")
    
    # Enregistrer un entraînement
    st.subheader("✅ Enregistrer un entraînement")
    
    with st.form("workout_form_sonia"):
        col1, col2 = st.columns(2)
        with col1:
            workout_type_s = st.selectbox("Type d'entraînement",
                                         ["Bas du corps", "Haut du corps", "Cardio HIIT", 
                                          "Cardio modéré", "Full body", "Fessiers", "Repos actif"])
        with col2:
            duration_s = st.number_input("Durée (minutes)", min_value=10, max_value=120, value=45, key="dur_sonia")
        
        exercises_done_s = st.multiselect("Exercices effectués",
                                          ["Squats", "Fentes", "Hip thrust", "Pompes", "Planche",
                                           "HIIT", "Marche", "Vélo", "Crunch", "Glute bridge"])
        workout_notes_s = st.text_area("Notes sur la séance", key="notes_workout_sonia")
        
        if st.form_submit_button("Enregistrer la séance"):
            add_workout("Sonia", workout_type_s, duration_s, exercises_done_s, workout_notes_s)
            st.success("Séance enregistrée !")
            st.rerun()
    
    # Historique
    workout_history_s = get_workout_history("Sonia")
    if not workout_history_s.empty:
        st.subheader("📜 Historique des séances")
        st.dataframe(workout_history_s[['date', 'workout_type', 'duration', 'notes']].head(10),
                    use_container_width=True)

# ===================== ONGLET NUTRITION =====================
with tab3:
    st.header("🥗 Nutrition & Recettes")
    
    # Sous-navigation
    nutrition_tab = st.radio("", ["📖 Recettes", "➕ Ajouter une recette", "📊 Macros quotidiennes"],
                            horizontal=True)
    
    if nutrition_tab == "📖 Recettes":
        st.subheader("Recettes disponibles")
        
        # Calculateur de portions
        st.markdown("### 🧮 Calculateur de portions")
        col1, col2 = st.columns(2)
        with col1:
            nb_personnes = st.number_input("Nombre de personnes", min_value=1, max_value=10, value=2)
        with col2:
            category_filter = st.selectbox("Catégorie", ["Toutes", "Petit-déjeuner", "Déjeuner", "Dîner", "Collation"])
        
        st.markdown("---")
        
        recipes_df = get_recipes()
        
        if category_filter != "Toutes":
            recipes_df = recipes_df[recipes_df['category'] == category_filter]
        
        for _, recipe in recipes_df.iterrows():
            with st.expander(f"**{recipe['name']}** - {recipe['category']} ({recipe['calories_per_serving']:.0f} kcal/portion)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Ingrédients:**")
                    ingredients = json.loads(recipe['ingredients'])
                    for ing in ingredients:
                        # Calculer pour le nombre de personnes
                        st.write(f"• {ing} (x{nb_personnes})")
                    
                    st.markdown("**Instructions:**")
                    st.write(recipe['instructions'])
                
                with col2:
                    st.markdown("**Macros par portion:**")
                    st.metric("Calories", f"{recipe['calories_per_serving']:.0f} kcal")
                    st.metric("Protéines", f"{recipe['protein']:.0f}g")
                    st.metric("Glucides", f"{recipe['carbs']:.0f}g")
                    st.metric("Lipides", f"{recipe['fat']:.0f}g")
                    
                    st.markdown(f"**Pour {nb_personnes} personnes:**")
                    st.write(f"Total: {recipe['calories_per_serving'] * nb_personnes:.0f} kcal")
    
    elif nutrition_tab == "➕ Ajouter une recette":
        st.subheader("Ajouter une nouvelle recette")
        
        with st.form("new_recipe"):
            name = st.text_input("Nom de la recette")
            category = st.selectbox("Catégorie", ["Petit-déjeuner", "Déjeuner", "Dîner", "Collation"])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                calories = st.number_input("Calories/portion", min_value=0, max_value=2000, value=300)
            with col2:
                protein = st.number_input("Protéines (g)", min_value=0, max_value=100, value=20)
            with col3:
                carbs = st.number_input("Glucides (g)", min_value=0, max_value=200, value=30)
            with col4:
                fat = st.number_input("Lipides (g)", min_value=0, max_value=100, value=10)
            
            ingredients_text = st.text_area("Ingrédients (un par ligne)")
            instructions = st.text_area("Instructions")
            servings = st.number_input("Nombre de portions", min_value=1, max_value=10, value=1)
            
            if st.form_submit_button("Ajouter la recette"):
                if name and ingredients_text:
                    ingredients_list = [i.strip() for i in ingredients_text.split('\n') if i.strip()]
                    add_recipe(name, category, calories, protein, carbs, fat, 
                              ingredients_list, instructions, servings)
                    st.success(f"Recette '{name}' ajoutée !")
                    st.rerun()
                else:
                    st.error("Veuillez remplir au moins le nom et les ingrédients")
    
    else:  # Macros quotidiennes
        st.subheader("📊 Objectifs macros quotidiens")
        
        user_select = st.selectbox("Sélectionner le profil", ["Luca", "Sonia"])
        
        if user_select == "Luca":
            st.markdown("### Objectifs pour Luca (Prise de masse sèche)")
            
            # Calcul besoins Luca (maintenance + léger surplus)
            bmr_luca = 10 * 88 + 6.25 * 195 - 5 * 30 + 5  # Estimation
            maintenance_luca = bmr_luca * 1.6  # Activité élevée
            target_luca = maintenance_luca + 200  # Léger surplus
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories", f"{target_luca:.0f}", "+200 surplus")
            with col2:
                st.metric("Protéines", f"{88 * 2:.0f}g", "2g/kg")
            with col3:
                st.metric("Glucides", f"{target_luca * 0.45 / 4:.0f}g", "45%")
            with col4:
                st.metric("Lipides", f"{target_luca * 0.25 / 9:.0f}g", "25%")
            
            st.markdown("""
            **Conseils pour Luca:**
            - Protéines réparties sur 4-5 repas
            - Glucides autour des entraînements
            - Éviter les sucres simples pour perdre le ventre
            - Privilégier les protéines maigres (poulet, poisson, oeufs)
            """)
            
        else:
            st.markdown("### Objectifs pour Sonia (Perte de poids)")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories", "1400-1500", "-500 déficit")
            with col2:
                st.metric("Protéines", f"{78 * 1.6:.0f}g", "1.6g/kg")
            with col3:
                st.metric("Glucides", "130-150g", "Modérés")
            with col4:
                st.metric("Lipides", "45-55g", "Essentiels")
            
            st.markdown("""
            **Conseils pour Sonia:**
            - Privilégier les aliments rassasiants (légumes, protéines)
            - Éviter les calories liquides
            - Manger lentement pour favoriser la satiété
            - Collation protéinée pour éviter les fringales
            - Boire minimum 2L d'eau par jour
            """)
        
        st.markdown("---")
        
        # Exemple de journée type
        st.subheader("🍽️ Exemple de journée type")
        
        if user_select == "Luca":
            meal_plan = {
                "Petit-déjeuner (7h)": "Porridge protéiné + 1 banane",
                "Collation (10h)": "Shake protéiné",
                "Déjeuner (12h30)": "Poulet grillé + patate douce + légumes",
                "Collation (16h)": "Yaourt grec + amandes",
                "Dîner (19h30)": "Saumon + riz + haricots verts",
                "Post-training": "Shake protéiné si entraînement"
            }
        else:
            meal_plan = {
                "Petit-déjeuner (8h)": "Oeufs brouillés + 1 tranche pain complet",
                "Collation (10h30)": "Yaourt grec 0% + fruits",
                "Déjeuner (12h30)": "Salade protéinée (poulet/thon) + légumes",
                "Collation (16h)": "Poignée d'amandes",
                "Dîner (19h)": "Poisson + légumes vapeur",
            }
        
        for meal, content in meal_plan.items():
            st.write(f"**{meal}:** {content}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    💪 Fitness Tracker - Luca & Sonia | Créé avec ❤️ | 
    <em>Persévérance et régularité sont les clés du succès !</em>
</div>
""", unsafe_allow_html=True)
