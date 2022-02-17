from virtuoso_call_sparql import call_local_sparql

print("Restituisce tutti gli edifici con indirizzo e coordinate geo")

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT DISTINCT ?edificio ?nome ?indirizzo
WHERE
{
  ?edificio rdf:type ug:CollegeOrUniversityBuilding .
  ?edificio sc:name ?nome .
  OPTIONAL
  {
    ?edificio sc:address ?luogo .
	  ?luogo sc:streetAddress ?via .
	  ?luogo sc:postalCode ?cap .
	  BIND(CONCAT(?via, ", ", ?cap) AS ?indirizzo) .
  }
}"""
    
call_local_sparql(query, "query_1_buildings")