from virtuoso_call_sparql import call_local_sparql

print("Dato un edificio, restituisce tutte le persone che ci lavorano\n")
edificio = input("Inserire il nome dell'edificio: ")

select = ["edificio", "nome_persona", "cognome_persona", "qualifica", "nome_dipartimento", "nome_edificio", "indirizzo", "coordinate_maps"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT DISTINCT ?edificio ?nome_persona ?cognome_persona ?qualifica ?nome_dipartimento ?nome_edificio ?indirizzo ?coordinate_maps
WHERE
{
	?edificio rdf:type ug:CollegeOrUniversityBuilding .
	?edificio sc:name ?nome_edificio .
	?edificio sc:employee ?persona .
	?persona sc:givenName ?nome_persona .
	?persona sc:familyName ?cognome_persona .
	?persona sc:hasOccupation ?occupazione .
	?occupazione sc:qualifications ?qualifica .
	?persona sc:worksFor ?dipartimento .
  ?dipartimento sc:name ?sigla_dipartimento .
	?dipartimento sc:legalName ?nome_legale_dipartimento .
  BIND(CONCAT(?nome_legale_dipartimento, " - ", ?sigla_dipartimento) AS ?nome_dipartimento) .
	?edificio sc:address ?luogo .
	?luogo sc:streetAddress ?via .
	?luogo sc:postalCode ?cap .
	BIND(CONCAT(?via, ", ", ?cap) AS ?indirizzo) .
  ?edificio ug:geo ?coordinate .
	?coordinate geo:lat ?lat .
	?coordinate geo:long ?long .
	BIND(CONCAT("https://google.com/maps?q=", STR(?lat), ",", STR(?long)) AS ?coordinate_maps) .
	FILTER (?nome_edificio = \"""" + edificio + """\")
}
ORDER BY ?cognome_persona"""
    
call_local_sparql(query, select, "query_2_person_building")