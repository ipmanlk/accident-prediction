import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import os
import pickle

DATASET_PATH = Path(__file__).parent / "csv" / "dataset.csv"
MODEL_PATH = Path(__file__).parent / "models" / "model.pkl"

def generate_model():
  # Load the dataset
  data = pd.read_csv(DATASET_PATH)
  data.columns = data.columns.str.strip()

  X = data.drop('Status', axis=1)
  y = data['Status']
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  model = RandomForestClassifier()
  model.fit(X_train, y_train)

  # Export the trained model as a pickle file
  with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

  print("Model has been generated successfully.")