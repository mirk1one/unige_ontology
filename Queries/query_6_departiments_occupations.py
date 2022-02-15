import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-c", "--code", help = "Sigla del dipartimento", required = True)

argument = parser.parse_args()
dipartimento = argument.code

print(f"\nData la sigla del dipartimento {dipartimento}, restituisce tutte le persone che ricoprono dei ruoli inerenti\n")

select = ["dipartimento", "nome_dipartimento", "responsabilita", "persona", "nome_persona"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?dipartimento ?nome_dipartimento ?responsabilita ?persona ?nome_persona
WHERE
{
	?dipartimento rdf:type ug:Department .
	?dipartimento sc:name ?sigla .
	?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?nome_dipartimento) .
  ?dipartimento ug:occupationDepartment ?occupazione .
  ?occupazione sc:responsabilities ?responsabilita .
  ?occupazione sc:hasOccupation ?persona .
  ?persona sc:givenName ?nome .
  ?persona sc:familyName ?cognome .
  BIND(CONCAT(?nome, " ", ?cognome) AS ?nome_persona) .
	FILTER (?sigla = \"""" + dipartimento + """\")
}"""
    
call_local_sparql(query, select, "query_6_departments_occupations")