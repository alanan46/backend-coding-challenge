#!usr/bin/env python
from pt import PT
import cPickle


# build the Patricia Tree and save it to a pickle file so that we can load it
# from disk
def build(fName_in, fName_out):
    pt = PT()
    with open(fName_in, "rb") as g:
        unpickler = cPickle.Unpickler(g)
        while True:
            try:
                row = unpickler.load()
                pt.insert(row[0], row[1:])
            except EOFError:
                break
        g.close()
    with open(fName_out, "wb") as gt:
        pickler = cPickle.Pickler(gt)
        pickler.dump(pt)
        gt.close()


if __name__ == "__main__":
    build("../pickle_data/geodatanew.pkl", "../pickle_data/geo_pt.pkl")
