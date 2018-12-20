import DataCollector
import datetime
import time

def loadSymbols():
    symbols = open("symbols.txt", "r")

    text = symbols.read()
    return text.split("\n")

storeName = str(datetime.datetime.now().date()) + ".ttl"
companies = loadSymbols()
lastAPICall = datetime.datetime.now()

for company in companies:
    while (datetime.datetime.now() - lastAPICall).seconds < 15:
        time.sleep(1)

    try:
        print("Collecting data for", company)
        lastAPICall = datetime.datetime.now()
        DataCollector.collectStockData(company, storeName)
    except:
        print("WARNING error caught when executing data collection for", company)
        log = open('log.txt', 'a+')
        log.write(str("WARNING error caught when executing data collection for" + str(company) + " on " + str(datetime.datetime.now()) + "\n"))
        log.close()