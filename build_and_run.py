#!usr/bin/env python
import preprocess.preprocess as process
import pt.build_pt as bld
import city_api


def main():
    process.format_info("./data/cities_canada-usa.tsv",
                        "./pickle_data/geodatanew.pkl")
    bld.build("./pickle_data/geodatanew.pkl", "./pickle_data/geoPT.pkl")
    city_api.run()


if __name__ == "__main__":
    main()
