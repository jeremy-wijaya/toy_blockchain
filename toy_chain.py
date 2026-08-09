import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        content = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(content.encode()).hexdigest()

class StableCoinChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.balances = {} # Track who has how much money

    def create_genesis_block(self):
        return Block(0, "Genesis Block: System Initialized", "0")

    def mint(self, user, amount):
        """ Creating coins out of thin air (The Central Bank action) """
        transaction = f"MINT: {amount} USD to {user}"
        new_block = Block(len(self.chain), transaction, self.chain[-1].hash)
        self.chain.append(new_block)
        
        # Update the balance sheet
        self.balances[user] = self.balances.get(user, 0) + amount
        print(f"✅ Minted {amount} USD to {user}")

    def transfer(self, sender, receiver, amount):
        """ Moving coins from one person to another """
        if self.balances.get(sender, 0) < amount:
            print(f"❌ Error: {sender} does not have enough money!")
            return

        transaction = f"TRANSFER: {amount} USD from {sender} to {receiver}"
        new_block = Block(len(self.chain), transaction, self.chain[-1].hash)
        self.chain.append(new_block)
        
        # Update balances
        self.balances[sender] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount
        print(f"✅ Transferred {amount} USD from {sender} to {receiver}")

# --- RUNNING THE TOY ---
coin = StableCoinChain()

# 1. Minting (Creating the money)
coin.mint("Bank_Reserve", 10000) # The bank creates the pool
coin.mint("User_A", 500)         # Give User A some money

# 2. Transferring (The Banking part)
coin.transfer("User_A", "User_B", 200)
coin.transfer("User_A", "User_B", 1000) # This should fail!

print("\n--- Final Balance Sheet ---")
print(coin.balances)

print("\n--- Blockchain Ledger ---")
for block in coin.chain:
    print(f"Block {block.index} | Hash: {block.hash[:10]}... | Data: {block.transactions}")
