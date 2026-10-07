import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


DATABASE_URL = "mysql+pymysql://cnn_user:password@localhost:3306/cnn"

@pytest.fixture(scope="module")
def db_connection():
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    yield connection
    connection.close()

def test_bug_requete_sql_garde_fou(db_connection):
    requete_invalide = text("""
        INSERT INTO predictions (image, commentaire) 
        VALUES ('test_bug.jpg', 'Ceci devrait planter');
    """)
    # On s'attend à la bonne erreur retournée par MySQL
    with pytest.raises(OperationalError):
        db_connection.execute(requete_invalide)

def test_logique_monitoring_anomalies(db_connection):
    # On teste l'anomalie sur le label (car la base interdit de toucher à l'ID)
    db_connection.execute(text("ALTER TABLE predictions MODIFY label INT NULL;"))
    
    db_connection.execute(text("""
        INSERT INTO predictions (image, label, commentaire, modele) 
        VALUES ('anomalie.jpg', NULL, 'Test monitoring', 'CNN');
    """))
    db_connection.commit()

    requete_monitoring = text("SELECT COUNT(*) FROM predictions WHERE label IS NULL;")
    resultat = db_connection.execute(requete_monitoring).scalar()
    
    assert resultat >= 1

    db_connection.execute(text("DELETE FROM predictions WHERE label IS NULL;"))
    db_connection.execute(text("ALTER TABLE predictions MODIFY label INT NOT NULL;"))
    db_connection.commit()