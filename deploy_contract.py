from solcx import compile_standard, install_solc
from web3 import Web3
import json
import os

# ✅ 1. Install Solidity compiler (only if not already installed)
install_solc('0.8.19')

# ✅ 2. Read the Solidity contract
contract_path = r"C:\projects\Claims\contracts\HealthInsurance.sol"
with open(contract_path, 'r', encoding='utf-8') as f:
    contract_source = f.read()

# ✅ 3. Compile contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"HealthInsurance.sol": {"content": contract_source}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.19",
)

# ✅ 4. Save compiled contract to a file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# ✅ 5. Extract bytecode & ABI
bytecode = compiled_sol["contracts"]["HealthInsurance.sol"]["HealthInsurance"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["HealthInsurance.sol"]["HealthInsurance"]["abi"]

# ✅ 6. Connect to local Ganache blockchain
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
print("🔗 Connected to Blockchain:", w3.is_connected())

# ✅ 7. Use your Ganache account
chain_id = 1337
my_address = "0xECC1229DA3809DB61213Ef1A4eAfD49de2928F25"  # ⚠️ Replace this with your Ganache address
private_key = "0x6d3078ab9a91c33207b6d0de1c4930c4cc8197ca7fe3cedf04b3ce514aa9eeea"      # ⚠️ Replace this with your Ganache private key

# ✅ 8. Create contract object
HealthInsurance = w3.eth.contract(abi=abi, bytecode=bytecode)

# ✅ 9. Build transaction
nonce = w3.eth.get_transaction_count(my_address)
transaction = HealthInsurance.constructor().build_transaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce,
    "gas": 2000000,
    "gasPrice": w3.to_wei("50", "gwei"),
})

# ✅ 10. Sign and send transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("🚀 Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# ✅ Deployment successful
print("✅ Contract Deployed Successfully!")
print("📄 Contract Address:", tx_receipt.contractAddress)

# Save ABI to file
with open("contract_abi.json", "w") as f:
    json.dump(abi, f)

# Save contract address to file
with open("contract_address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)

print("✅ ABI and address saved for Flask app.")

