import hashlib
import json
import os
import time


class Transaction:
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        required_fields = ["version", "locktime", "vin", "vout"]
        if not all(field in self.data for field in required_fields):
            return False
        # Check if each 'vin' entry has a 'txid' field
        for vin in self.data.get("vin", []):
            if "txid" not in vin:
                return False
        return True


class Block:
    def __init__(self, transactions):
        self.transactions = transactions
        self.previous_hash = (
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
        self.nonce = 0
        self.timestamp = int(time.time())
        self.difficulty_target = (
            "0000ffff0000000000000000000000000000000000000000000000000000000"
        )

    def calculate_hash(self):
        header = f"{self.previous_hash}{self.timestamp}{self.nonce}"
        assert len(header) <= 80, "Block header exceeds 80 bytes"
        return hashlib.sha256(header.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.calculate_hash()[:difficulty] != target:
            self.nonce += 1


def main():
    transactions = []
    try:
        for filename in os.listdir("mempool"):
            with open(f"mempool/{filename}", "r") as file:
                data = json.load(file)
                tx = Transaction(data)
                if tx.is_valid():
                    transactions.append(tx)
    except FileNotFoundError:
        print("Error: The 'mempool' directory does not exist.")
        return
    except json.JSONDecodeError:
        print("Error: A file in the 'mempool' directory could not be decoded as JSON.")
        return

    block = Block(transactions)
    try:
        block.mine_block(4)  # Assuming a difficulty of 4 for simplicity
    except Exception as e:
        print(f"Error: An error occurred while mining the block: {e}")
        return

    try:
        with open("output.txt", "w") as file:
            file.write(f"Block Header: {block.calculate_hash()}\n")
            file.write("Coinbase Transaction: Simplified for demonstration\n")
            for tx in block.transactions:
                if tx.is_valid():
                    # Assuming the first 'vin' entry's 'txid' is the one we're interested in
                    txid = tx.data["vin"][0]["txid"] if tx.data["vin"] else "N/A"
                    file.write(f"Transaction ID: {txid}\n")
    except IOError:
        print("Error: Unable to write to 'output.txt'.")


if __name__ == "__main__":
    main()
