from flask import Flask, Response, request
from broker import create_transaction

app = Flask(__name__)

@app.route('/create-transaction', methods=['POST'])
def endpoint_create_transaction():
    '''
    Endpoint for forwarding the transaction to the broker
    '''
    # get the request body
    request_data = request.get_json()
    # only forward transaction if request body is correct
    if "type" in request_data and "stock_id" in request_data and "user_id" in request_data \
        and (request_data["type"] == "buy" or request_data["type"] == "sell"):
        transaction = create_transaction(request_data["type"], request_data["stock_id"], request_data["user_id"])
        return transaction, 201
    # if request body is not correct, return status code 400
    return Response(status=400)
