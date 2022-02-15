import argparse
from virtuoso_call_sparql import call_local_sparql

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-n", "--name", help = "Nome della persona", required = True, nargs='+')

argument = parser.parse_args()
persona = argument.name
nome = persona[0]
cognome = persona[1]

print(f"\nData la persona {nome} {cognome}, restituisce tutti i suoi dati\n")

select = ["persona", "nome", "cognome", "link_immagine", "telefono", "email", "ruolo", "nome_ssd" "nome_dipartimento", "link_cv"]

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ug: <http://www.unige.it/2022/01/>
PREFIX sc: <http://www.schema.org/>

SELECT DISTINCT ?persona ?nome ?cognome ?link_immagine ?telefono ?email ?ruolo ?nome_ssd ?nome_dipartimento ?link_cv
WHERE
{
	?persona rdf:type sc:Person .
    ?persona sc:givenName ?nome .
    ?persona sc:familyName ?cognome .
	?persona sc:image ?immagine .
	?immagine sc:url ?url_immagine .
	?url_immagine ug:link ?link_immagine .
	?persona sc:contactPoint ?contatto .
	?contatto sc:telephone ?telefono .
	?contatto sc:email ?email .
	?persona sc:hasOccupation ?occupazione .
	?occupazione sc:qualifications ?ruolo .
    ?persona sc:member ?ssd .
    ?ssd sc:legalName ?ssd_nome_legale .
    ?ssd sc:branchCode ?ssd_sigla .
    BIND(CONCAT(?ssd_sigla, " - ", ?ssd_nome_legale) AS ?nome_ssd) .
	?persona sc:worksFor ?dipartimento .
	?dipartimento sc:name ?sigla_dipartimento .
	?dipartimento sc:legalName ?nome_legale_dipartimento .
    BIND(CONCAT(?nome_legale_dipartimento, " - ", ?sigla_dipartimento) AS ?nome_dipartimento) .
    ?persona sc:url ?url .
    ?url ug:link ?link_cv .
	FILTER (?nome = \"""" + nome + """\" && ?cognome = \"""" + cognome + """\")
}"""
    
call_local_sparql(query, select, "query_3_person_detail")