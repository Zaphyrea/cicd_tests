# Import des librairies uvicorn, pickle, FastAPI, File, UploadFile, BaseModel
from fastapi import FastAPI, File, UploadFile
import uvicorn
import numpy as np 
from pydantic import BaseModel
import pickle
import pandas as pd

import mlflow
import os
import boto3



# Création des tags (un tag par point de terminaison) 
tags = [
       {
            "name": "Hello",
            "description": "Hello World"
        },
       {
            "name": "Predict V1",
            "description": "It will predict if someone has a **sleep disorder** or not, based on gender, age, physical activity level, heart rate, daily steps, blood pressure high, blood pressure low. It will return 1 if the person has a sleep disorder, and 0 if the person does not have a sleep disorder",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/tutorial/metadata/",
            },
        },
       {
            "name": "Predict V2",
            "description": "It will predict if someone has a **sleep disorder** or not, based on physical activity level, heart rate, daily steps. It will return 1 if the person has a sleep disorder, and 0 if the person does not have a sleep disorder"
        }
]

# Chargement des modèles
model_1 = pickle.load(open("model_1.pkl", "rb"))
model_2 = pickle.load(open("model_2.pkl", "rb"))

# Création de l'application
app = FastAPI(
       title="API de prediction",
       description= "Predictions",
       version= "1.0.0",
       openapi_tags= tags
)

# Point de terminaison avec paramètre
@app.get("/hello", tags=["Hello name V1"])
def hello(name: str='World'):
        return {"message": f"Hello {name}"}


# class Credit(BaseModel):
#        Gender : int
#        Age : int
#        Physical_Activity_Level : int
#        Heart_Rate : int
#        Daily_Steps : int
#        BloodPressure_high : float
#        BloodPressure_low : float
#        Sleep_Disorder : int  # It's the target variable

# Création du modèle de données pour le modéle 1 ('Gender', 'Age', 'Physical Activity Level', 'Heart Rate', 'Daily Steps', 'BloodPressure_high', 'BloodPressure_low', 'Sleep Disorder'])
class Credit(BaseModel):
       Gender : int
       Age : int
       Physical_Activity_Level : int
       Heart_Rate : int
       Daily_Steps : int
       BloodPressure_high : float
       BloodPressure_low : float
       Sleep_Disorder : int  # It's the target variable


### Première technique sans appeler directement la classe Credit
# # Point de terminaison : Prédiction 1
# @app.post("/predict", tags=["Predict V1"])
# def predict(credit: Credit):
#     data = dict(credit)  # Convertir l'objet Pydantic en dictionnaire

#     # data = {    # Appel Class au dessus
#     #     'Gender': data['Gender'],
#     #     'Age': data['Age'],
#     #     'Physical Activity Level': data['Physical_Activity_Level'],
#     #     'Heart Rate': data['Heart_Rate'],
#     #     'Daily Steps': data['Daily_Steps'],
#     #     'BloodPressure_high': data['BloodPressure_high'],
#     #     'BloodPressure_low': data['BloodPressure_low'],
#     # }
#     data_df = pd.DataFrame([data])  # Convertir le dictionnaire en DataFrame
#     prediction_1 = model_1.predict(data_df)

#     # Convert the prediction result to a native Python type
#     prediction_1 = prediction_1[0].item()

#     # Save the prediction to a file
#     with open('predictions_model_1.txt', 'a') as f:
#         f.write(str(prediction_1) + '\n')

#     return {"prediction": prediction_1}

### Deuxième technique en appelant la classe Credit
@app.post("/predict", tags=["Predict V1"])
def predict(credit: Credit):
    # gender_numerical = le_gender.transform([credit.Gender])[0]
   
    X_new = [[credit.Gender, credit.Age, credit.Physical_Activity_Level,
              credit.Heart_Rate, credit.Daily_Steps,
              credit.BloodPressure_high, credit.BloodPressure_low]]
   
    prediction_result = model_1.predict(X_new)
    # prediction_result_categorical = le_sleep.inverse_transform([prediction_result])
    return {"prediction": prediction_result.tolist()}
     
# Création du modèle de données pour le modèle 2 ('Physical Activity Level', 'Heart Rate', 'Daily Steps', 'Sleep Disorder')
class Credit_2(BaseModel):
       Physical_Activity_Level : int
       Heart_Rate : int
       Daily_Steps : int
       Sleep_Disorder : int  # It's the target variable

# Point de terminaison : Prédiction 2
@app.post("/predict_2", tags=["Predict V2"])
def predict_2(credit_2: Credit_2):
    data = dict(credit_2)
    data = {
        'Physical Activity Level': data['Physical_Activity_Level'],
        'Heart Rate': data['Heart_Rate'],
        'Daily Steps': data['Daily_Steps'],
    }
    data_df = pd.DataFrame([data])
    prediction_2 = model_2.predict(data_df)

    # Convertir le résultat de la prédiction en un type Python natif (dict, liste, int, float, str, etc.)
    prediction_2 = prediction_2[0].item()

    # Sauvegarder la prédiction dans un fichier pour garder un historique 
    with open('predictions_model_2.txt', 'a') as f:
        f.write(str(prediction_2) + '\n')

    return {"prediction": prediction_2}


# Démarrage de l'application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)