from virtuoso_call_sparql import call_local_sparql

print("Restituisce tutti i dipartimenti con il numero di personale afferente alla struttura")

select = ["dipartimento", "nome", "numero_afferenti"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?dipartimento ?nome (count(distinct ?persona) as ?numero_afferenti)
WHERE
{
	?dipartimento rdf:type ug:Department .
	?dipartimento sc:name ?sigla .
	?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?nome) .
	?dipartimento sc:employee ?persona .
}
GROUP BY ?dipartimento ?nome"""
    
call_local_sparql(query, select, "query_4_departments")