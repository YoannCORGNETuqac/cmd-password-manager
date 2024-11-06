import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pysqlcipher3 import dbapi2 as sqlite

DB_PATH = 'data/passwords.db'

def init_database(path, password):
    # Connecter à la base de données
    conn = sqlite.connect(path)
    cursor = conn.cursor()

    # Définir la clé de chiffrement
    cursor.execute(f"PRAGMA key = {password};")

    # Créer une table
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT);')
    cursor.execute("INSERT INTO users (name) VALUES ('Alice');")
    conn.commit()
    conn.close()

def open_database(path, password):
    """
    Accède à une base de données SQLite chiffrée avec SQLCipher.
    """
    # Connexion à la base de données chiffrée
    conn = sqlite.connect(path)
    cursor = conn.cursor()

    # Définir la clé de déchiffrement (doit être la même que celle utilisée pour chiffrer)
    cursor.execute(f"PRAGMA key = '{password}';")

    # Vérifier l'accès en lisant les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables dans la base de données :", tables)

    return conn, cursor



if __name__ == "__main__":
    
    load_dotenv()
    password = os.getenv('DB_PASSWORD')

    if not os.path.isfile(DB_PATH):
        init_database("db/data.sqlite", password)

    open_database("db/data.sqlite", password)

    