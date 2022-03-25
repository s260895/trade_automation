from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from stocks.deprecated.db import Base


class StockDAO(Base):
    __tablename__ = 'stock'
    stock_id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String)
    price = Column(String)
    ticker = Column(String)

    def __init__(self, name, price, ticker):
        self.name = name
        self.price = price
        self.ticker = ticker