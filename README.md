# 🏠 Bangalore House Price Prediction ML App

A web-based machine learning application built with **Flask** that predicts house prices in Bangalore based on key features such as location, total square footage, number of bathrooms, and BHK (bedrooms).

---

## 📊 Dataset

- **Source**: [Bangalore House Price Data](https://www.kaggle.com/amitabhajoy/bengaluru-house-price-data)
- The dataset contains:
  - `location`
  - `total_sqft`
  - `bath`
  - `bhk`
  - `price` (target variable)

---

## 🧠 Machine Learning Model

- **Algorithm**: Linear Regression
- **Input Features**:
  - Total square footage
  - Number of bathrooms
  - Number of bedrooms (BHK)
  - Location (label encoded)
- **Preprocessing**:
  - Null value handling
  - Categorical encoding using `LabelEncoder`
  - Feature scaling where necessary

---

## 📁 Project Structure

app.py # Main Flask backend
├── templates/
│ └── index.html # Frontend HTML template
├── static/ # Optional static files
├── price_model.pkl # Trained model file
├── label_encoder.pkl # Saved LabelEncoder for location
├── Bengaluru_House_Data.csv # Raw dataset
├── requirements.txt # List of dependencies
└── README.md # This file

### 1. Clone the Repository

```bash
git clone https://github.com/varmaManish/banglore-house-prediction-ml.git
cd banglore-house-prediction-ml

ade with ❤️ by Manish Varma
