from SPARQLWrapper import SPARQLWrapper, TURTLE
from datetime import datetime
import os
import time

def call_local_sparql(query, select, scriptName):
  start_time = time.time()
  
  sparql = SPARQLWrapper('http://localhost:8890/sparql')
  sparql.setQuery(f''' {query} ''') 
  sparql.setReturnFormat(TURTLE)
  results = sparql.query().convert()
  
  print("\nTempo esecuzione query: %s secondi" % (time.time() - start_time))
  
  now = datetime.now()
  
  nowDStr = now.strftime("%Y_%m_%d")
  dir_name = 'Results_' + nowDStr
  
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)
  
  nowDTStr = now.strftime("%Y_%m_%d_%H_%M_%S")
  file_name = scriptName + '_' + nowDTStr + '.ttl'
  
  f = open(dir_name + '/' + file_name, "w")
  f.write(str(results,'utf-8'))
  f.close()
  
  labels, results = parse_turtle_string(str(results,'utf-8'))
  
  print("\nRISULTATI\n\n| ", end = '')
  print(*labels, sep=" | ", end = '')
  print(" | ")
  
  if (len(results) != 0):
    for res in results:
      print("| ", end = '')
      for lab in labels:
        value = res.get(lab, "")
        print(value + " | ", end = '')
      print("\n")
  else:
    print("Nessun risultato trovato\n")

def parse_turtle_string(result):
  prefixes = {}
  labels = []
  results = []
  data = {}
  lines = result.replace("\t"," ").split("\n")
  found = False
  for l in lines:
    l = l.replace(" .", "").lstrip()
    if l.startswith("@prefix"):
      prefix = l.split(' ', 1)[1].split(' ')
      prefixes[prefix[0]] = prefix[1].replace("<","").replace(">","")
    elif l.startswith("_:_ res:resultVariable"):
      labels = l.split(' ', 2)[2].replace("\"","").split(" , ")
    elif l.startswith("_:_ res:solution") and data:
      results.append(data)
      data = {}
    elif l.startswith("res:binding"):
      found = True
      label = l.split(' ')[3].replace("\"","")
      value = l.split(' ', 6)[6]
      if value.startswith("\""):
        endStr = value.index("\"",1) + 1
        value = value[:endStr]
      else:
        value = value.split()[0]
        for prefix, namespace in prefixes.items():
          value = value.replace(prefix, namespace)
      data[label] = value
  if(found):
    results.append(data)
  return labels, results
      