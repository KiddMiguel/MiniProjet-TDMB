import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from fetch_data import fetch_data_json_in_data
from fetch_data import fetch_data_online
from cach_and_simulation import simulate_high_load_with_cache
from test import test_repeated_executions, stress_test

load_dotenv()

########################## PARTIE TEST A DECOMMENTER POUR TESTER

# stress_test()
# test_repeated_executions()

# Ajuster la taille du layout
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chemin où stocker le fichier JSON
file_path = "./data/movie_ids_09_17_2024.json"
nameFile ='movie_ids_10_16_2024'

option = st.selectbox(
    'Voulez-vous télécharger le fichier JSON ou utiliser les données en ligne ?',
    ('Télécharger le fichier JSON', 'Utiliser les données en ligne')
)

if option == 'Télécharger le fichier JSON':
    nameFile = st.text_input("Entrez le nom du fichier JSON", nameFile)
    if st.button('Télécharger le fichier JSON'):
        # Logique pour télécharger le fichier JSON
        downloaded_file = fetch_data_json_in_data(nameFile, file_path)
        if downloaded_file:
            st.success(f"Téléchargement du fichier réussi")
            with open('./options/option01.py', 'r') as file:
                exec(file.read())
        else:
            st.error("Échec du téléchargement du fichier.")
    
else:
    # Logique pour utiliser les données en ligne
    with open('./options/option02.py', 'r') as file:
        exec(file.read())
    

    