import urllib
import time

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import pandas

def retry(delay, attempts):
    def wrapper(function):
        def wrapped(*args, **kwargs):
            for i in range(attempts):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    print(str(e))
                    print("failure after attempt", attempts, "- retrying in...", delay)
                    time.sleep(delay)
        return wrapped
    return wrapper


def loadQuery(queryName):
    with open(queryName, "r") as f:
        return f.read()


@retry(60, 10)
def runQuery(query):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    return sparql.query()


def writeResultsToFile(results, resultsFileName):
    with open("results.json", "w+") as f:
        json.dump(results, f)


def loadCompanyData():
    companyData = pandas.read_csv("companylist.csv", sep=',',header=0)
    companyData = companyData.loc[:, ["Symbol","Name"]]

    return companyData

def buildQuery(companySymbol, companyName):
    query = '''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    
    PREFIX d: <http://dbpedia.org/ontology/>
    
    SELECT *
    WHERE {     
        ?comp <http://dbpedia.org/property/symbol> \"''' + companySymbol + '''\"^^rdf:langString .
    }
    
    '''
    return query


def storeResults(resultFileName, results):
    with open(resultFileName, "w+") as f:
        for result in results:
            f.write(str(result) + "\n")


def findCompanies():
    companySymbols = loadCompanyData()
    results = []

    for count, data in companySymbols.iterrows():
        query = buildQuery(data['Symbol'], data['Name'].split(",")[0])
        result = runQuery(query).convert()

        if len(result['results']['bindings']) > 0:
            for r in result['results']['bindings']:
                print(data['Symbol'], r)
                results.append(str(data['Symbol'] + "|" + str(r)))
        else:
            print(data['Symbol'], "no results")
    storeResults("uriSymbolPairs.csv", results)

findCompanies()