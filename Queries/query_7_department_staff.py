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

SELECT DISTINCT ?dipartimento ?nome ?qualifica ?afferenza (group_concat(DISTINCT ?dato_contatto, "; ") as ?contatti)
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
	FILTER (?sigla = \"""" + dipartimento + """\")
}
GROUP BY ?dipartimento ?nome ?qualifica ?afferenza"""
    
call_local_sparql(query, "query_7_department_staff")