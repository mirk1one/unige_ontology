import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-c", "--code", help = "Sigla del dipartimento", required = True)

argument = parser.parse_args()
dipartimento = argument.code

print(f"\nData la sigla del dipartimento {dipartimento}, restituisce tutti i suoi contatti\n")

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT DISTINCT ?dipartimento ?nome ?tipo_contatto ?dettaglio_contatto ?altro_dato
WHERE
{
  ?dipartimento rdf:type ug:Department .
  ?dipartimento sc:branchCode ?sigla .
  ?dipartimento sc:legalName ?nome_legale .
  BIND(CONCAT(?nome_legale, " - ", ?sigla) AS ?nome) .
  {
    ?dipartimento sc:address ?luogo .
    BIND("Indirizzo" AS ?tipo_contatto) .
    ?luogo sc:streetAddress ?via .
    ?luogo sc:postalCode ?cap .
    ?luogo sc:addressLocality ?citta .
    BIND(CONCAT(?via, ", ", ?cap, ", ", ?citta) AS ?dettaglio_contatto) .
    ?dipartimento ug:geo ?coordinate .
    ?coordinate geo:lat ?lat .
    ?coordinate geo:long ?long .
    BIND(CONCAT("https://google.com/maps?q=", STR(?lat), ",", STR(?long)) AS ?altro_dato) .
  } UNION
  {
    ?dipartimento sc:contactPoint ?contatto .
    ?contatto sc:contactType ?tipo_contatto .
    ?contatto sc:telephone ?dettaglio_contatto .
    BIND("" AS ?altro_dato) .
  } UNION
  {
    ?dipartimento sc:contactPoint ?contatto .
    ?contatto sc:contactType ?tipo_contatto .
    ?contatto sc:fax ?dettaglio_contatto .
    BIND("" AS ?altro_dato) .
  } UNION
  {
    ?dipartimento sc:contactPoint ?contatto .
    ?contatto sc:contactType ?tipo_contatto .
    ?contatto sc:email ?dettaglio_contatto .
    BIND("" AS ?altro_dato) .
  } UNION
  {
    ?dipartimento sc:contactPoint ?contatto .
    ?contatto sc:contactType ?tipo_contatto .
    ?contatto sc:telephone ?dettaglio_contatto .
    BIND("" AS ?altro_dato) .
  } UNION
  {
    ?dipartimento sc:url ?contatto .
    ?contatto sc:description ?tipo_contatto .
    ?contatto ug:link ?dettaglio_contatto .
    BIND("" AS ?altro_dato) .
  }
	FILTER (?sigla = \"""" + dipartimento + """\")
}"""
    
call_local_sparql(query, "query_5_department_contacts")