import json
import hashlib
from time import time
from uuid import uuid4
from urllib.parse import urlparse
import requests


class BlockChain():

    def __init__(self):
        self.nodes = set()
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

        #self.current_transactions = []
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

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: <str> URL address of node
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given block chain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid else False
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if (block['previous_hash'] != self.hash(last_block)) or \
                    (not self.valid_proof(last_block['proof'], block['proof'])):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        A consensus algorithm that resolves conflicts by replacing chains with the
        longest one in the network.

        :return: <bool> True if chain was replaced else False
        """
        neighbors = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get('http://{}/chain'.format(node))

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']


                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

            if new_chain:
                self.chain = new_chain
                return True

        return False
