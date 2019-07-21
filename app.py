from flask import Flask

from views import (
    nodes,
    chain,
    transactions,
)

app = Flask(__name__)


@app.route('/mine', methods=['GET'])
def my_transactions():
    return transactions.mine()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    """
    transactions.new()


@app.route('/chain', methods=['GET'])
def full_chain():
    return chain.full_chain()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    return nodes.register()


@app.route('/nodes/resolve', methods=['GET'])
def resolve_nodes():
    return nodes.consensus()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
