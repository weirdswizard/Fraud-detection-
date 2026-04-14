# Proactive Fraud Detection System for Government Schemes

## Overview

This project is a machine learning-based system designed to detect fraudulent activities in government schemes and identify users who are likely to commit fraud in the future. The system analyzes applicant behavior and classifies users as Fraud, High Risk, or Normal.

---

## Tech Stack

* Python
* Pandas
* Scikit-learn
* Streamlit

---

## Project Structure

```
project-folder/
│
├── train_dataset.csv
├── train_model.py
├── app.py
├── model.pkl
└── README.md
```

---

## How to Run

### Install dependencies

```
pip install pandas scikit-learn streamlit faker
```

### Generate training dataset

```
python generate_train_data.py
```

### Train the model

```
python train_model.py
```

### Run the application

```
python -m streamlit run app.py
```

---

## Usage

* Upload a dataset through the web interface
* Run analysis to detect fraud and potential future fraud
* View results in summary and detailed formats
