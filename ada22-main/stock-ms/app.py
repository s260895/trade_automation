from flask import Flask, request, jsonify
from database import db
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)


@app.route("/stocks", methods=["POST"])
def create_stock():
    '''
    Endpoint to create stock
    '''
    body_data = request.get_json()
    # return status 400 if request contains no body
    if not body_data:
        return "No body", 400
    # define the necessary data
    required_data_list = ["stock_id", "name", "price", "ticker"]
    # check for necessary data, return status 400 is data is not available
    for required_data in required_data_list:
        if required_data not in body_data.keys():
            return "No {} in body".format(required_data), 400
    # create object
    data_object = {data_name:body_data[data_name] for data_name in required_data_list}
    db.stocks.insert_one(data_object)
    data_object["_id"] = str(data_object["_id"])
    return data_object, 201


@app.route("/stocks", methods=["GET"])
def get_stocks():
    '''
    Endpoint to retrieve all stocks
    '''
    # get all stocks
    objects = db.stocks.find()
    # return dict with all stocks
    return_list = []
    # convert the ObjectId and append to return_list
    for object in objects:
        object["_id"] = str(object["_id"])
        return_list.append(object)
    return jsonify(return_list), 200



@app.route("/stocks/<stock_id>", methods=["PUT"])
def update_stock(stock_id):
    request_data = request.get_json()
    # return status 400 is necessary data is not available
    if "price" not in request_data:
        return "No price", 400
    # try to find the object, return status 400 is object_id is not correct
    try:
        object = db.stocks.find_one({"_id": ObjectId(stock_id)})
    except:
        return "Incorrect stock_id", 400

    # update object
    db.stocks.update_one({"_id": ObjectId(stock_id)}, {
        "$set": {
            "price": request_data["price"]
        }
    })
    return "Stock updated!", 202
