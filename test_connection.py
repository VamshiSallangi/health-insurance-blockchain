from web3 import Web3

# Use the same port that Ganache shows (usually 7545)
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

print("Connected to Blockchain:", w3.is_connected())
