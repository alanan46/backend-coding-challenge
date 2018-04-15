#! usr/bin/env python
import cPickle
from CA_CODE import *

def _format(output, fname):
    with open(fname) as ctry:
        next(ctry)
        for aLine in ctry:
            line = aLine.rstrip().split('\t')
            state_abbr = line[STATE]
            if (state_abbr in CA_PROVINCE_CODE.keys()):
                state_abbr = CA_PROVINCE_CODE[line[STATE]]
            temp = [line[GEONAME],
                    line[LATITUDE],
                    line[LONGITUDE],
                    state_abbr,
                    line[POPULATION]
                    ]
            output.append(temp)
        ctry.close()


def format_info(fName_in, fName_out):
    try:
        res = []
        _format(res, fName_in)
        i = 1
        with open(fName_out, 'wb') as out:
            pickler = cPickle.Pickler(out)

            for row in res:
                print i, row
                i += 1
                pickler.dump(row)
            out.close()
    except IOError:
        print "IO Error"
        pass

if __name__ == "__main__":
    format_info("cities_canada-usa.tsv", "geodatanew.pkl")
