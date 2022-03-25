from datetime import datetime
from flask import Flask, json, jsonify, Response
from daos.stock_dao import StockDAO
from stocks.deprecated.db import Session


class Stock:
  
    @staticmethod
    def create(body):
        session = Session()
        stock = StockDAO(body['name'], body['price'], body['ticker'])
        session.add(stock)
        session.commit()
        session.refresh(stock)
        session.close()
        return jsonify({'message': f'stock with id {stock.stock_id} created'}), 200

    @staticmethod
    def get():
        session = Session()
        stock = session.query(StockDAO).all()
        if stock:
           session.close()
           return json.dumps(stock), 200
           
        else:
            session.close() 
            return jsonify({'message': f'Database not found'}), 404
      
    @staticmethod
    def update(stock_id, name, price, ticker):
        session = Session()
        stock = session.query(StockDAO).filter(StockDAO.stock_id == stock_id).first()
        if stock:
            stock.name = name
            stock.price = price
            stock.ticker = ticker
            session.close()
            return jsonify({'message:': f'Stock at id {stock_id} updated'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no stock with id {stock_id}'}), 404