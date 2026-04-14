import pandas as pd
import random
from faker import Faker

fake = Faker("en_IN")
random.seed(42)

data = []

num_records = 300

for i in range(num_records):
    applicant_id = f"A{i+1}"
    name = fake.name()

    age = random.randint(18, 65)
    income = random.randint(10000, 50000)
    scheme = random.choice(["Pension", "Scholarship", "Subsidy", "Loan"])

    user_type = random.choices(
        ["normal", "risky", "fraud"],
        weights=[0.5, 0.3, 0.2]
    )[0]

    if user_type == "normal":
        applications = random.randint(1, 3)
        transactions = random.randint(1, 3)
        claimed_amount = random.randint(2000, income)
        location_risk = 0
        duplicate_id = 0

    elif user_type == "risky":
        applications = random.randint(3, 6)
        transactions = random.randint(2, 5)
        claimed_amount = int(income * random.uniform(1.1, 1.6))
        location_risk = random.randint(0, 1)
        duplicate_id = random.randint(0, 1)

    else:
        applications = random.randint(5, 10)
        transactions = random.randint(5, 10)
        claimed_amount = int(income * random.uniform(1.5, 3.0))
        location_risk = 1
        duplicate_id = 1

    avg_amount = int(claimed_amount * random.uniform(0.7, 1.3))

    trend = random.choice(["Increasing", "Stable", "Decreasing"])

    score = 0

    if applications > 4:
        score += 2
    if duplicate_id == 1:
        score += 2
    if claimed_amount > income * 1.5:
        score += 2
    if transactions > 4:
        score += 1
    if location_risk == 1:
        score += 1

    fraud = 1 if score >= 5 else 0

    data.append([
        applicant_id, name, age, income, scheme,
        applications, transactions, claimed_amount,
        avg_amount, location_risk, duplicate_id, trend, fraud
    ])

df = pd.DataFrame(data, columns=[
    "ApplicantID", "Name", "Age", "Income", "SchemeType",
    "ApplicationCount", "TransactionCount", "ClaimedAmount",
    "AvgClaimAmount", "LocationRisk", "DuplicateID",
    "AmountTrend", "IsFraud"
])

df.to_csv("train_dataset.csv", index=False)

print("Training dataset created")