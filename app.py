from blockchain import Blockchain, load_demo_data

from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
import json
import pandas as pd
from utils import add_claim_to_blockchain, get_all_claims, load_demo_csv
blockchain = Blockchain()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))

# ✅ Load contract ABI
with open("contract_abi.json") as f:
    abi = json.load(f)

# ✅ Load deployed contract address from file
with open("contract_address.txt") as f:
    contract_address = Web3.to_checksum_address(f.read().strip())

# ✅ Connect to contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Default account
account = w3.eth.accounts[0]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/load_demo_csv")
def load_demo():
    msg = load_demo_csv(contract, account)
    flash(msg, "info")
    return redirect(url_for("view_claims"))
@app.route("/clear_blockchain")
def clear_blockchain():
    blockchain.reset_chain()
    flash("✅ Blockchain cleared successfully!", "success")
    return redirect(url_for("view_blockchain"))


@app.route("/add_claim", methods=["GET", "POST"])
def add_claim():
    if request.method == "POST":
        patient = request.form["patient"]
        amount = int(request.form["amount"])
        description = request.form["description"]

        tx_hash = add_claim_to_blockchain(contract, account, patient, amount, description)
        flash(f"✅ Claim added. Tx Hash: {tx_hash.hex()}", "success")
        return redirect(url_for("view_claims"))

    return render_template("add_claim.html")
@app.route("/reset_chain")
def reset_chain():
    blockchain.reset_chain()
    return "✅ Blockchain has been reset successfully!"
@app.route("/view_blockchain")
def view_blockchain():
    try:
        # Load your blockchain data (adjust filename if different)
        with open("blockchain.json", "r") as f:
            chain = json.load(f)
    except FileNotFoundError:
        chain = []

    return render_template("view_blockchain.html", chain=chain)


@app.route("/view_claims")
def view_claims():
    claims = get_all_claims(contract)
    return render_template("view_claims.html", claims=claims)


if __name__ == "__main__":
    app.run(debug=True)
