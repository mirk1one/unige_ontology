import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-c", "--code", help = "Sigla del dipartimento", required = True)

argument = parser.parse_args()
dipartimento = argument.code

print(f"\nData la sigla del dipartimento {dipartimento}, restituisce tutte le persone che ricoprono dei ruoli inerenti\n")

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?dipartimento ?nome_dipartimento ?responsabilita ?persona ?nome_persona
WHERE
{
  ?dipartimento rdf:type ug:Department .
  ?dipartimento sc:branchCode ?sigla .
  ?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?nome_dipartimento) .
  ?dipartimento sc:employee ?persona .
  ?persona sc:givenName ?nome .
  ?persona sc:familyName ?cognome .
  BIND(CONCAT(?nome, " ", ?cognome) AS ?nome_persona) .
  ?persona ug:assignment ?ruolo .
  ?ruolo sc:roleName ?responsabilita .
	FILTER (?sigla = \"""" + dipartimento + """\")
}"""
    
call_local_sparql(query, "query_6_departments_occupations")