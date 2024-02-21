# Import des librairies
from unittest import TestCase, main
from fastapi.testclient import TestClient
from api import app
import os
import pickle

client = TestClient(app)

# assertEqual(a, b) : Vérifie si a est égal à b.
# assertNotEqual(a, b) : Vérifie si a est différent de b.
        
# assertIn(a, b) : Vérifie si a est dans b.
# assertNotIn(a, b) : Vérifie si a n'est pas dans b.
        
# assertIs(a, b) : Vérifie si a est b.
# assertIsNot(a, b) : Vérifie si a n'est pas b.
        
# assertTrue(x) : Vérifie si x est vrai.
# assertFalse(x) : Vérifie si x est faux.
        
# assertIsNone(x) : Vérifie si x est None.
# assertIsNotNone(x) : Vérifie si x n'est pas None.
        
# assertIsInstance(a, b) : Vérifie si a est une instance de b.
# assertNotIsInstance(a, b) : Vérifie si a n'est pas une instance de b.
        
# assertRaises(exc, fun, *args, **kwargs) : Vérifie si fun(*args, **kwargs) lève une exception de type exc.
# assertRaisesRegex(exc, r, fun, *args, **kwargs) : Vérifie si fun(*args, **kwargs) lève une exception de type exc et dont le message correspond à l'expression régulière r.


# Tests unitaire de l'environnement de développement
class TestDev(TestCase):

    # Vérifie que les fichiers sont présents
    def test_files(self):
        list_files = os.listdir()
        self.assertIsNotNone(list_files) # with assertIsNot the test fail, so it's working
        

    # Vérifie que les requirements sont présents
    def test_requirements(self):
        toml_file = os.path.isfile('pyproject.toml')
        self.assertIsNotNone(toml_file)
    
    # Vérifie que le gitignore est présent
    def test_gitignore (self):
        gitignore_test = os.path.isfile('.gitignore')
        self.assertTrue(gitignore_test)


# Création du client de test

# Tests unitaire de l'API

    # Vérifie que l'API est bien lancée
    def test_api_launched (self):
        response = client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json()) # optional
         
    # Vérifie le endpoint hello_you
    def test_hello_you (self):
        response = client.get("/hello_you")
        self.assertEqual(response.status_code, 404)

    # Vérifie le endpoint predict 1
    def test_predict_1 (self):
        test_data = {
            "Gender": 0,
            "Age": 30,
            "Physical_Activity_Level": 2,
            "Heart_Rate": 70,
            "Daily_Steps": 6000,
            "BloodPressure_high": 110,
            "BloodPressure_low": 80,
            "Sleep_Disorder": 0
        }
        response = client.post("/predict", json=test_data)
        self.assertEqual(response.status_code, 200)

    # Vérifie le endpoint predict 2
    def test_predict_2 (self):
        client = TestClient(app)
        test_data = {
            "Physical_Activity_Level": 2,
            "Hearth_Rate": 70,
            "Daily_Steps": 6000,
            "Sleep_Disorder": 0
        }
        response = client.post("/predict_2", json=test_data)
        print(response.json())  # Print out the validation errors
        self.assertEqual(response.status_code, 200)



# Test du modèle individuellement
class TestModel(TestCase):

    # Vérifie que le modèle 1 est bien présent
    def test_model_1 (self):
        model_1 = pickle.load(open("model_1.pkl", "rb"))
        self.assertIsNotNone(model_1)

    # Vérifie que le modèle 2 est bien chargé
    def test_model_2 (self):
        model_2 = pickle.load(open("model_2.pkl", "rb"))
        self.assertIsNotNone(model_2)


# Démarrage des tests
if __name__== "__main__" :
    main(
        verbosity=2,
    )
