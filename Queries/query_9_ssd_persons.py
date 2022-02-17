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

SELECT DISTINCT ?ssd ?nome ?afferenza (group_concat(DISTINCT ?dato_contatto, "; ") as ?contatti)
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
  {
    SELECT ?dato_contatto
    WHERE
    {
      ?p sc:givenName ?nome_persona .
      ?p sc:familyName ?cognome_persona .
      ?p sc:contactPoint ?c .
      ?c sc:telephone ?v .
      ?c sc:contactType ?t .
      BIND(CONCAT(?v, " ", ?t) AS ?dato_contatto) .
    }
  } UNION
  {
    SELECT ?dato_contatto
    WHERE
    {
      ?p sc:givenName ?nome_persona .
      ?p sc:familyName ?cognome_persona .
      ?p sc:contactPoint ?c .
      ?c sc:email ?v .
      ?c sc:contactType ?t .
      BIND(CONCAT(?v, " ", ?t) AS ?dato_contatto) .
    }
  }
  FILTER (?codice_ssd = \"""" + codice + """\")
}
GROUP BY ?ssd ?nome ?afferenza"""
    
call_local_sparql(query, "query_9_ssd_persons")