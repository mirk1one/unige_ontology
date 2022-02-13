from virtuoso_call_sparql import call_local_sparql

print("Dato un edificio, restituisce tutte le persone che ci lavorano\n")
edificio = input("Inserire il nome dell'edificio: ")

select = ["edificio", "nome_persona", "cognome_persona", "ssd", "nome_edificio", "url_planimetria", "stanza", "telefono", "email"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?edificio ?nome_persona ?cognome_persona ?ssd ?nome_edificio ?url_planimetria ?stanza ?telefono ?email
WHERE
{
	?edificio rdf:type ug:CollegeOrUniversityBuilding .
	?edificio sc:name ?nome_edificio .
	?edificio sc:employee ?persona .
	?persona sc:givenName ?nome_persona .
	?persona sc:familyName ?cognome_persona .
  OPTIONAL
  {
    ?persona sc:member ?settore .
    ?settore sc:legalName ?ssd_nome .
    ?settore sc:branchCode ?ssd_codice .
    BIND(CONCAT(?ssd_nome, " - ", ?ssd_codice) AS ?ssd) .
  }
	?persona sc:contactPoint ?contatto .
	?contatto sc:telephone ?telefono .
	OPTIONAL { ?contatto sc:email ?email } .
	OPTIONAL { ?contatto ug:roomCode ?stanza } .
	?contatto sc:areaServed ?area .
	?contatto sc:url ?url_planimetria .
	?url_planimetria ug:link ?planimetria .
	FILTER (?nome_edificio = \"""" + edificio + """\" && ?area = \"""" + edificio + """\")
}
ORDER BY ?cognome_persona"""
    
call_local_sparql(query, select, "query_2_person_building_2")