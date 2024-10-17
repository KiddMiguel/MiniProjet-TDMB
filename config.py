from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd

# Configuration de la base de données SQL
DATABASE_URL = "mysql+pymysql://root:@localhost/tdm"

# Créer l'engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour déclarer les modèles
Base = declarative_base()

# Définir le modèle Movie
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    adult = Column(Integer)  
    original_title = Column(String(255))  
    popularity = Column(Float)  
    video = Column(Integer) 

def create_movies_table_and_insert_data(json_file_path):
    # Création de la table dans la base de données
    try:
        Base.metadata.create_all(engine)
        print("Table 'movies' créée ou déjà existante.")
    except Exception as e:
        print(f"Erreur lors de la création de la table: {e}")
        return

    # Lire les données du fichier JSON en utilisant pandas
    try:
        movies_data = pd.read_json(json_file_path, lines=True)  # Utiliser 'lines=True' pour les fichiers avec plusieurs lignes
        print("Données JSON lues avec succès.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON: {e}")
        return

    # Insertion des données dans la table
    session = SessionLocal()
    try:
        for index, movie in movies_data.iterrows():
            new_movie = Movie(
                id=movie['id'],
                title=movie['original_title'],
                adult=int(movie.get('adult', False)),  
                original_title=movie.get('original_title', ''),
                popularity=movie.get('popularity', 0.0),
                video=int(movie.get('video', False))
            )
            session.add(new_movie)

        session.commit()  # Commencer la transaction
        print("Données insérées avec succès.")
    except Exception as e:
        session.rollback()  # Annuler la transaction en cas d'erreur
        print(f"Erreur lors de l'insertion des données dans la base de données: {e}")
    finally:
        session.close()  # Toujours fermer la session