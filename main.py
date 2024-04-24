import os
import json
import hashlib
import time


def read_transactions(directory):
    transactions = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                with open(os.path.join(directory, filename), "r") as file:
                    transactions.append(json.load(file))
    except Exception as e:
        print(f"Error reading the transactions: {e}")
    return transactions


def validate_transactions(transactions):
    valid_transactions = []
    for tx in transactions:
        if "vin" in tx and "vout" in tx and not tx["vin"][0]["is_coinbase"]:
            valid_transactions.append(tx)
    return valid_transactions


def calculate_fee(transactions):
    total_fee = 0
    for tx in transactions:
        for vout in tx["vout"]:
            total_fee += vout["value"] * 0.01
    return total_fee


def mine_block(transactions, difficulty_target):
    nonce = 0
    while True:
        block_header = f"Version: 1\nPrevious Block Hash: 0000000000000000000000000000000000000000000000000000000000000000\nMerkle Root: 0000000000000000000000000000000000000000000000000000000000000000\nTimestamp: {int(time.time())}\nBits: {difficulty_target}\nNonce: {nonce}\n"
        hash_result = hashlib.sha256(block_header.encode()).hexdigest()
        if hash_result < difficulty_target:
            return nonce, hash_result
        nonce += 1


def write_output(nonce, hash_result, transactions, difficulty_target):
    if nonce is None or hash_result is None or transactions is None:
        print("Error: Nonce, hash_result, or transactions is None.")
        return

    total_fee = calculate_fee(transactions)
    block_space_utilization = len(transactions)

    try:
        with open("output.txt", "w") as file:
            file.write(
                f"Block Header:\nVersion: 1\nPrevious Block Hash: 0000000000000000000000000000000000000000000000000000000000000000\nMerkle Root: 0000000000000000000000000000000000000000000000000000000000000000\nTimestamp: {int(time.time())}\nBits: {difficulty_target}\nNonce: {nonce}\n"
            )
            file.write(f"Total Fee Collected: {total_fee}\n")
            file.write(f"Block Space Utilization: {block_space_utilization}\n")
            file.write("Coinbase Transaction\n")
            for tx in transactions:
                file.write(f"{tx['vin'][0]['txid']}\n")
    except Exception as e:
        print(f"Error writing to output.txt: {e}")


def main():
    transactions = read_transactions("mempool")
    valid_transactions = validate_transactions(transactions)
    difficulty_target = "0000ffff00000000000000000000000000000000000000000000000000000000"  # Define difficulty target here
    nonce, hash_result = mine_block(valid_transactions, difficulty_target)
    write_output(nonce, hash_result, valid_transactions, difficulty_target)


if __name__ == "__main__":
    main()
