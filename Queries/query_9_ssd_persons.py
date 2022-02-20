import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-c", "--code", help = "Sigla del ssd", required = True)

argument = parser.parse_args()
codice = argument.code

print(f"Data la sigla del ssd {codice}, restituisce tutte le persone affiliate\n")

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?ssd ?nome ?afferenza ?ssd_nome ?email ?telefono
WHERE
{
  ?ssd rdf:type ug:Ssd .
  ?ssd sc:branchCode ?codice_ssd .
  ?ssd sc:legalName ?nome_ssd .
  BIND(CONCAT(?codice_ssd, " - ", ?nome_ssd) AS ?ssd_nome) .
  ?ssd sc:member ?persona .
  ?persona sc:givenName ?nome_persona .
  ?persona sc:familyName ?cognome_persona .
  BIND(CONCAT(?nome_persona, " ", ?cognome_persona) AS ?nome) .
  OPTIONAL
  {
    ?persona sc:worksFor ?dipartimento .
    ?dipartimento sc:branchCode ?sigla_dipartimento .
    ?dipartimento sc:legalName ?nome_dipartimento .
    BIND(CONCAT(?nome_dipartimento, " - ", ?sigla_dipartimento) AS ?afferenza) .
  }
  ?persona sc:contactPoint ?contatto .
  OPTIONAL {?contatto sc:email ?email} .
  OPTIONAL {?contatto sc:telephone ?telefono} .
  FILTER (?codice_ssd = \"""" + codice + """\")
}"""
    
call_local_sparql(query, "query_9_ssd_persons")