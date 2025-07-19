from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model and label encoder
model = pickle.load(open('price_model.pkl', 'rb'))
le = pickle.load(open('label_encoder.pkl', 'rb'))
locations = sorted(le.classes_.tolist())
print("LOCATIONS:", locations[:5])  # Debug print

@app.route('/')
def index():
    return render_template('index.html', locations=locations, prediction_text=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = request.form['location']
        total_sqft = float(request.form['sqft'])
        bath = int(request.form['bath'])
        bhk = int(request.form['bhk'])

        location_encoded = le.transform([location])[0]
        features = np.array([[total_sqft, bath, bhk, location_encoded]])
        predicted_price = model.predict(features)[0]

        return render_template(
            'index.html',
            locations=locations,
            prediction_text=f"Estimated Price: ₹ {predicted_price:.2f} Lakhs",
            location_text=f"Location: {location}"
        )
    except Exception as e:
        return render_template(
            'index.html',
            locations=locations,
            prediction_text="Prediction failed. Please check your input.",
            location_text=f"Error: {str(e)}"
        )
# In your app.py, add this route for testing
@app.route('/test')
def test_template():
    test_locations = ['Location1', 'Location2', 'Location3']
    return render_template('index.html', 
                         locations=test_locations,
                         prediction_text="Test Prediction",
                         location_text="Test Location")

if __name__ == '__main__':
    app.run(debug=True)
