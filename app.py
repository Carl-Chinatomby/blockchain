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
    return 'mining'

@app.route('/transactions/new', methods=['POST'])
def new_transation():
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
    return jsonify(response, 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
