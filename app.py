from flask import Flask, jsonify, request
import pickle
import pandas as pd
from pathlib import Path
from mail import send_email
from maps import get_nearest_hospital, get_google_maps_url
from generate_model import  generate_model

# paths
MODELS_DIR = Path(__file__).parent / "models"

# Initialize model
generate_model()

# Load general model
with open(MODELS_DIR / 'model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

user_data = {
    "123" : {
        "GuardianPhoneNumber": "+94714445555",
        "Velocity": 0.0,
        "Lean": 0.0,
        "Pitch": 0.0,
        "Yaw": 0.0,
        "Longitude": 6.9271,
        "Latitude": 79.8612,
        "Status": "Not Crashed"
    },
}

# POST request
@app.route('/store-user-data', methods=['POST'])
def store_user_data():
    data = request.get_json()
    uid = str(data['uid'])
    user_data[uid]["Velocity"] = float(data["Velocity"])
    user_data[uid]["Lean"] = float(data["Lean"])
    user_data[uid]["Pitch"] = float(data["Pitch"])
    user_data[uid]["Yaw"] = float(data["Yaw"])
    user_data[uid]["Longitude"] = float(data["Longitude"])
    user_data[uid]["Latitude"] = float(data["Latitude"])


    # Predict
    X = pd.DataFrame({
        "Velocity": [user_data[uid]["Velocity"]],
        "Lean": [user_data[uid]["Lean"]],
        "Pitch": [user_data[uid]["Pitch"]],
        "Yaw": [user_data[uid]["Yaw"]],
    })

    prediction = model.predict(X)
    predicted_category = prediction[0]
    
    user_data[uid]["Status"] = predicted_category

    print(f"Predicted category: {predicted_category}")

    if predicted_category == "Crashed":
        # get nearest hospital
        print("Getting nearest hospital")
        name, phone, address = get_nearest_hospital(longitude=user_data[uid]["Longitude"], latitude=user_data[uid]["Latitude"])
        print(name, phone, address)

        # Crash Location
        maps_url = get_google_maps_url(latitude=user_data[uid]["Latitude"], longitude=user_data[uid]["Longitude"])

        # Prepare message body with hospital details and location of crash
        message_body = f"Your loved one has crashed!\n\nHospital: {name}\nContact: {phone}\nAddress: {address}\n\nLocation: {maps_url}"
        
        # send sms to guardian
        print("Sending SMS to guardian")
        send_email(receiver_email="ict18820@sjp.ac.lk", subject="Your loved one has crashed", body=message_body)
        send_email(receiver_email="navinda@yandex.com", subject="Your loved one has crashed", body=message_body)
        
        # send sms to emergency services
        print("Sending SMS to emergency services")


    return user_data[uid]

# GET request
@app.route('/get-user-data', methods=['GET'])
def get_user_data():
    uid = str(request.args.get('uid'))
    return user_data[uid]


app.run(debug=True, port=8080)