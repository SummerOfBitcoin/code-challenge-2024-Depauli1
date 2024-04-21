import os
import json
import hashlib
import time


# This function reads transactions from the mempool directory
def read_transactions(directory):
    transactions = []
    try:
        # Iterates over files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                # Opens and read each transaction file
                with open(os.path.join(directory, filename), "r") as file:
                    transactions.append(json.load(file))
    except Exception as e:
        print(f"Error reading the transactions: {e}")
    return transactions


# Function to validate transactions
def validate_transactions(transactions):
    valid_transactions = []
    for tx in transactions:
        # Checks for necessary fields and exclude coinbase transactions
        if "vin" in tx and "vout" in tx and not tx["vin"][0]["is_coinbase"]:
            valid_transactions.append(tx)
    return valid_transactions


def calculate_fee(transactions):
    total_fee = 0
    for tx in transactions:
        # Assuming each transaction has a 'value' field in 'vout'
        # and a 'fee' field that is a percentage of the value
        for vout in tx["vout"]:
            total_fee += vout["value"] * 0.01  # Assuming a 1% fee
    return total_fee


# Function to mine a block
def mine_block(transactions, difficulty_target):
    nonce = 0
    # Constructs the block header
    while True:
        block_header = f"Version: 1\nPrevious Block Hash: 0000000000000000000000000000000000000000000000000000000000000000\nMerkle Root: 0000000000000000000000000000000000000000000000000000000000000000\nTimestamp: {int(time.time())}\nBits: {difficulty_target}\nNonce: {nonce}\n"
        hash_result = hashlib.sha256(block_header.encode()).hexdigest()

        # Checks if the hash meets the difficulty target
        if hash_result < difficulty_target:
            return nonce, hash_result
        nonce += 1


# Function to write out the output
def write_output(nonce, hash_result, transactions):
    if nonce is None or hash_result is None or transactions is None:
        print("Error: Nonce, hash_result, or transactions is None.")
        return

    total_fee = calculate_fee(transactions)
    block_space_utilization = len(transactions)

    try:
        with open("output.txt", "w") as file:
            file.write(f"Block Header: {nonce}, {hash_result}\n")
            file.write(f"Total Fee Collected: {total_fee}\n")
            file.write(f"Block Space Utilization: {block_space_utilization}\n")
            file.write("Coinbase Transaction\n")
            for tx in transactions:
                file.write(f"{tx['vin'][0]['txid']}\n")
    except Exception as e:
        print(f"Error writing to output.txt: {e}")


# Main function to start the process
def main():
    transactions = read_transactions("mempool")

    # Validate transactions by checking for necessary fields

    valid_transactions = validate_transactions(transactions)

    # Attempt to mine a block with the valid transactions
    nonce, hash_result = mine_block(
        valid_transactions,
        "0000ffff000000000000000000000000000000000000000000000000000000000",
    )

    # Writes the output to output.txt
    write_output(nonce, hash_result, valid_transactions)


# Calls the main function to start the process

if __name__ == "__main__":
    main()
