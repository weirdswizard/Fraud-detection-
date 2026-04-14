import streamlit as st
import pandas as pd
import joblib

st.title(" Government Scheme Fraud Detection System")

model = joblib.load("model.pkl")

uploaded_file = st.file_uploader("Upload Dataset", type=["csv"])

def highlight_risk(val):
    if "Fraud" in val:
        return "background-color: #ff4d4d; color: black"
    elif "High Risk" in val:
        return "background-color: #ffcc00; color: black"
    else:
        return "background-color: #28a745; color: white"

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    if st.button("Run Analysis"):

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

        df["PredictedFraud"] = model.predict(X)
        df["FraudProbability"] = model.predict_proba(X)[:, 1]

        threshold = 0.35

        fraud_df = df[df["PredictedFraud"] == 1]
        risk_df = df[
            (df["PredictedFraud"] == 0) &
            (df["FraudProbability"] > threshold)
        ]

        st.subheader("Fraud Detection Summary")

        col1, col2 = st.columns(2)

        col1.metric("Fraud Cases", len(fraud_df))
        col2.metric("Potential Future Fraud", len(risk_df))

        fraud_df = fraud_df.sort_values(by="FraudProbability", ascending=False)
        risk_df = risk_df.sort_values(by="FraudProbability", ascending=False)

        with st.expander("View Fraud Users"):
            if not fraud_df.empty:
                st.dataframe(fraud_df[[
                    "ApplicantID",
                    "Name",
                    "ClaimedAmount",
                    "FraudProbability"
                ]])
            else:
                st.write("No fraud users detected")

        with st.expander("View Potential Future Fraud Users"):
            if not risk_df.empty:
                st.dataframe(risk_df[[
                    "ApplicantID",
                    "Name",
                    "ClaimedAmount",
                    "FraudProbability"
                ]])
            else:
                st.write("No future fraud users detected")

        df["RiskStatus"] = df.apply(
            lambda row: "Fraud"
            if row["PredictedFraud"] == 1
            else "High Risk"
            if row["FraudProbability"] > threshold
            else "Normal",
            axis=1
        )

        st.subheader("Detailed Results")

        styled_df = df[[
            "ApplicantID",
            "Name",
            "SchemeType",
            "ClaimedAmount",
            "FraudProbability",
            "RiskStatus"
        ]].style.map(highlight_risk, subset=["RiskStatus"])

        st.dataframe(styled_df)