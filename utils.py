import pandas as pd
import uuid
from datetime import datetime

# ✅ Function to add claim to blockchain
def add_claim_to_blockchain(contract, account, patient, amount, description):
    tx = contract.functions.addClaim(patient, amount, description).build_transaction({
        'from': account,
        'gas': 2000000,
        'gasPrice': 0
    })
    tx_hash = contract.web3.eth.send_transaction(tx)
    return tx_hash

# ✅ Get all claims from blockchain
def get_all_claims(contract):
    total = contract.functions.getClaimCount().call()
    claims = []
    for i in range(total):
        c = contract.functions.getClaim(i).call()
        claims.append({
            "id": i,
            "patient": c[0],
            "amount": c[1],
            "description": c[2],
            "timestamp": c[3]
        })
    return claims

# ✅ Load insurance.csv and upload data into blockchain
def load_demo_csv(contract, account):
    try:
        df = pd.read_csv("insurance.csv")

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Check for expected columns
        expected_cols = {"age", "sex", "bmi", "children", "smoker", "region", "charges"}
        if not expected_cols.issubset(df.columns):
            return f"❌ Missing required columns. Found: {list(df.columns)}"

        # Load top 10 claims for demo
        for _, row in df.head(10).iterrows():
            patient = f"Patient_{row['age']}_{row['region']}"
            amount = int(float(row["charges"]))
            description = f"{row['sex']}, BMI {row['bmi']}, Smoker: {row['smoker']}, Region: {row['region']}"
            add_claim_to_blockchain(contract, account, patient, amount, description)

        return "✅ Successfully loaded 10 demo claims from insurance.csv!"

    except Exception as e:
        return f"⚠️ Error loading dataset: {str(e)}"
