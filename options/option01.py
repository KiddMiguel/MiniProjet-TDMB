import streamlit as st
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Dashboard Option 01

st.markdown("<h1 style='text-align: center; width: 100%; font-size: 1.8rem'>Bienvenue sur TDM Avec votre fichier</h1>", unsafe_allow_html=True)

# Récupérer les données mais par 100 lignes
df = pd.read_json('./data/movie_ids_09_17_2024.json', lines=True, chunksize=100).__next__()

# Function pour charger les données par chunk (100 lignes)
def load_chunk(start_idx, chunk_size=100):
    chunk = pd.read_json('./data/movie_ids_09_17_2024.json', lines=True, chunksize=chunk_size)
    for i, part in enumerate(chunk):
        if i == start_idx // chunk_size:
            return part
    return pd.DataFrame() 


# Recherche par ID
# movie_id = st.text_input('Rechercher par ID')

# if movie_id:
#     movie_details = df[df['id'] == int(movie_id)]
#     if not movie_details.empty:
#         with st.expander("Détails du film"):
#             st.write(movie_details)
#     else:
#         st.write("Aucun film trouvé avec cet ID.")
    
# Pagination
rows_per_page = 100
total_rows = 1000000  # Assuming we know the total number of rows
page = st.number_input("Page", min_value=1, max_value=(total_rows // rows_per_page) + 1, value=1)

start_idx = (page - 1) * rows_per_page
df = load_chunk(start_idx, rows_per_page)

df = df.replace({True: 'Oui', False: 'Non'})

# Afficher uniquement les colonnes utiles
st.dataframe(df[['original_title', 'popularity']])


# Graphiques
st.bar_chart(df['popularity'])

