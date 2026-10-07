import sys
import os
from streamlit.testing.v1 import AppTest

def test_chargement_interface():
    # 1. On calcule le chemin absolu du dossier "client"
    dossier_client = os.path.abspath(os.path.join(os.path.dirname(__file__), "../e5-2026-cnn/client"))
    chemin_app = os.path.join(dossier_client, "app.py")
    
    # 2. On ajoute ce dossier à la liste des chemins que Python connaît
    # Cela permet à app.py de trouver config.py
    sys.path.insert(0, dossier_client)
    
    # 3. On lance le test Streamlit
    at = AppTest.from_file(chemin_app)
    at.run()
    
    # 4. On vérifie qu'il n'y a pas d'erreur rouge à l'écran
    assert not at.exception