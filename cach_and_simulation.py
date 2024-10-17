import asyncio
import aiohttp
import time
import cachetools
from cachetools import TTLCache

routes = [
    "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1",
    "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
]

# Créer un cache avec une durée de vie de 1 heure (3600 secondes)
cache = TTLCache(maxsize=1000, ttl=3600)

# Fonction pour envoyer une requête HTTP avec gestion du cache
async def fetch_with_cache(session, url):
    # Vérifier si la réponse est déjà en cache
    if url in cache:
        print(f"Récupéré du cache : {url}")
        return cache[url]

    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                # Stocker la réponse dans le cache
                cache[url] = data
                return data
            else:
                return f"Erreur {response.status}: {url}"
    except Exception as e:
        return f"Erreur de connexion: {e}"

# Fonction principale pour gérer les requêtes en parallèle avec cache
async def fetch_all_with_cache(routes):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_cache(session, route) for route in routes]
        results = await asyncio.gather(*tasks)
        return results

# Simuler une charge élevée avec cache
def simulate_high_load_with_cache():
    start_time = time.time()

    # Exécuter les requêtes avec cache
    results = asyncio.run(fetch_all_with_cache(routes))

    # Temps écoulé
    duration = time.time() - start_time
    print(f"Requêtes effectuées en {duration:.2f} secondes.")

    # Afficher les résultats
    for result in results:
        print(result)

