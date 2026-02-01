import streamlit as st
import json
import os

# --- CONFIGURATION ET DONNÉES ---
DB_FILE = "recettes.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(recipes):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=4, ensure_ascii=False)

# Initialisation de la session
if "recipes" not in st.session_state:
    st.session_state.recipes = load_data()

# --- INTERFACE ---
st.set_page_config(page_title="Mon Livre de Recettes", page_icon="🍳")
st.title("🍳 Mon Livre de Recettes Numérique")

menu = ["Voir les recettes", "Ajouter une recette"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- LOGIQUE : VOIR LES RECETTES ---
if choice == "Voir les recettes":
    st.header("Mes Recettes")
    
    if not st.session_state.recipes:
        st.info("Votre livre est vide. Commencez par ajouter une recette !")
    else:
        # Recherche et Filtre
        search = st.text_input("Rechercher une recette ou un ingrédient...")
        categories = list(set([r['cat'] for r in st.session_state.recipes]))
        cat_filter = st.multiselect("Filtrer par catégorie", categories)

        for i, recipe in enumerate(st.session_state.recipes):
            # Logique de filtrage simple
            if search.lower() in recipe['nom'].lower() or search.lower() in recipe['ing']:
                if not cat_filter or recipe['cat'] in cat_filter:
                    with st.expander(f"{recipe['nom']} ({recipe['cat']})"):
                        st.subheader("Ingrédients")
                        st.write(recipe['ing'])
                        st.subheader("Instructions")
                        st.write(recipe['inst'])
                        if st.button("Supprimer", key=f"del_{i}"):
                            st.session_state.recipes.pop(i)
                            save_data(st.session_state.recipes)
                            st.rerun()

# --- LOGIQUE : AJOUTER UNE RECETTE ---
elif choice == "Ajouter une recette":
    st.header("Nouvelle Création")
    
    with st.form("add_form", clear_on_submit=True):
        nom = st.text_input("Nom du plat")
        cat = st.selectbox("Catégorie", ["Entrée", "Plat", "Dessert", "Boisson", "Snack"])
        ing = st.text_area("Ingrédients (un par ligne)")
        inst = st.text_area("Instructions de préparation")
        
        submit = st.form_submit_button("Sauvegarder la recette")
        
        if submit:
            if nom and ing and inst:
                new_recipe = {"nom": nom, "cat": cat, "ing": ing, "inst": inst}
                st.session_state.recipes.append(new_recipe)
                save_data(st.session_state.recipes)
                st.success(f"Recette '{nom}' ajoutée avec succès !")
            else:
                st.error("Veuillez remplir tous les champs.")
