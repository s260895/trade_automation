from daos.stock_dao import StockDAO
from db import Session

# 2 - extract a session
session = Session()

stocks = session.query(StockDAO).all()

# 4 - print deliveries' details
print('\n### All stocks:')
for stock in stocks:
    print(f'{stock.stock_id} with price {stock.price} and name {stock.name}')
print('')