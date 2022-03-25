from daos.stock_dao import StockDAO
from db import Session, engine, Base

# os.environ['DB_URL'] = 'sqlite:///delivery.db'
# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

stock_1 = StockDAO(1, "TestName", "100", "TestTickers")

session.add(stock_1)

# 10 - commit and close session
session.commit()
session.close()