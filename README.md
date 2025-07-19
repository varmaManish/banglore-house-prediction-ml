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


## 1. Clone the Repository

```bash
git clone https://github.com/varmaManish/banglore-house-prediction-ml.git
cd banglore-house-prediction-ml
```
made with ❤️ by Manish Varma

