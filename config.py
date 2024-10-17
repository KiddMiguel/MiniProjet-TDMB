from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker
import json

# Configuration de la base de données SQL
DATABASE_URL = "mysql+pymysql://root:@localhost/tdm"  

# Créer l'engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_movies_table_and_insert_data(json_file_path):
    # Définir la table movies
    metadata = MetaData()
    movies_table = Table(
        'movies', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('title', String(255), nullable=False),
        Column('overview', String(1024)),
        Column('release_date', String(50)),
        Column('vote_average', Float),
        Column('vote_count', Integer),
        Column('adult', Integer),  
        Column('original_title', String(255)),  
        Column('popularity', Float),  
        Column('video', Integer) 
    )

    # Création de la table dans la base de données
    try:
        metadata.create_all(engine)
        print("Table 'movies' créée ou déjà existante.")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")
        return

    # Lire les données du fichier JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies_data = json.load(file)
            print("Données JSON lues avec succès.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON: {e}")
        return

    # Insertion des données dans la table
    try:
        with engine.connect() as connection:
            for movie in movies_data:
                insert_statement = movies_table.insert().values(
                    title=movie['title'],
                    overview=movie.get('overview', ''),
                    release_date=movie.get('release_date', ''),
                    vote_average=movie.get('vote_average', 0.0),
                    vote_count=movie.get('vote_count', 0),
                    adult=int(movie.get('adult', False)),  # Convertir boolean en entier
                    original_title=movie.get('original_title', ''),
                    popularity=movie.get('popularity', 0.0),
                    video=int(movie.get('video', False))  # Convertir boolean en entier
                )
                connection.execute(insert_statement)
            print("Données insérées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans la base de données: {e}")


