from flask import (
    jsonify,
    request,
)


from extensions import blockchain


def register():
    params = request.form.to_dict()

    nodes = params.get('nodes')
    if nodes is None:
        return "Error: Please supply a list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Nodes have been registered',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Chain was replaced',
            'new_chain': blockchain.chain,
        }
    else:
        response = {
            'message': 'The chain is authoritative ',
            'chain': blockchain.chain
        }

    return jsonify(response), 200
