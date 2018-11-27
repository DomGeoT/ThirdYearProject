import urllib.request
import sys
import json
from collections import defaultdict

# collects data from NASDAQ market
# opens   0930 Eastern -> 1430 GMT
# closes  1600 Eastern -> 2130 GMT

# data collection occurs at approximately 2200 GMT

# Parse sys.argv, where stocks are passed

companies = ['MSFT', 'AAPL']

#returns json
def requestStockData(stock):
    with urllib.request.urlopen("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stock+"&interval=1min&outputsize=full&apikey=QT9W4J81W90I0XQE") as url:
        return json.loads(url.read().decode())


# create our output dictionary
jsonOut = defaultdict()

for company in companies:
    # Grab that JSON
    data= requestStockData(str(company))
    #initialise the structure if it doesnt exist
    for key in data["Time Series (1min)"]:
        if key not in jsonOut:
            jsonOut[key] = defaultdict()
    #Flatten the structure
    for key in data["Time Series (1min)"]:
        jsonOut[key][str(company)] = data["Time Series (1min)"][key]

#Output to stdout
print(json.dumps(jsonOut))