from asyncio.windows_events import NULL
from datetime import datetime
import pandas
import ccxt
from pyti.exponential_moving_average import exponential_moving_average
import pickle
import time
from datetime import datetime


def rule_evaluator(event,context):
    '''
        Stateless Function to Evaluate Trading Logic on the latest price data
        Event/Trigger: Cloud Scheduler

    '''

    '''
        Stock List and Corresponding Prices to be fetched from GET /stocks
    '''
    # stock_list=['BTCUSDT','ETHUSDT','BNBUSDT']
    
    # with open('sample_output.pkl', 'rb') as f:
    #     stock_prices = pickle.load(f)


    stocks_db = [{
        "id": 1,
        "name": "Bitcoin",
        "ticker": "BTCUSDT",
        "prices": [1,10,100,10]
        },
        {
        "id": 2,
        "name": "Ethereum",
        "ticker": "ETHUSDT",
        "prices": [1000,100,10,1]
        },
        {
        "id": 3,
        "name": "Binance",
        "ticker": "BNBUSDT",
        "prices": [1,10,1,10]
        }
    ]

    user_stocks_db = [
        {
            "id": 1,
            "stock_id": 1,
            "user_id": 1,
            "date_opened": 1648058100,
            "date_closed": 1648058104,
            "open_price": "1526.32",
            "close_price": "1621.25"
        },
        {
            "id": 2,
            "stock_id": 1,
            "user_id": 1,
            "date_opened": 1648058102,
            "date_closed": None,
            "open_price": "1500.32",
            "close_price": None
        },
        {
            "id": 3,
            "stock_id": 1,
            "user_id": 1,
            "date_opened": 1648058104,
            "date_closed": None,
            "open_price": "1200",
            "close_price": None
        }
    ]

    '''Hard Coded Parameters: 
            Number of Candles, 
            Interval, 
            User ID/Pwd, 
            Whether to Fetch the Last Price 
            Strategy Name/Description
            Technical Indicators Used
    '''

    strategy_params = {
        'strat_name':'ema_cross_over_under',
        'technical_indicators': {'fast_ema':2,'slow_ema':3}
    }

    prices_per_stock = 4

    '''
        for each stock
    '''
    for stock_db in stocks_db:

        if len(list(stock_db['prices'])) != prices_per_stock:
            return "INPUT STOCK HAS TOO FEW PRICES"

        closes = [float(price) for price in stock_db['prices']]

        '''Calculate "Aggregate" Indicator from all Technical Indicators'''
        indicator = pandas.DataFrame(exponential_moving_average(closes,strategy_params['technical_indicators']['fast_ema'])
                                - exponential_moving_average(closes,strategy_params['technical_indicators']['slow_ema']),
                                columns=['ema_diff'])
        '''Reduce Length of All Columns'''
        # closes = closes[(prices_per_stock+1):]
        # indicator = indicator[(prices_per_stock+1):]
        '''Compute Signal Column (permissible values 1,-1,0)'''
        signal = [1 if  float(closes[index])>float(closes[index-1])
                    else -1 if float(closes[index])<float(closes[index-1])
                    else 0
                    for index in range(len(closes))]

        # [0] + [1 if float(indicator.loc[index]) > 0 and float(indicator.loc[index-1]) < 0
        #                 else -1 if float(indicator.loc[index]) < 0 and float(indicator.loc[index-1]) > 0  
        #                 else 0 for index in indicator.index[1:]]

        # print(signal)
        print(stock_db['ticker'])
        '''
            if signal not 0, fetch all users 
            GET /user_stocks (argument: stock id)
        '''
        if signal[-1] != 0:
            '''
                If Non Zero Signal
                Make Transaction with 
                POST /transactions (args: user_id, stock_id)
            '''

            if signal[-1] == 1:
                user_ids = set([user_stock_db['user_id'] for user_stock_db in user_stocks_db if user_stock_db['stock_id'] == stock_db['id']])
                for user_id in user_ids:
                    # 1. BUY transaction to be forwarded to the transaction-ms
                    new_transaction = {
                        "symbol": stock_db['ticker'],
                        "type": "MARKET",
                        "side": "BUY",
                        "positionSide": "BOTH",
                        "quantity": 1.0,
                        "user_id": user_id
                    }
                    # POST /transactions, body = new_transaction

                    # 2. Create a new UserStock in userstock-ms
                    new_user_stock = {
                        "stock_id": 1,
                        "user_id": user_id,
                        "date_opened": datetime.now(),
                        "date_closed": None,
                        "open_price": stock_db['prices'],
                        "close_price": None
                    }

                    user_stocks_db.append(new_user_stock)
                    # POST /user_stocks, body = new_user_stock

            if signal[-1] == -1:
                
                selected_user_stocks = [user_stock_db for user_stock_db in user_stocks_db if (user_stock_db['stock_id'] == stock_db['id']) and (user_stock_db['date_closed'] == None)]
                user_ids = [selected_user_stock['user_id'] for selected_user_stock in selected_user_stocks]
                
                
                # print(user_stocks_db)
                # print(user_ids)
                for user_id in user_ids:
                    # print(user_stocks_db)
                    print("123")
                    # 1. SELL transaction to be forwarded to the transaction-ms
                    new_transaction = {
                        "symbol": stock_db['ticker'],
                        "type": "MARKET",
                        "side": "SELL",
                        "positionSide": "BOTH",
                        "quantity": 1.0,
                        "user_id": user_id
                    }
                    # POST /transactions, body = new_transaction

                    # 2. Close an UserStock in userstock-ms
                    selected_user_stock = [selected_user_stock for selected_user_stock in selected_user_stocks if selected_user_stock['user_id'] == user_id][0]
                    print(selected_user_stock)
                    # print(selected_)
                    selected_index = user_stocks_db.index(selected_user_stock)
                    
                    selected_user_stock['date_closed'] = datetime.now()
                    selected_user_stock['close_price'] = stock_db['prices'][-1]



                    user_stocks_db[selected_index] = selected_user_stock

                    print(user_stocks_db)


                    # new_user_stock = {
                    #     "stock_id": 1,
                    #     "user_id": user_id,
                    #     "date_opened": datetime.now(),
                    #     "date_closed": None,
                    #     "open_price": stock_db['price'],
                    #     "close_price": stock_db['price']
                    # }

    return user_stocks_db