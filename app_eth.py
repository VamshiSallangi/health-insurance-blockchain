from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from web3 import Web3
import json
import uuid
from datetime import datetime
from blockchain import Blockchain, load_demo_data

app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret"

# --------------------------------------------------
# ✅ Connect to Ganache
# --------------------------------------------------
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
if not w3.is_connected():
    raise SystemExit("❌ Cannot connect to Ganache at http://127.0.0.1:7545")

# Use unlocked account 0 (Ganache default)
w3.eth.default_account = w3.eth.accounts[0]

# --------------------------------------------------
# ✅ Load contract ABI and address
# --------------------------------------------------
with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)
with open('contract_address.txt', 'r') as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize blockchain (for off-chain view)
blockchain = Blockchain()

# --------------------------------------------------
# ✅ Routes
# --------------------------------------------------
@app.route('/')
def index():
    total = contract.functions.getTotalClaims().call()
    return render_template('eth_index.html', total=total)


@app.route('/add_claim', methods=['GET', 'POST'])
def add_claim():
    if request.method == 'POST':
        claim_id = str(uuid.uuid4())
        patient_name = request.form['patient_name']
        age = request.form['age']
        gender = request.form['gender']
        hospital = request.form['hospital']
        diagnosis = request.form['diagnosis']
        claim_amount = request.form['claim_amount']
        date_of_service = request.form.get('date_of_service', datetime.now().strftime("%Y-%m-%d"))

        tx_hash = contract.functions.addClaim(
            claim_id, patient_name, int(age), gender, hospital, diagnosis, int(claim_amount), date_of_service
        ).transact({'from': w3.eth.accounts[0]})

        w3.eth.wait_for_transaction_receipt(tx_hash)
        flash(f"✅ Claim added to Ethereum — Tx Hash: {tx_hash.hex()}", "success")

        # Also log in local blockchain for view
        blockchain.add_transaction(age, gender, diagnosis, hospital, claim_amount)
        blockchain.mine_block()

        return redirect(url_for('view_claims'))

    return render_template('add_claim.html')


@app.route('/view_claims')
def view_claims():
    claims = []
    for block in blockchain.chain:
        for txn in block["transactions"]:
            claims.append(txn)
    return render_template("view_claims.html", claims=claims)


@app.route("/view_blockchain")
def view_blockchain():
    return render_template("view_blockchain.html", chain=blockchain.chain)


@app.route("/clear_blockchain")
def clear_blockchain():
    blockchain.reset_chain()
    flash("🗑 Blockchain cleared successfully!", "warning")
    return redirect(url_for("index"))


@app.route("/load_demo_csv")
def load_demo_csv():
    load_demo_data(blockchain)
    flash("📂 Demo data successfully loaded!", "info")
    return redirect(url_for("view_blockchain"))


# --------------------------------------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
