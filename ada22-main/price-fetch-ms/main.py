from datetime import datetime
import pandas
import ccxt

def price_fetcher(event,context):
    '''
        Stateless Function to fetch latest price data of all stocks
        Event/Trigger: Cloud Scheduler

    '''


    '''
        Stock List to be fetched from GET /stocks
    '''
    stock_list= ['BTCUSDT','ETHUSDT','BNBUSDT']


    '''Hard Coded Parameters: 
            Number of Candles, 
            Interval, 
            User ID/Pwd, 
            Whether to Fetch the Last Price 
    '''
    candles = 50
    interval = '1h'
    exchange= ccxt.binance({
                        'apiKey': 'INH9JYsd4Cu3kMPoONiCVHP3KlACsg3F4ehDN1cburoKohsARMpZGcq4PnQoqzyF',
                        'secret': 'FSVMXANswsGOj3B4Oi4NSDOlX5fsvWOJ3s56DQsWvJTjLhSuPyq1aFLbFEWoOrMt',
                        'enableRateLimit': True, 
                        'options': {'defaultType': 'future'},
                        'hedgeMode':True
                        })
    last_incomplete_candle = False


    '''
        For Each Stock: Store the fetched Price Values and Datetimes as a Pandas Dataframe 
    '''
    df_dict = dict()
    for symbol in stock_list:    
        if last_incomplete_candle == False:
            closes = [[datetime.datetime.utcfromtimestamp(float(elem[0]) / 1000.),elem[4]] 
            for elem in exchange.fapiPublic_get_klines({'symbol':symbol,'interval':interval})][-candles:-1]
        if last_incomplete_candle == True:
            closes = [[datetime.datetime.utcfromtimestamp(float(elem[0]) / 1000.),elem[4]] 
            for elem in exchange.fapiPublic_get_klines({'symbol':symbol,'interval':interval})][-(candles-1):]
        dates = [elem[0] for elem in closes]
        values = [float(elem[1]) for elem in closes]
        df = pandas.DataFrame([(elem[0],elem[1]) for elem in zip(dates,values)],columns=['datetime','closes'])
        df_dict[symbol]=df
    

    '''
    update through PUT /stocks/<stock_id>
    '''
    return df_dict
    