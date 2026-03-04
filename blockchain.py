import hashlib
import json
import pandas as pd
from time import time
from uuid import uuid4
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': [],
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_transaction(self, age, gender, diagnosis, hospital, claim_amount):
        transaction = {
            "claim_id": str(uuid4()),
            "age": int(age),
            "gender": gender,
            "diagnosis": diagnosis,
            "hospital": hospital,
            "claim_amount": float(claim_amount),
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.get_previous_block()["transactions"].append(transaction)
        return transaction

    def mine_block(self):
        previous_block = self.get_previous_block()
        previous_hash = self.hash(previous_block)
        block = self.create_block(previous_hash)
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i - 1]
            curr = self.chain[i]
            if curr['previous_hash'] != self.hash(prev):
                return False
        return True

    def reset_chain(self):
        self.chain = []
        self.create_block(previous_hash='0')

def load_demo_data(blockchain):
    df = pd.read_csv("insurance.csv")
    df.columns = df.columns.str.strip().str.lower()

    for _, row in df.head(5).iterrows():
        blockchain.add_transaction(
            row["age"],
            row["sex"].capitalize(),
            f"Smoker: {row['smoker']}, Region: {row['region']}",
            "City Hospital",
            row["charges"]
        )
        blockchain.mine_block()
