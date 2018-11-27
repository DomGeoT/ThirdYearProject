import urllib.request
import json
import datetime
import time

class Stock:
    def __init__(self, date, symbol, time, open, high, low, close, volume):
        self.date = date
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __str__(self):
        return str("SYMBOL: " + str(self.symbol) + "\n" + "DATE: " + str(self.date) + "\n" + "TIME: " + str(self.time) + "\n" + "OPEN: " + str(self.open) + "\n" + "HIGH: " + str(self.high) + "\n" + "LOW: " + str(self.low) + "\n" + "CLOSE: : " + str(self.close) + "\n" + "VOLUME: " + str(self.volume) + "\n")



def loadSymbols():
    symbols = open("symbols.txt", "r")

    text = symbols.read()
    return text.split("\n")

def requestStockData(symbol):
    print("Fetching data for", symbol)
    urllib.request.urlretrieve("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol + "&interval=1min&outputsize=full&apikey=QT9W4J81W90I0XQE", "query.json")
    time.sleep(25)
    print("FETCHED")

def jsonToStocks(symbol):
    stockData = json.load(open("query.json", "r"))["Time Series (1min)"]
    stocks = []

    for key in stockData.keys():
        dateTime = key.split(" ")
        if (dateTime[0] == str(datetime.datetime.now().date())):
            stock = Stock(dateTime[0], symbol, dateTime[1], stockData[key]['1. open'], stockData[key]['2. high'], stockData[key]['3. low'], stockData[key]['4. close'], stockData[key]['5. volume'])
            stocks.append(stock)
    return stocks

def stocksToDict(stocks):
    data = {}
    for stock in stocks:
        if not stock.date in data:
            data.update({stock.date : {}})

        if not stock.symbol in data[stock.date]:
            data[stock.date].update({stock.symbol : {}})

        stockData = {
            "open": stock.open,
            "high": stock.high,
            "low": stock.low,
            "close": stock.close,
            "volume": stock.volume
        }
        data[stock.date][stock.symbol].update({stock.time : stockData})

    return data

def processSymbols(symbols):
    stocks = []
    for symbol in symbols:
        requestStockData(symbol)
        stocks.extend(jsonToStocks(symbol))

    return stocksToDict(stocks)


def writeStockDictToFile(stocksDictionary):
    with open("data.json", 'ab+') as f:
        f.seek(0,2)                                #Go to the end of file
        if f.tell() == 0 :                         #Check if file is empty
            f.write(json.dumps(stocksDictionary).encode())  #If empty, write an array
        else :
            f.seek(-1,2)
            f.truncate()                           #Remove the last character, open the array
            f.write(' , '.encode())                #Write the separator
            f.write(json.dumps(stocksDictionary).encode())    #Dump the dictionary
            f.write('}'.encode())


writeStockDictToFile(processSymbols(loadSymbols()))