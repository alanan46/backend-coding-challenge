#! usr/bin/env python
import cPickle


def _format(output, fName):
    CA_CODE = {
                "01": "AB",
                "02": "BC",
                "03": "MB",
                "04": "NB",
                "05": "NL",
                "07": "NS",
                "08": "ON",
                "09": "PE",
                "10": "QC",
                "11": "SK",
                "12": "YT",
                "13": "NT",
                "14": "NU"
            }
    with open(fName) as ctry:
        line = next(ctry)
        header = line.rstrip().split('\t')
        geoName = header.index("name")
        lat = header.index("lat")
        lng = header.index("long")
        state = header.index("admin1")
        population = header.index("population")
        for line in ctry:
            try:
                row = line.rstrip().split('\t')
                state_abbr = row[state]
                if (state_abbr in CA_CODE.keys()):
                    state_abbr = CA_CODE[row[state]]
                temp = [row[geoName],
                        row[lat],
                        row[lng],
                        state_abbr,
                        row[population]
                        ]
                output.append(temp)
            except IndexError:
                pass
        ctry.close()


def format_info(fName_in, fName_out):
    try:
        res = []
        _format(res, fName_in)

        with open(fName_out, 'wb') as out:
            pickler = cPickle.Pickler(out)

            for row in res:
                pickler.dump(row)
            out.close()
    except IOError:
        pass


if __name__ == "__main__":
    format_info("../data/cities_canada-usa.tsv",
                "../pickle_data/geodatanew.pkl")
