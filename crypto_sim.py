import hashlib, json, time

# --- CONFIG ---
USERS = ["Alice", "Bob", "Carol", "Dave", "Eve"]
INITIAL_BALANCE = 100       # Each user starts with this balance
BOOTSTRAP_AMOUNT = 200      # Coins mined before self-sustaining phase
MINING_REWARD = 50
DIFFICULTY = 3              # Number of leading zeros required in hash


# --- BLOCK & BLOCKCHAIN ---
class Block:
    def __init__(self, index, previous_hash, transactions, difficulty, nonce=0, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = timestamp or time.time()

    def header(self):
        data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }
        return json.dumps(data, sort_keys=True)

    def hash(self):
        return hashlib.sha256(self.header().encode()).hexdigest()


class Blockchain:
    def __init__(self, users):
        genesis = Block(0, "0"*64, [], DIFFICULTY)
        self.chain = [genesis]
        self.pending = []
        self.difficulty = DIFFICULTY
        self.reward = MINING_REWARD
        self.total_mined = 0
        self.users = users
        # Initialize balances
        self.balances = {user: INITIAL_BALANCE for user in users}

    def last_block(self):
        return self.chain[-1]

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev = self.chain[i-1]
            cur = self.chain[i]
            if cur.previous_hash != prev.hash():
                return False
            if not cur.hash().startswith("0"*cur.difficulty):
                return False
        return True

    def show_chain(self):
        for b in self.chain:
            print(f"Block {b.index}: hash {b.hash()[:20]}... | prev {b.previous_hash[:10]}...")
            print(f"  Transactions: {b.transactions}")

    # --- TRANSACTIONS ---
    def add_transaction(self, sender_idx, recipient_idx, amount):
        sender = self.users[sender_idx]
        recipient = self.users[recipient_idx]
        if sender == recipient:
            print("⚠️ Sender and recipient cannot be the same.")
            return False
        if self.get_balance(sender) < amount:
            print(f"⚠️ {sender} does not have enough balance! Current balance: {self.get_balance(sender)}")
            return False
        tx = {"sender": sender, "recipient": recipient, "amount": amount}
        self.pending.append(tx)
        print(f"✅ Transaction added: {sender} -> {recipient} : {amount}")
        return True

    # --- PROOF OF WORK ---
    def proof_of_work(self, block):
        target = "0" * block.difficulty
        guesses = 0
        while True:
            guesses += 1
            h = block.hash()
            if h.startswith(target):
                print(f"\n✅ Block mined after {guesses} guesses!")
                return block
            block.nonce += 1
            if guesses % 5000 == 0:
                block.timestamp = time.time()
                print(".", end="", flush=True)

    # --- MINING ---
    def mine_pending(self, miner):
        # Bootstrap phase: allow mining even with no pending transactions
        if not self.pending:
            if self.total_mined < BOOTSTRAP_AMOUNT:
                print("⛏️ Bootstrapping: mining reward-only block...")
                transactions = [{"sender": "NETWORK", "recipient": miner, "amount": self.reward}]
            else:
                print("⚠️ No pending transactions. Mining paused until new transactions arrive.")
                return
        else:
            # Include pending transactions + reward
            transactions = self.pending + [{"sender": "NETWORK", "recipient": miner, "amount": self.reward}]

        new_block = Block(len(self.chain), self.last_block().hash(), transactions, self.difficulty)
        mined = self.proof_of_work(new_block)
        self.chain.append(mined)
        self.pending = []

        # Update balances
        for tx in transactions:
            sender = tx["sender"]
            recipient = tx["recipient"]
            amount = tx["amount"]
            if sender != "NETWORK":
                self.balances[sender] -= amount
            self.balances[recipient] = self.balances.get(recipient, 0) + amount

        # Update total mined coins
        for tx in transactions:
            if tx["sender"] == "NETWORK":
                self.total_mined += tx["amount"]

        print(f"✅ Block {mined.index} mined by {miner}! Hash: {mined.hash()[:20]}...")
        print(f"Total coins mined: {self.total_mined}")
        if self.total_mined >= BOOTSTRAP_AMOUNT:
            print("🎉 Currency is now self-sustaining. Future mining requires transactions.")

    # --- FORK SIMULATION ---
    def fork_mining_demo(self):
        if not self.pending:
            print("⚠️ No pending transactions for fork demo.")
            return

        # Miner1 mining
        print("\nMiner1 is mining...")
        block_miner1 = Block(len(self.chain), self.last_block().hash(), 
                             self.pending + [{"sender":"NETWORK","recipient":"Miner1","amount":self.reward}], self.difficulty)
        mined1 = self.proof_of_work(block_miner1)

        # Miner2 mining
        print("\nMiner2 is mining...")
        block_miner2 = Block(len(self.chain), self.last_block().hash(), 
                             self.pending + [{"sender":"NETWORK","recipient":"Miner2","amount":self.reward}], self.difficulty)
        mined2 = self.proof_of_work(block_miner2)

        # Resolve fork: append first mined block
        self.chain.append(mined1)
        self.balances["Miner1"] = self.balances.get("Miner1", 0) + self.reward
        self.total_mined += self.reward
        print(f"\n✅ Miner1's block appended to the chain: {mined1.hash()[:20]}...")
        print(f"Miner2's block is abandoned due to fork resolution: {mined2.hash()[:20]}...")

        # Clear pending transactions (only included in winning block)
        self.pending = []


# --- MENU ---
def menu():
    print("=== Interactive Classroom Blockchain Simulator ===")
    miner = input("Enter your miner name: ") or "Miner1"

    # Replace first user with the active miner
    if miner not in USERS:
        USERS[0] = miner

    bc = Blockchain(USERS)

    while True:
        print("\nMenu:")
        print("1) Add Transaction")
        print("2) Mine Pending Transactions")
        print("3) View Balances")
        print("4) View Blockchain")
        print("5) Check Validity")
        print("6) Quit")
        print("7) Simulate Fork Mining")
        choice = input("> ").strip()

        if choice == "1":
            print("\nSelect sender:")
            for idx, user in enumerate(USERS):
                print(f"{idx}) {user}")
            sender_idx = int(input("> "))
            print("Select recipient:")
            for idx, user in enumerate(USERS):
                print(f"{idx}) {user}")
            recipient_idx = int(input("> "))
            amount = int(input("Amount: "))
            bc.add_transaction(sender_idx, recipient_idx, amount)

        elif choice == "2":
            bc.mine_pending(miner)

        elif choice == "3":
            print("\nBalances:")
            for user in USERS:
                print(f"{user}: {bc.get_balance(user)}")

        elif choice == "4":
            bc.show_chain()

        elif choice == "5":
            print("Blockchain valid?", bc.is_valid())

        elif choice == "6":
            print("Goodbye!")
            break

        elif choice == "7":
            bc.fork_mining_demo()

        else:
            print("Invalid option.")


# --- RUN ---
if __name__ == "__main__":
    menu()

