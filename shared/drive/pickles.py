import pickle

from shared.drive import drive as drv


def println(fn):
    print(load(fn))

def confirm(fn, linReg):
    if drv.exist(fn) == False:
        save(fn, linReg)
        print('Pickle doesn\'t exist; Creating new pickle.')

def save(fn, linReg):
    with open(fn, 'wb') as f:
        pickle.dump(linReg, f)

def load(fn):
    pickle_in = open(fn, 'rb')
    return pickle.load(pickle_in)