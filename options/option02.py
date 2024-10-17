import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from fetch_data import fetch_data_online, get_movie_details


load_dotenv()

# Dashboard Option 0

st.markdown("<h1 style='text-align: center; width: 100%; font-size: 1.8rem'>Bienvenue sur TDM Online</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; width: 100%; font-size: 1.5rem'>Les plus populaires</h3>", unsafe_allow_html=True)

# Tableau des films populaires
option = [{
    "langage": 'en-US',
    "page": "1",
    "indice": 'popular'
}, {
    "langage": 'fr-FR',
    "page": "1",
    "indice": 'top_rated'
},{
    "langage": 'en-US',
    "page": "1",
    "indice": 'upcoming'
}]

dataPopulaire = fetch_data_online(option[0])
dataTopRated = fetch_data_online(option[1])
dataUpcoming = fetch_data_online(option[2])

name = st.text_input('Rechercher par nom')

if name:
    option = {
        "name": name,
        "include_adult": 'false',
        "language": 'fr-FR',
        "page": "1"
    }
    data = get_movie_details(option)

    if data:
        for i in data['results']:
            with st.expander(f"{i['title']}", expanded=False):
                st.write(f"**Date de sortie**: {i['release_date']}".encode('utf-8').decode('utf-8'))
                st.write(f"**Popularité**: {i['popularity']}".encode('utf-8').decode('utf-8'))
                st.write(f"**Synopsis**: {i['overview']}".encode('utf-8').decode('utf-8'))
    else:
        st.warning("Aucun film trouvé.")      

# Afficher dans un tableau et un graphique les films populaires
if dataPopulaire:
    dfPopulaire = pd.DataFrame(dataPopulaire['results'])
    col1, col2 = st.columns(2)
    
    with col1:
        dfPopulaire_sorted = dfPopulaire.sort_values(by='popularity', ascending=False)
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Films populaires</h4>", unsafe_allow_html=True)
        st.dataframe(dfPopulaire_sorted[['original_title', 'popularity']], width=500 , height=500)
        st.divider()
        
        dfTopRated = pd.DataFrame(dataTopRated['results'])
        dfTopRated_sorted = dfTopRated.sort_values(by='vote_average', ascending=False)
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Films les mieux notés</h4>", unsafe_allow_html=True)
        st.dataframe(dfTopRated_sorted[['original_title', 'vote_average']], width=500, height=500)
        st.divider()
        
        dfUpcoming = pd.DataFrame(dataUpcoming['results'])
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Films à venir</h4>", unsafe_allow_html=True)
        st.dataframe(dfUpcoming[['original_title', 'release_date']], width=500, height=500)
        
    with col2:
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Graphique films populaires</h4>", unsafe_allow_html=True)
        st.bar_chart(dfPopulaire.set_index('original_title')['popularity'], height=500)
        st.divider()
        
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Graphique films les mieux notés</h4>", unsafe_allow_html=True)
        st.bar_chart(dfTopRated.set_index('original_title')['vote_average'], height=500)
        st.divider()
        
        st.markdown("<h4 style='text-align: center; width: 100%; font-size: 1.2rem'>Graphique films à venir</h4>", unsafe_allow_html=True)
        st.bar_chart(dfUpcoming.set_index('original_title')['release_date'], height=500)
else:
    st.error("Échec de la récupération des données.")
    