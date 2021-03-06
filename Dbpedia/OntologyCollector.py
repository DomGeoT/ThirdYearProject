from SPARQLWrapper import SPARQLWrapper, JSON
import json
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
    ?owner dbp:owner ?comp1 .
    ?owner dbp:owner ?comp2 .
    ?comp1 dbpedia2:symbol ?comp1Symbol .
    ?comp2 dbpedia2:symbol ?comp2Symbol .

   FILTER (?comp1 != ?comp2) .
}

'''

def runQuery():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)  # the previous query as a literal string

    with open("results.json", "w+") as f:
        json.dump(sparql.query().convert(), f)




print(runQuery())