README: Interactive Classroom Blockchain/Crypto Simulator
==========================================

Overview
--------
This Python script is an interactive blockchain simulator for classroom use.
Students can explore the basics of blockchain and cryptocurrency, including:
- Mining and proof-of-work (PoW)
- Mining rewards and bootstrap blocks
- Transactions between users
- Forks and consensus resolution
- Self-sustaining blockchain behavior

Features
--------
- Fixed users and initial balances (default 100 coins per user)
- First user replaced with the student running the script
- Bootstrap mining: early blocks mined even without transactions
- Self-sustaining phase: mining only allowed when transactions exist
- Proof-of-work visualization with multiple guesses per block
- Fork simulation: shows two miners competing for the same block
- Menu-driven interface:
    1) Add Transaction
    2) Mine Pending Transactions
    3) View Balances
    4) View Blockchain
    5) Check Validity
    6) Quit
    7) Simulate Fork Mining

Requirements
------------
-Python 3.x
-No external dependencies

Usage
-----
1. Run the script in a terminal:
     python3 crypto_sim.py
2. Enter your miner name (this name will be the first user in the menu)
3. Use the menu options to add transactions, mine blocks, view balances, or simulate forks
4. Observe how balances, mining, and forks work

Classroom Activities
-------------------
-Activity 1: Add transactions and mine blocks to see balances update
-Activity 2: Simulate forks and discuss how consensus resolves conflicts
-Activity 3: Mine until the bootstrap amount is reached, then observe self-sustaining mining

Notes
-----
-Educational purposes only; does not implement real cryptographic security
-Runs entirely locally; no real cryptocurrency is used
-Suitable for interactive classroom demonstrations
