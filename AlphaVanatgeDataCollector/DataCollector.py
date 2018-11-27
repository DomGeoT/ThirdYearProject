import urllib.request
import datetime
import shutil
import os

# collects data from NASDAQ market
# opens   0930 Eastern -> 1430 GMT
# closes  1600 Eastern -> 2100 GMT

# data collection occurs at approximately 2200 GMT

def move(src, dest):
    shutil.move(src, dest)

def requestStockData(symbol):
    urllib.request.urlretrieve("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + symbol + "&interval=1min&outputsize=full&apikey=QT9W4J81W90I0XQE", "query.json")

def storeStockData(symbol, now):
    if not os.path.isdir("data"):
        os.mkdir("data")

    # check to see if day already included


    collatedDataFile = open("data/" + symbol + ".csv", "a+")
    dailyDataFile = open("query.csv", "r")

    firstLine = True
    for line in dailyDataFile:
        if firstLine:
            firstLine = False
            continue

        collatedDataFile.write(line)


    collatedDataFile.close()
    dailyDataFile.close()

def loadSymbols():
    symbols = open("symbols.txt", "r")

    text = symbols.read()
    return text.split("\n")

companies = loadSymbols()

now = datetime.datetime.now()

for company in companies:
    requestStockData(company)
    storeStockData(company, now)
