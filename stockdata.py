import json
### googlefinance -> yahoo_fin.stock_info
from googlefinance import getQuotes
from yahoo_fin import stock_info as si
import requests
from time import sleep

class Main():
    def __init__(self, db="stocks", stocks_file="stocks.json"):
        self.stocks=None
        self.db=db
        self.load_stocks(stocks_file)
    
    def write_to_db(self, measurement, tags, values):
        tag_string=["".join(["{}={}".format(k,v) for k,v in t.iteritems()]) for t in tags]
        data_string="".join(["{},{} value={}".format(measurement, tag_string[i], values[i]) for i in range(len(values))])
        requests.post("http://localhost:8086/write?db={}".format(self.db), data_string)
    
    def get_stock_prices(self, stocks):
        quotes_json=getQuotes(stocks)
        quotes={q["StockSymbol"]:q["LastTradePrice"] for q in quotes_json}
        return quotes

    def load_stocks(self, stocks_file):
        with open(stocks_file) as f:
            data=json.load(f)
            self.stocks=data['stocks']

    def run(self, interval=10):
        while 1:
            try:
                sleep(interval)
                stock_prices=self.get_stock_prices(self.stocks)
                self.write_to_db("stock_value", [{"symbol":k} for k in stock_prices.keys()], stock_prices.values())
            except KeyboardInterrupt:
                quit()
            except:
                pass

if __name__=="__main__":
    m=Main()
    m.run()
