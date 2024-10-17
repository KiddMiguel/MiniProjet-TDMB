import os
import requests
import gzip
from dotenv import load_dotenv
import time
from cachetools import TTLCache
from cach_and_simulation import fetch_with_cache
from config import create_movies_table_and_insert_data

load_dotenv()

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + os.getenv('API_KEY')
}

# Créer un cache avec une durée de vie de 1 heure (3600 secondes)
cache = TTLCache(maxsize=1000, ttl=3600)
url = os.getenv('API_URL') 
urlOnline = os.getenv('API_URL_ONLINE')

# Fonction pour appeler l'API avec gestion des erreurs
def error_api(url, headers=None, params=None, max_retries=5, backoff_factor=1):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            
            # Gérer les erreurs 429, 500, etc.
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"Erreur 429: Trop de requêtes. Réessayer après {retry_after} secondes.")
                time.sleep(retry_after)
                
            elif response.status_code in [400, 401, 403, 404]:
                print(f"Erreur {response.status_code}: {response.reason}. Vérifiez la requête ou l'authentification.")
                return None
            elif response.status_code in [500, 502, 503, 504]:
                print(f"Erreur {response.status_code}: Erreur du serveur. Réessayer après {backoff_factor} secondes.")
                time.sleep(backoff_factor)
                backoff_factor *= 2
            else:
                print(f"Erreur inconnue: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f'Erreur de connexion: {e}. Réessayer après {backoff_factor} secondes.')
            time.sleep(backoff_factor)
        retries += 1
        print(f"Nombre de tentatives restantes: {max_retries - retries}")
    return None


def fetch_data_json_in_data(option, file_path):
    if url is None:
        raise ValueError("L'URL de l'API n'est pas définie. Assurez-vous que la variable API_URL est présente dans le fichier .env")
    
    print('Downloading data...')
    try:
        # EN DECOMMENTANT CETTE LIGNE, VOUS POUVEZ UTILISER LA FONCTION error_api POUR GÉRER LES ERREURS
        # data = error_api(url + option + '.json.gz', headers=headers)
        data = requests.get(url + option + '.json.gz')
        if data:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Sauvegarder le fichier compressé
            gz_file_path = file_path.replace('.json', '.json.gz')
            with open(gz_file_path, 'wb') as file:
                file.write(data.content)

            print('Data downloaded successfully')

            # Décompresser le fichier
            with gzip.open(gz_file_path, 'rb') as f_in:
                with open(file_path, 'wb') as f_out:
                    f_out.writelines(f_in)


            print('Data decompressed successfully')
            
            # Supprimer le fichier gzip après décompression
            os.remove(gz_file_path)

            # Créer la table de films et insérer les données
            # create_movies_table_and_insert_data(file_path)
            
            return file_path

    except Exception as e:
        print(f"Erreur lors du téléchargement ou de la décompression des données : {e}")
        return None



def fetch_data_online(option):
    try:
        # Utiliser error_api au lieu de requests.get
        data = error_api(urlOnline + "movie/" + option["indice"] + "?language=" + option["langage"] + "&page=" + option["page"], headers=headers)
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None

def get_movie_details(option):
    try:
        # Utiliser error_api au lieu de requests.get
        data = error_api(urlOnline + "search/movie?query=" + option['name'] + "&include_adult=" + str(option["include_adult"]).lower() + "&language=" + option["language"] + "&page=" + option["page"], headers=headers)
        return data
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None

