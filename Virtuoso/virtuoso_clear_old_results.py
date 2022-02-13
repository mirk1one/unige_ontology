import os
import sys
import shutil
import time

days = input("Inserire il numero di giorni oltre il quale le cartelle verranno rimosse: ")
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