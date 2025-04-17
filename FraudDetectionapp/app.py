from flask import Flask, render_template, request
import pandas as pd
from catboost import CatBoostClassifier
from utils.notify import send_sms

app = Flask(__name__)

# Load trained CatBoost model
model = CatBoostClassifier()
model.load_model("model/fraud_detection_catboost_model.cbm")

# Mapping categorical 'type' to numeric values (same as during training)
type_mapping = {
    "CASH_OUT": 1,
    "TRANSFER": 4,
    "DEBIT": 2,
    "PAYMENT": 3,
    "CASH_IN": 0
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    sms_status = None
    try:
        # Extract form data and map 'type' to numeric
        step       = float(request.form['step'])
        type_str   = request.form['type'].upper()
        type_code  = type_mapping.get(type_str, -1)  # default to -1 if not found
        amount     = float(request.form['amount'])
        obo        = float(request.form['oldbalanceOrg'])
        nbo        = float(request.form['newbalanceOrig'])
        obd        = float(request.form['oldbalanceDest'])
        nbd        = float(request.form['newbalanceDest'])

        if type_code == -1:
            raise ValueError(f"Invalid transaction type: {type_str}")

        # Create DataFrame with correct column names & float types
        input_data = pd.DataFrame([{
            'step': step,
            'type': float(type_code),
            'amount': amount,
            'oldbalanceOrg': obo,
            'newbalanceOrig': nbo,
            'oldbalanceDest': obd,
            'newbalanceDest': nbd
        }])

        input_data = input_data.astype('float32')

        # Predict
        pred = model.predict(input_data)[0]
        result = "Fraudulent" if pred == 1 else "Legitimate"

        # SMS notification
        if pred == 1:
            try:
                send_sms("⚠️ Fraud Alert: suspicious transaction detected!")
                sms_status = "SMS sent successfully ✅"
            except Exception as e:
                sms_status = f"SMS failed: {e}"

    except Exception as e:
        result = None
        sms_status = f"Prediction error: {e}"

    return render_template("index.html",
                           prediction=result,
                           sms_status=sms_status)

if __name__ == '__main__':
    app.run(debug=True)
