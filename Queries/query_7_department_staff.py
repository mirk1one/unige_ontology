import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-c", "--code", help = "Sigla del dipartimento", required = True)

argument = parser.parse_args()
dipartimento = argument.code

print(f"\nDato il dipartimento {dipartimento}, restituisce tutto il personale del dipartimento e i loro dati\n")

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?dipartimento ?nome ?qualifica ?afferenza ?email ?telefono
WHERE
{
  ?dipartimento rdf:type ug:Department .
  ?dipartimento sc:branchCode ?sigla .
  ?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?afferenza) .
  ?dipartimento sc:employee ?persona .
  ?persona sc:givenName ?nome_persona .
  ?persona sc:familyName ?cognome_persona .
  BIND(CONCAT(?nome_persona, " ", ?cognome_persona) AS ?nome) .
  ?persona sc:hasOccupation ?occupazione .
  ?occupazione sc:qualifications ?qualifica .
  ?persona sc:contactPoint ?contatto .
  OPTIONAL {?contatto sc:email ?email} .
  OPTIONAL {?contatto sc:telephone ?telefono} .
	FILTER (?sigla = \"""" + dipartimento + """\")
}"""
    
call_local_sparql(query, "query_7_department_staff")