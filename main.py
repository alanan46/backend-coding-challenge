#!usr/bin/env python
import preprocess as process
import buildPT as bld
import cityApi
def main():
    process.format_info("./data/cities_canada-usa.tsv", "geodatanew.pkl")
    bld.build("geodatanew.pkl", "geoPT.pkl")
    cityApi.run()


if __name__ == "__main__":
    main()
