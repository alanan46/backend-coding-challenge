#!usr/bin/env python
from PT import PT
import cPickle

# build the Patricia Tree and save it to a pickle file so that we can load it
# from disk
def build(fName_in, fName_out):
    pt = PT()
    with open(fName_in, "rb") as g:
        unpickler = cPickle.Unpickler(g)
    # test = [
    #     ["London", "42.98", "-81.233", 150000],
    #     ["London", "39.88", "-83.44", 22321],
    #     ["Londontowne", "38.933", "-76.54", 122],
    #     ["montreal", '38', '38', 1233333],
    #     ["mont-royal", '45', '45', 1223]
    #     ]
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
