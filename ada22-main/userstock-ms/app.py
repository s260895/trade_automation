from flask import Flask, request, jsonify
from database import db
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)


@app.route("/user_stock", methods=["POST"])
def create_user_stock():
    '''
    Endpoint to create user_stock
    '''
    body_data = request.get_json()
    # return status 400 if request contains no body
    if not body_data:
        return "No body", 400
    # define the necessary data
    required_data_list = ["stock_id", "user_id", "date_opened", "date_closed", "open_price", "close_price"]
    # check for necessary data, return status 400 is data is not available
    for required_data in required_data_list:
        if required_data not in body_data.keys():
            return "No {} in body".format(required_data), 400
    # create object
    data_object = {data_name:body_data[data_name] for data_name in required_data_list}
    db.userstocks.insert_one(data_object)
    data_object["_id"] = str(data_object["_id"])
    return data_object, 201


@app.route("/user_stocks/<user_id>", methods=["GET"])
def get_user_stocks(user_id):
    '''
    Endpoint to retrieve user_stocks for a certain user
    '''
    # get all user_stocks
    objects = db.userstocks.find({"user_id": int(user_id)})
    # return dict with all userstocks in a strange way
    return_list = []
    # convert the ObjectId and append to return_list
    for object in objects:
        object["_id"] = str(object["_id"])
        return_list.append(object)
    return jsonify(return_list), 200



@app.route("/sell", methods=["PUT"])
def update_user_stock():
    request_data = request.get_json()
    # return status 400 is necessary data is not available
    if "stock_id" not in request_data:
        return "No stock_id", 400
    if "close_price" not in request_data:
        return "No close_price", 400
    # try to find the object, return status 400 is object_id is not correct
    try:
        object = db.userstocks.find_one({"_id": ObjectId(request_data["stock_id"])})
    except:
        return "Not correct user_stock_id", 400
    # return status 400 is object is already sold
    if object["date_closed"] != None:
        return "UserStock already sold", 400
    # update object
    db.userstocks.update_one({"_id": ObjectId(request_data["stock_id"])}, {
        "$set": {
            "date_closed": datetime.now(),
            "close_price": request_data["close_price"]
        }
    })
    return "UserStock Sold!", 202
