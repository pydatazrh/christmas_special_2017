from uuid import uuid4

from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields

from blockchain import Blockchain

# Instantiate the Blockchain
blockchain = Blockchain()

# Instantiate the Node
app = Flask(__name__)
api = Api(app, version="1.0", title="PyData Zurich Blockchain", description="PyData Zurich Blockchain")

nodes = api.model("Nodes", {
    "nodes": fields.List(fields.String(description="Node url"), description="List of nodes")
})


transaction = api.model("Transaction", {
    "sender": fields.String(description="Sender id"),
    "recipient": fields.String(description="Recipient id"),
    "amount": fields.String(description="Amount to transfer"),
})

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')


@api.route('/mine', endpoint="run the proof of work algorithm")
@api.doc(description="run the proof of work algorithm")
class Miner(Resource):

    def get(self):
        # We run the proof of work algorithm to get the next proof...
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return response


@api.route('/transactions/new')
class TransactionCreator(Resource):

    @api.expect(transaction)
    def post(self):
        values = api.payload

        # Check that the required fields are in the POST'ed data
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

        response = {'message': 'Transaction will be added to Block {}'.format(index)}
        return response


@api.route('/chain')
class Chain(Resource):

    def get(self):
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }

        return response


@api.route('/nodes')
class Nodes(Resource):

    def get(self):
        return list(blockchain.nodes)

@api.route('/nodes/register')
class NodeRegistrar(Resource):

    @api.expect(nodes)
    def post(self):
        values = api.payload

        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400

        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes),
        }
        return response


@api.route('/nodes/resolve')
class NodeResolver(Resource):

    def get(self):
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        return response

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
