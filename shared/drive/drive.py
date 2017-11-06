from os.path import exists
import os

def getDirFiles(fp):
    return os.listdir(fp)

def exist(fn):
    return exists(fn)

def save (fn, cont):
    fw = open(fn, 'w')
    fw.write(cont)
    fw.close()

def confirm (fn, cont=''):
    if (exists(fn)) == False:
        save(fn, cont)

def load (fn):
    fr = open(fn, 'r')
    s = fr.read()
    fr.close()
    return s

def append (fn, app):
    cont = load(fn)
    cont = cont + app
    save(fn, cont)

def confirmDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)