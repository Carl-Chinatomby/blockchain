import json
import hashlib
from time import time
from uuid import uuid4


class BlockChain():

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        """
            Creates a new transaction to go into the next mined blocked

            :param sender: <str> Address of the sender
            :param recipient: <str> Address of the Recipient
            :param amount: <int> amount
            :return <int> The index of the block that will hold this transaction
        """
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            }
        )
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of work Algorithm:
            - Find a number p' such that hash(pp') contains 4 leading zeros
            where p is the previous p'
            - p is the previous proof and p' is the new proof

            :param last_proof: <int>
            :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not
        """
        guess = '{}{}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
