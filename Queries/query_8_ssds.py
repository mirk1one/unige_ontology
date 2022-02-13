from virtuoso_call_sparql import call_local_sparql

print("Restituisce tutti i settori scientifici disciplinari con nome e sigla\n")

select = ["ssd", "sigla", "nome"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?ssd ?sigla ?nome
WHERE
{
	?ssd rdf:type ug:Ssd .
	?ssd sc:branchCode ?sigla .
	?ssd sc:legalName ?nome .
}"""
    
call_local_sparql(query, select, "query_8_ssds")