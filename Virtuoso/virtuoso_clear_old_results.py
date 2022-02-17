import os
import argparse
import shutil
import time

parser = argparse.ArgumentParser(description = "Parser per query")
parser.add_argument("-d", "--days", help = "Numero dei giorni", required = True)

argument = parser.parse_args()
days = int(argument.days)

print(f"\nIl numero di giorni oltre il quale le cartelle verranno rimosse è di {days} giorni\n")
path = "./"
now = time.time()
old = now - (days * 24 * 60 * 60) 

for root, dirs, files in os.walk(path, topdown=False):
    for _dir in dirs:
        if _dir.startswith("Results_") and os.path.getmtime(_dir) < old:
            try:
                shutil.rmtree(_dir)
            except OSError as e:
                print("Errore: %s - %s." % (e.filename, e.strerror))
                
print(f"Operazione completata\n")