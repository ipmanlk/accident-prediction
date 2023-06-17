import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pickle
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

DATASET_PATH = Path(__file__).parent / "csv" / "dataset.csv"
MODEL_PATH = Path(__file__).parent / "models" / "model.pkl"

def generate_model():
  # Load the dataset
  data = pd.read_csv(DATASET_PATH)
  data.columns = data.columns.str.strip()

  # Separate features and target variable
  X = data.drop('Status', axis=1)
  y = data['Status']

  # Perform label encoding on the target variable
  le = LabelEncoder()
  y = le.fit_transform(y)

  # Split the dataset into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Train the model
  classifier = SVC()
  classifier.fit(X_train, y_train)

  # Export the trained model as a pickle file
  with open(MODEL_PATH, 'wb') as f:
    pickle.dump(classifier, f)

  print("Model has been generated successfully.")

def get_label_encoder():
    # Load the dataset
  data = pd.read_csv(DATASET_PATH)
  data.columns = data.columns.str.strip()

  # Separate features and target variable
  y = data['Status']

  # Perform label encoding on the target variable
  le = LabelEncoder()
  y = le.fit_transform(y)

  return le