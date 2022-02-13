from virtuoso_call_sparql import call_local_sparql

print("Data la sigla di un dipartimento, restituisce tutto il personale del dipartimento e i loro dati\n")
dipartimento = input("Inserire la sigla del dipartimento: ")

select = ["dipartimento", "nome", "qualifica", "afferenza", "contatti"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?dipartimento ?nome ?qualifica ?afferenza (group_concat(?dato_contatto, '; ') as ?contatti)
WHERE
{
	?dipartimento rdf:type ug:Department .
	?dipartimento sc:name ?sigla .
	?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?afferenza) .
  ?dipartimento sc:employee ?persona .
  ?persona sc:givenName ?nome_persona .
  ?persona sc:familyName ?cognome_persona .
  BIND(CONCAT(?nome_persona, " ", ?cognome_persona) AS ?nome) .
  ?persona sc:hasOccupation ?occupazione .
  ?occupazione sc:qualifications ?qualifica .
  ?occupazione sc:hasOccupation ?persona .
  ?persona sc:contactPoint ?contatto .
  {
     ?contatto sc:telephone ?valore_contatto .
     ?contatto sc:contactType ?tipo_contatto .
     BIND(CONCAT(?valore_contatto, " ", ?tipo_contatto) AS ?dato_contatto) .
  } UNION
  {
     ?contatto sc:email ?valore_contatto .
     ?contatto sc:contactType ?tipo_contatto .
     BIND(CONCAT(?valore_contatto, " ", ?tipo_contatto) AS ?dato_contatto) .
  }
	FILTER (?sigla = \"""" + dipartimento + """\")
}
GROUP BY ?dipartimento ?nome ?qualifica ?afferenza"""
    
call_local_sparql(query, select, "query_7_department_staff")