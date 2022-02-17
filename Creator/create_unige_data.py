from os.path import exists


def create_ontology(name):
    f = open(name, "a+")
    f.write("# Prefissi usati nella ontologia\n")
    f.write("@prefix ug: <http://www.unige.it/2022/01/> .\n")
    f.write("@prefix sc: <http://www.schema.org/> .\n")
    f.write("@prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n")
    f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    f.write("@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n")
    f.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")
    f.write("# Definizione di edificio e di dipartimento\n")
    f.write("ug:CollegeOrUniversityBuilding rdfs:subClassOf sc:CollegeOrUniversity .\n")
    f.write("ug:Department rdfs:subClassOf sc:EducationOrganization .\n\n")
    f.write("# Definizione di occupazione nel dipartimento\n")
    f.write("ug:occupationDepartment rdf:type rdf:Property .\n")
    f.write("ug:occupationDepartment rdfs:label \"Il dipartimento in cui la persona occupa il ruolo\" .\n")
    f.write("ug:occupationDepartment rdfs:domain sc:Occupation .\n")
    f.write("ug:occupationDepartment rdfs:range ug:Department .\n\n")
    f.write("# Definizione di punto geolocalizzato\n")
    f.write("ug:geo rdf:type rdf:Property .\n")
    f.write("ug:geo rdfs:label \"Connette un punto geolocalizzato ad un posto\" .\n")
    f.write("ug:geo rdfs:domain sc:Place .\n")
    f.write("ug:geo rdfs:range geo:Point .\n\n")
    f.write("# Definizione del codice di una stanza\n")
    f.write("ug:roomCode rdf:type rdf:Property .\n")
    f.write("ug:roomCode rdfs:label \"Aggiunge il codice della stanza dove lavora\" .\n")
    f.write("ug:roomCode rdfs:domain sc:ContactPoint .\n")
    f.write("ug:roomCode rdfs:range sc:Text .\n\n")
    f.write("# Definizione del link riferito ad un url\n")
    f.write("ug:link rdf:type rdf:Property .\n")
    f.write("ug:link rdfs:label \"Collega un url al suo relativo collegamento\" .\n")
    f.write("ug:link rdfs:domain sc:URL .\n")
    f.write("ug:link rdfs:range sc:Text .\n\n")
    f.close()


def create_edificio(file):
    subj = input("Inserisci il soggetto all'edificio: ")
    file.write(f"\n# Definizione dell'edificio {subj}\n")
    file.write(f"{subj} rdf:type ug:CollegeOrUniversityBuilding .\n")
    name = input("Inserisci il nome dell'edificio: ")
    file.write(f"{subj} sc:name \"{name}\" .\n")
    create = input("Vuoi creare l'oggetto indirizzo relativo (y/n): ")
    if create == 'y':
        obj = create_indirizzo(file)
        file.write(f"\n# Assegnazione dell'edificio {subj} all'indirizzo {obj}\n")
        file.write(f"{subj} sc:address {obj} .\n")
        file.write(f"{obj} sc:address {subj} .\n")
    else:
        assign = input("Vuoi assegnare l'edificio ad un indirizzo esistente (y/n): ")
        if assign == 'y':
            assign_edificio_indirizzo(file, subj, '')
    create = input("Vuoi creare le coordinate dell'edificio (y/n): ")
    if create == 'y':
        obj = create_coordinata_geo(file)
        file.write(f"\n# Assegnazione dell'edificio {subj} alle coordinate geo {obj}\n")
        file.write(f"{subj} ug:geo {obj} .\n")
        file.write(f"{obj} ug:geo {subj} .\n")
    else:
        assign = input("Vuoi assegnare una coordinata geo esistente all'edificio (y/n): ")
        if assign == 'y':
            assign_coordinata_geo_dipartimento(file, '', obj)
    create = input("Vuoi creare il dipartimento relativo all'edificio (y/n): ")
    if create == 'y':
        obj = create_dipartimento(file)
        file.write(f"\n# Assegnazione del dipartimento {subj} all'indirizzo {obj}\n")
        file.write(f"{subj} sc:department {obj} .\n")
        file.write(f"{obj} sc:department {subj} .\n")
    else:
        assign = input("Vuoi assegnare un dipartimento esistente all'edificio (y/n): ")
        if assign == 'y':
            assign_dipartimento_edificio(file, '', subj)
    return subj


def create_indirizzo(file):
    subj = input("Inserisci il soggetto all'indirizzo: ")
    file.write(f"\n# Definizione dell'indirizzo {subj}\n")
    file.write(f"{subj} rdf:type ug:PostalAddress .\n")
    location = input("Inserisci la località dell'indirizzo: ")
    file.write(f"{subj} sc:addressLocality \"{location}\" .\n")
    street = input("Inserisci la via dell'indirizzo: ")
    file.write(f"{subj} sc:streetAddress \"{street}\" .\n")
    cap = input("Inserisci il codice postale dell'indirizzo: ")
    file.write(f"{subj} sc:postalCode \"{cap}\" .\n")
    return subj


def create_persona(file):
    subj = input("Inserisci il soggetto alla persona: ")
    file.write(f"\n# Definizione della persona {subj}\n")
    file.write(f"{subj} rdf:type sc:Person .\n")
    name = input("Inserisci il nome della persona: ")
    file.write(f"{subj} sc:name \"{name}\" .\n")
    surname = input("Inserisci il cognome della persona: ")
    file.write(f"{subj} sc:name \"{surname}\" .\n")
    create = input("Vuoi creare l'oggetto dell'occupazione della persona (y/n): ")
    if create == 'y':
        obj = create_occupazione(file)
        file.write(f"\n# Assegnazione della persona {subj} all'occupazione {obj}\n")
        file.write(f"{subj} sc:hasOccupation {obj} .\n")
        file.write(f"{obj} sc:hasOccupation {subj} .\n")
    else:
        assign = input("Vuoi assegnare la persona ad una occupazione esistente (y/n): ")
        if assign == 'y':
            assign_persona_occupazione(file, subj, '')
    create = input("Vuoi creare l'oggetto edificio affiliato alla persona (y/n): ")
    if create == 'y':
        obj = create_edificio(file)
        file.write(f"\n# Assegnazione della persona {subj} all'edificio {obj}\n")
        file.write(f"{subj} sc:employee {obj} .\n")
        file.write(f"{obj} sc:affiliation {subj} .\n")
    else:
        assign = input("Vuoi assegnare la persona ad un edificio esistente (y/n): ")
        if assign == 'y':
            assign_persona_edificio(file, subj, '')
    create = input("Vuoi creare il dipartimento dove lavora la persona (y/n): ")
    if create == 'y':
        obj = create_dipartimento(file)
        file.write(f"\n# Assegnazione della persona {subj} al dipartimento {obj}\n")
        file.write(f"{subj} sc:employee {obj} .\n")
        file.write(f"{obj} sc:worksFor {subj} .\n")
    else:
        assign = input("Vuoi assegnare la persona che lavora ad un dipartimento esistente (y/n): ")
        if assign == 'y':
            assign_persona_dipartimento(file, subj, '')
    create = input("Vuoi creare l'oggetto incarico della persona nel dipartimento (y/n): ")
    if create == 'y':
        obj = create_incarico(file)
        file.write(f"\n# Assegnazione della persona {subj} all'incarico {obj}\n")
        file.write(f"{subj} ug:assigment {obj} .\n")
        file.write(f"{obj} ug:assigment {subj} .\n")
    else:
        assign = input("Vuoi assegnare la persona ad un incarico esistente (y/n): ")
        if assign == 'y':
            assign_persona_incarico(file, subj, '')
    create = ''
    while create != 'n':
        create = input("Vuoi creare un contatto relativo alla persona (y/n): ")
        if create == 'y':
            obj = create_contatto(file)
            file.write(f"\n# Assegnazione della persona {subj} al contatto {obj}\n")
            file.write(f"{subj} sc:contactPoint {obj} .\n")
            file.write(f"{obj} sc:contactPoint {subj} .\n")
        else:
            assign = input("Vuoi assegnare la persona ad un contatto esistente (y/n): ")
            if assign == 'y':
                assign_persona_contatto(file, subj, '')
    create = ''
    while create != 'n':
        create = input("Vuoi associare l'url di un curriculum relativo alla persona (y/n): ")
        if create == 'y':
            obj = create_url(file)
            file.write(f"\n# Assegnazione della persona {subj} all'url {obj}\n")
            file.write(f"{subj} sc:url {obj} .\n")
            file.write(f"{obj} sc:url {subj} .\n")
        else:
            assign = input("Vuoi assegnare alla persona un curriculum esistente (y/n): ")
            if assign == 'y':
                assign_persona_url(file, subj, '')
    create = input("Vuoi associare un'immagine alla persona (y/n): ")
    if create == 'y':
        obj = create_immagine(file)
        file.write(f"\n# Assegnazione della persona {subj} all'immagine {obj}\n")
        file.write(f"{subj} sc:image {obj} .\n")
        file.write(f"{obj} sc:image {subj} .\n")
    else:
        assign = input("Vuoi assegnare alla persona un'immagine esistente (y/n): ")
        if assign == 'y':
            assign_persona_immagine(file, subj, '')
    create = input("Vuoi creare il ssd associato alla persona (y/n): ")
    if create == 'y':
        obj = create_ssd(file)
        file.write(f"\n# Assegnazione della persona {subj} al ssd {obj}\n")
        file.write(f"{subj} sc:member {obj} .\n")
        file.write(f"{obj} sc:member {subj} .\n")
    else:
        assign = input("Vuoi assegnare il ssd associato alla persona (y/n): ")
        if assign == 'y':
            assign_persona_ssd(file, subj, '')
    return subj


def create_occupazione(file):
    subj = input("Inserisci il soggetto all'occupazione: ")
    file.write(f"\n# Definizione dell'occupazione {subj}\n")
    file.write(f"{subj} rdf:type sc:Occupation .\n")
    qualifica = input("Inserisci la qualifica dell'occupazione: ")
    file.write(f"{subj} sc:qualifications \"{qualifica}\" .\n")
    return subj


def create_contatto(file):
    subj = input("Inserisci il soggetto al contatto: ")
    file.write(f"\n# Definizione del contatto {subj}\n")
    file.write(f"{subj} rdf:type sc:ContactPoint .\n")
    email = input("Inserisci l'email del contatto: ")
    if email != '':
        file.write(f"{subj} sc:email \"{email}\" .\n")
    telefono = input("Inserisci il telefono del contatto: ")
    if telefono != '':
        file.write(f"{subj} sc:telephone \"{telefono}\" .\n")
    fax = input("Inserisci il fax del contatto: ")
    if fax != '':
        file.write(f"{subj} sc:fax \"{fax}\" .\n")
    tipo = input("Inserisci il tipo del contatto: ")
    if tipo != '':
        file.write(f"{subj} sc:contactType \"{tipo}\" .\n")
    area = input("Inserisci l'area del contatto: ")
    if area != '':
        file.write(f"{subj} sc:areaServed \"{area}\" .\n")
    stanza = input("Inserisci il codice della stanza: ")
    if stanza != '':
        file.write(f"{subj} sc:description \"{stanza}\" .\n")
    create = input("Vuoi creare l'URL alla planimetria della stanza relativo al contatto (y/n): ")
    if create == 'y':
        obj = create_url(file)
        file.write(f"\n# Assegnazione del contatto {subj} all'url {obj}\n")
        file.write(f"{subj} sc:url {obj} .\n")
        file.write(f"{obj} sc:url {subj} .\n")
    else:
        assign = input("Vuoi assegnare al contatto l'URL della planimetria di una stanza esistente (y/n): ")
        if assign == 'y':
            assign_contatto_url(file, subj, '')
    return subj


def create_dipartimento(file):
    subj = input("Inserisci il soggetto al dipartimento: ")
    file.write(f"\n# Definizione del dipartimento {subj}\n")
    file.write(f"{subj} rdf:type ug:Department .\n")
    sigla = input("Inserisci la sigla del dipartimento: ")
    file.write(f"{subj} sc:branchCode \"{sigla}\" .\n")
    name = input("Inserisci il nome legale del dipartimento: ")
    file.write(f"{subj} sc:legalName \"{name}\" .\n")
    create = input("Vuoi creare l'oggetto indirizzo del dipartimento (y/n): ")
    if create == 'y':
        obj = create_indirizzo(file)
        file.write(f"\n# Assegnazione del dipartimento {subj} all'indirizzo {obj}\n")
        file.write(f"{subj} sc:address {obj} .\n")
        file.write(f"{obj} sc:address {subj} .\n")
    else:
        assign = input("Vuoi assegnare il dipartimento ad un indirizzo esistente (y/n): ")
        if assign == 'y':
            assign_dipartimento_indirizzo(file, subj, '')
    create = input("Vuoi creare l'url del dipartimento (y/n): ")
    if create == 'y':
        obj = create_url(file)
        file.write(f"\n# Assegnazione del dipartimento {subj} all'url {obj}\n")
        file.write(f"{subj} sc:url {obj} .\n")
        file.write(f"{obj} sc:url {subj} .\n")
    else:
        assign = input("Vuoi assegnare il dipartimento ad un URL esistente (y/n): ")
        if assign == 'y':
            assign_dipartimento_url(file, subj, '')
    create = ''
    while create != 'n':
        create = input("Vuoi creare il ruolo di una persona nel dipartimento (y/n): ")
        if create == 'y':
            obj = create_occupazione(file)
            file.write(f"\n# Assegnazione del dipartimento {subj} al contatto {obj}\n")
            file.write(f"{subj} sc:contactPoint {obj} .\n")
            file.write(f"{obj} sc:contactPoint {subj} .\n")
        else:
            assign = input("Vuoi assegnare al dipartimento un contatto di un dipartimento esistente (y/n): ")
            if assign == 'y':
                assign_dipartimento_contatto(file, subj, '')
    create = input("Vuoi creare le coordinate del dipartimento (y/n): ")
    if create == 'y':
        obj = create_coordinata_geo(file)
        file.write(f"\n# Assegnazione del dipartimento {subj} alla coordinata geo {obj}\n")
        file.write(f"{subj} ug:geo {obj} .\n")
        file.write(f"{obj} ug:geo {subj} .\n")
    else:
        assign = input("Vuoi assegnare una coordinata geo esistente al dipartimento (y/n): ")
        if assign == 'y':
            assign_coordinata_geo_dipartimento(file, '', subj)
    create = input("Vuoi creare l'edificio relativo al dipartimento (y/n): ")
    if create == 'y':
        obj = create_edificio(file)
        file.write(f"\n# Assegnazione del dipartimento {subj} all'ufficio {obj}\n")
        file.write(f"{subj} sc:department {obj} .\n")
        file.write(f"{obj} sc:department {subj} .\n")
    else:
        assign = input("Vuoi assegnare un edificio esistente al dipartimento (y/n): ")
        if assign == 'y':
            assign_dipartimento_edificio(file, '', subj)
    return subj


def create_incarico(file):
    subj = input("Inserisci il soggetto dell'incarico: ")
    file.write(f"\n# Definizione dell'incarico {subj}\n")
    file.write(f"{subj} rdf:type sc:Role .\n")
    name = input("Inserisci il nome dell'incarico: ")
    file.write(f"{subj} sc:roleName \"{name}\" .\n")
    return subj


def create_url(file):
    subj = input("Inserisci il soggetto dell'url: ")
    file.write(f"\n# Definizione dell'url {subj}\n")
    file.write(f"{subj} rdf:type sc:URL .\n")
    url = input("Inserisci l'url relativo: ")
    file.write(f"{subj} ug:link \"{url}\" .\n")
    descr = input("Inserisci la descrizione dell'url: ")
    file.write(f"{subj} sc:description \"{descr}\" .\n")
    return subj


def create_immagine(file):
    subj = input("Inserisci il soggetto dell'immagine: ")
    file.write(f"\n# Definizione dell'immagine {subj}\n")
    file.write(f"{subj} rdf:type sc:ImageObject .\n")
    caption = input("Inserisci la didascalia relativo: ")
    file.write(f"{subj} sc:caption \"{caption}\" .\n")
    format = input("Inserisci il formato dell'immagine: ")
    file.write(f"{subj} sc:encodingFormat \"{format}\" .\n")
    height = input("Inserisci l'altezza dell'immagine: ")
    file.write(f"{subj} sc:encodingFormat \"{height}\" .\n")
    width = input("Inserisci la larghezza dell'immagine: ")
    file.write(f"{subj} sc:encodingFormat \"{width}\" .\n")
    create = input("Vuoi creare l'url dell'immagine (y/n): ")
    if create == 'y':
        obj = create_url(file)
        file.write(f"\n# Assegnazione dell'immagine {subj} all'url {obj}\n")
        file.write(f"{subj} sc:url {obj} .\n")
        file.write(f"{obj} sc:url {subj} .\n")
    else:
        assign = input("Vuoi assegnare il dipartimento ad un URL esistente (y/n): ")
        if assign == 'y':
            assign_immagine_url(file, subj, '')
    return subj


def create_coordinata_geo(file):
    subj = input("Inserisci il soggetto di coordinate geo: ")
    file.write(f"\n# Definizione della coordinata geo {subj}\n")
    file.write(f"{subj} rdf:type geo:Point .\n")
    lat = input("Inserisci la latitudine relativa: ")
    file.write(f"{subj} sc:lat \"{lat}\"^^xsd:float .\n")
    long = input("Inserisci la longitudine relativa: ")
    file.write(f"{subj} sc:long \"{long}\"^^xsd:float .\n")
    return subj


def create_ssd(file):
    subj = input("Inserisci il soggetto di settore scientifico disciplinare: ")
    file.write(f"\n# Definizione del ssd {subj}\n")
    file.write(f"{subj} rdf:type ug:Ssd .\n")
    name = input("Inserisci il nome relativo: ")
    file.write(f"{subj} sc:legalName {name} .\n")
    code = input("Inserisci il codice relativo: ")
    file.write(f"{subj} sc:branchCode {code} .\n")
    return subj


def assign_edificio_indirizzo(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto dell'edificio: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'indirizzo: ")
    file.write(f"\n# Assegnazione dell'edificio {subj} all'indirizzo {obj}\n")
    file.write(f"{subj} sc:address {obj} .\n")
    file.write(f"{obj} sc:address {subj} .\n")


def assign_dipartimento_indirizzo(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'indirizzo: ")
    file.write(f"\n# Assegnazione del dipartimento {subj} all'indirizzo {obj}\n")
    file.write(f"{subj} sc:address {obj} .\n")
    file.write(f"{obj} sc:address {subj} .\n")


def assign_persona_edificio(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'edificio: ")
    file.write(f"\n# Assegnazione della persona {subj} all'edificio {obj}\n")
    file.write(f"{subj} sc:affiliation {obj} .\n")
    file.write(f"{obj} sc:employee {subj} .\n")


def assign_persona_occupazione(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'occupazione: ")
    file.write(f"\n# Assegnazione della persona {subj} all'occupazione {obj}\n")
    file.write(f"{subj} sc:hasOccupation {obj} .\n")
    file.write(f"{obj} sc:hasOccupation {subj} .\n")


def assign_persona_contatto(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto del contatto: ")
    file.write(f"\n# Assegnazione della persona {subj} al contatto {obj}\n")
    file.write(f"{subj} sc:contactPoint {obj} .\n")
    file.write(f"{obj} sc:contactPoint {subj} .\n")


def assign_persona_dipartimento(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto del dipartimento: ")
    file.write(f"\n# Assegnazione della persona {subj} al dipartimento {obj}\n")
    file.write(f"{subj} sc:worksFor {obj} .\n")
    file.write(f"{obj} sc:employee {subj} .\n")


def assign_persona_incarico(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'incarico: ")
    file.write(f"\n# Assegnazione della persona {subj} all'incarico {obj}\n")
    file.write(f"{subj} ug:assignment {obj} .\n")
    file.write(f"{obj} ug:assignment {subj} .\n")


def assign_persona_url(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'url: ")
    file.write(f"\n# Assegnazione della persona {subj} all'url {obj}\n")
    file.write(f"{subj} sc:url {obj} .\n")
    file.write(f"{obj} sc:url {subj} .\n")


def assign_persona_immagine(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'immagine: ")
    file.write(f"\n# Assegnazione della persona {subj} all'immagine {obj}\n")
    file.write(f"{subj} sc:image {obj} .\n")
    file.write(f"{obj} sc:image {subj} .\n")


def assign_immagine_url(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto dell'immagine': ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'url: ")
    file.write(f"\n# Assegnazione dell'immagine {subj} all'url {obj}\n")
    file.write(f"{subj} sc:url {obj} .\n")
    file.write(f"{obj} sc:url {subj} .\n")


def assign_contatto_url(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del contatto: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'url: ")
    file.write(f"\n# Assegnazione del contatto {subj} all'url {obj}\n")
    file.write(f"{subj} sc:url {obj} .\n")
    file.write(f"{obj} sc:url {subj} .\n")


def assign_dipartimento_url(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'url: ")
    file.write(f"\n# Assegnazione del dipartimento {subj} all'url {obj}\n")
    file.write(f"{subj} sc:url {obj} .\n")
    file.write(f"{obj} sc:url {subj} .\n")


def assign_dipartimento_contatto(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto del contatto: ")
    file.write(f"\n# Assegnazione del dipartimento {subj} al contatto {obj}\n")
    file.write(f"{subj} sc:contactPoint {obj} .\n")
    file.write(f"{obj} sc:contactPoint {subj} .\n")


def assign_dipartimento_occupazione(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'occupazione: ")
    file.write(f"\n# Assegnazione del dipartimento {subj} all'occupazione {obj}\n")
    file.write(f"{subj} ug:occupationDepartment {obj} .\n")
    file.write(f"{obj} ug:occupationDepartment {subj} .\n")


def assign_coordinata_geo_edificio(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto dell'edificio: ")
    if obj == '':
        obj = input("Inserisci l'oggetto della coordinata geo: ")
    file.write(f"\n# Assegnazione delle coordinate geo {subj} all'edificio {obj}\n")
    file.write(f"{subj} ug:geo {obj} .\n")
    file.write(f"{obj} ug:geo {subj} .\n")


def assign_coordinata_geo_dipartimento(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto della coordinata geo: ")
    file.write(f"\n# Assegnazione delle coordinate geo {subj} al dipartimento {obj}\n")
    file.write(f"{subj} ug:geo {obj} .\n")
    file.write(f"{obj} ug:geo {subj} .\n")


def assign_dipartimento_edificio(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto del dipartimento: ")
    if obj == '':
        obj = input("Inserisci l'oggetto dell'edificio: ")
    file.write(f"\n# Assegnazione del dipartimento {subj} all'edificio {obj}\n")
    file.write(f"{subj} sc:department {obj} .\n")
    file.write(f"{obj} sc:department {subj} .\n")


def assign_occupazione_dipartimento(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto dell'occupazione: ")
    if obj == '':
        obj = input("Inserisci l'oggetto del dipartimento: ")
    file.write(f"\n# Assegnazione dell'occupazione {subj} al dipartimento {obj}\n")
    file.write(f"{subj} ug:OccupationDepartment {obj} .\n")
    file.write(f"{obj} ug:OccupationDepartment {subj} .\n")


def assign_persona_ssd(file, subj, obj):
    if subj == '':
        subj = input("Inserisci il soggetto della persona: ")
    if obj == '':
        obj = input("Inserisci l'oggetto del ssd: ")
    file.write(f"\n# Assegnazione della persona {subj} al ssd {obj}\n")
    file.write(f"{subj} sc:member {obj} .\n")
    file.write(f"{obj} sc:member {subj} .\n")


if __name__ == '__main__':

    filename = input("Seleziona il nome del file (senza estensione): ")
    filename = f'{filename}.ttl'

    file_exists = exists(f'./{filename}')
    if not file_exists:
        create_ontology(filename)

    value = ''

    file = open(filename, "a+")

    while value != 'q':
        print('Seleziona un tra le seguenti operazioni digitando la lettera iniziale.\n')

        print('1) Aggiungi un soggetto')
        print('2) Assegna un soggetto ad un oggetto')
        print('3) Esci dal programma')

        value = input("Inserisci un'operazione: ")

        if value == '1':
            while value != 'z':
                print('a) Aggiungi un edificio')
                print('b) Aggiungi un indirizzo')
                print('c) Aggiungi una persona')
                print('d) Aggiungi una occupazione ')
                print('e) Aggiungi un contatto')
                print('f) Aggiungi un url')
                print('g) Aggiungi una immagine')
                print('h) Aggiungi un dipartimento')
                print('i) Aggiungi una coordinata geo')
                print('j) Aggiungi un settore scientifico disciplinare')
                print('z) Torna indietro')

                value = input("Inserisci un'operazione: ")

                if value == 'a':
                    create_edificio(file)
                if value == 'b':
                    create_indirizzo(file)
                if value == 'c':
                    create_persona(file)
                if value == 'd':
                    create_occupazione(file)
                if value == 'e':
                    create_contatto(file)
                if value == 'f':
                    create_url(file)
                if value == 'g':
                    create_immagine(file)
                if value == 'h':
                    create_dipartimento(file)
                if value == 'i':
                    create_coordinata_geo(file)
                if value == 'j':
                    create_ssd(file)

        if value == '2':
            while value != 'z':
                print('a) Assegna un indirizzo ad un edificio')
                print('b) Assegna un indirizzo ad un dipartimento')
                print('c) Assegna una persona ad un edificio')
                print('d) Assegna una persona ad un dipartimento')
                print('e) Assegna una persona ad un incarico')
                print('f) Assegna una occupazione ad una persona')
                print('g) Assegna un contatto ad una persona')
                print('h) Assegna un url ad una persona')
                print('i) Assegna una immagine ad una persona')
                print('j) Assegna una immagine ad un url')
                print('k) Assegna un url ad un contatto')
                print('l) Assegna un contatto ad un dipartimento')
                print('m) Assegna una coordinata geo ad un edificio')
                print('n) Assegna una coordinata geo ad un dipartimento')
                print('o) Assegna una occupazione ad un dipartimento')
                print('p) Assegna una edificio ad un dipartimento')
                print('q) Assegna un contatto ad un dipartimento')
                print('r) Assegna una persona ad un settore scientifico disciplinare')
                print('z) Torna indietro')

                value = input("Inserisci un'operazione: ")

                if value == 'a':
                    assign_edificio_indirizzo(file, '', '')
                if value == 'b':
                    assign_dipartimento_indirizzo(file, '', '')
                if value == 'c':
                    assign_persona_edificio(file, '', '')
                if value == 'd':
                    assign_persona_dipartimento(file, '', '')
                if value == 'e':
                    assign_persona_incarico(file, '', '')
                if value == 'f':
                    assign_persona_occupazione(file, '', '')
                if value == 'g':
                    assign_persona_contatto(file, '', '')
                if value == 'h':
                    assign_persona_url(file, '', '')
                if value == 'i':
                    assign_persona_immagine(file, '', '')
                if value == 'j':
                    assign_immagine_url(file, '', '')
                if value == 'k':
                    assign_contatto_url(file, '', '')
                if value == 'l':
                    assign_dipartimento_contatto(file, '', '')
                if value == 'm':
                    assign_coordinata_geo_edificio(file, '', '')
                if value == 'n':
                    assign_coordinata_geo_dipartimento(file, '', '')
                if value == 'o':
                    assign_dipartimento_occupazione(file, '', '')
                if value == 'p':
                    assign_dipartimento_edificio(file, '', '')
                if value == 'q':
                    assign_occupazione_dipartimento(file, '', '')
                if value == 'r':
                    assign_persona_ssd(file, '', '')

        if value == '3':
            break

    file.close()