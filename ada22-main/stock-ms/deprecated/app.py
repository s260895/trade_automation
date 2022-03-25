from flask import Flask, request

from stocks.deprecated.db import Base, engine
from resources.stock import Stock

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/stocks', methods=['POST'])
def create_stock():
    req_data = request.get_json()
    return Stock.create(req_data)


@app.route('/stocks', methods=['GET'])
def get_stocks():
    return Stock.get()


@app.route('/deliveries/<stock_id>', methods=['PUT'])
def update_stock(stock_id):
    stock_id = request.args.get('stock_id')
    name = request.args.get('name')
    price = request.args.get('price')
    ticker = request.args.get('ticker')
    return Stock.update(stock_id, name, price, ticker)
