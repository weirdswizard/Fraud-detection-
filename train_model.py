import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv("train_dataset.csv")

df["SchemeType"] = df["SchemeType"].map({
    "Pension": 0,
    "Scholarship": 1,
    "Subsidy": 2,
    "Loan": 3
})

df["AmountTrend"] = df["AmountTrend"].map({
    "Increasing": 1,
    "Stable": 0,
    "Decreasing": -1
})

X = df[[
    "Age",
    "Income",
    "SchemeType",
    "ApplicationCount",
    "TransactionCount",
    "ClaimedAmount",
    "AvgClaimAmount",
    "LocationRisk",
    "DuplicateID",
    "AmountTrend"
]]

y = df["IsFraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

train_acc = model.score(X_train, y_train)
y_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)

print(f"Train Accuracy: {train_acc:.2f}")
print(f"Test Accuracy: {test_acc:.2f}")

joblib.dump(model, "model.pkl")

print("Model trained and saved as model.pkl")