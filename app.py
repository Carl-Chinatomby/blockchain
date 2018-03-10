from textwrap import dedent
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import BlockChain


app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    # run proof of work algo to get next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # give a reward for finding the proof
    # send is 0 to signify that the node is a new coin mined
    blockchain.new_transaction(
        sender='0',
        recipient=node_identifier,
        amount=1
    )

    # add new block to chain
    previous_hash = blockchain.hash(last_block)
    new_block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'New Block Forged',
        'index': new_block['index'],
        'transactions': new_block['transactions'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    """
    params = request.get_json()

    # verify required params
    required_params = ('sender', 'recipient', 'amount')
    if not all(required_param in params for required_param in required_params):
        return 'Missing Params', 400   #TODO Fix this response

    index = blockchain.new_transaction(params['sender'], params['recipient'], params['amount'])
    response = {'message': 'Transaction will be added to the block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
