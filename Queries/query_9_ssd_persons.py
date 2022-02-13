from virtuoso_call_sparql import call_local_sparql

print("Data la sigla di un ssd, restituisce tutte le persone affiliate\n")
codice = input("Inserire la del ssd: ")

select = ["ssd", "nome", "afferenza", "telefono", "email"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?ssd ?nome ?afferenza ?telefono ?email
WHERE
{
	?ssd rdf:type ug:Ssd .
  ?ssd sc:branchCode ?codice_ssd .
	?ssd sc:member ?persona .
	?persona sc:givenName ?nome_persona .
	?persona sc:familyName ?cognome_persona .
  BIND(CONCAT(?nome_persona, " ", ?cognome_persona) AS ?nome) .
	?persona sc:worksFor ?dipartimento .
  ?dipartimento sc:name ?sigla_dipartimento .
	?dipartimento sc:legalName ?nome_dipartimento .
  BIND(CONCAT(?nome_dipartimento, " - ", ?sigla_dipartimento) AS ?afferenza) .
	?persona sc:contactPoint ?contatto .
	OPTIONAL { ?contatto sc:telephone ?telefono } .
	OPTIONAL { ?contatto sc:email ?email } .
	FILTER (?codice_ssd = \"""" + codice + """\")
}
ORDER BY ?cognome_persona"""
    
call_local_sparql(query, select, "query_9_ssd_persons")