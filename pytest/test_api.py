from fastapi.testclient import TestClient
from app.main import app # Import de l'application FastAPI depuis le fichier main.py 

client = TestClient(app)

def test_api_repond_bien():
    response = client.get("/")
    assert response.status_code == 200

def test_prediction_endpoint(tmp_path):
    image_path = tmp_path / "test_image.jpg"
    image_path.write_bytes(b"fausses_donnees_image")

    with open(image_path, "rb") as f:
        
        response = client.post("/predictions/satellite/", files={"file": ("test_image.jpg", f, "image/jpeg")})
    
    # On vérifie que la route existe (on ne veut pas d'erreur 404 "Introuvable")
    assert response.status_code != 404