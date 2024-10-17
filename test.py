import time
from cachetools import TTLCache
from cach_and_simulation import fetch_with_cache, simulate_high_load_with_cache

def test_repeated_executions():
    print("Test: Exécutions répétées avec des pauses")
    
    # Première exécution (sans cache)
    print("Exécution 1 (les données ne sont pas encore en cache) :")
    simulate_high_load_with_cache()
    print("\n")

    # Pause avant la deuxième exécution
    time.sleep(2)

    # Deuxième exécution (les données devraient être en cache)
    print("Exécution 2 (les données devraient être récupérées du cache) :")
    simulate_high_load_with_cache()
    print("\n")

    # Pause avant la troisième exécution
    time.sleep(2)

    # Troisième exécution (toujours avec cache)
    print("Exécution 3 (cache actif) :")
    simulate_high_load_with_cache()
    print("\n")



def stress_test():
    print("Test de stress :")
    
    # Boucler 100 fois pour simuler une forte charge
    for i in range(10):
        print(f"Exécution {i + 1} :")
        simulate_high_load_with_cache()
        print("\n")
        time.sleep(1)  # Pause pour ne pas saturer instantanément

