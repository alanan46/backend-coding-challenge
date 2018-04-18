# Coveo Backend Coding Challenge
(inspired by https://github.com/busbud/coding-challenge-backend-c)
PERSONAL HOSTING AT
https://city-name-autocomplete.herokuapp.com

## TO RUN
python city_api.py 
(given you have the .pkl data file ready)
### or
python build_and_run.py
(run the whole preprocess --> buildtree --> host API procedure)
## OVERVIEW
1.preprocess the raw data to extract the needed fields
In this case, the city name, latitude, longitude, State/Province name, population
2. Build a Patricia tree to store the data in a tree format, as it imporves search spead than the trivial
linear search. It also has the advantage over ternary search tree(TST). The TST's memory usage 
depends on the depth of the tree which in turn, depends on the length of city name.
If there are some long names in the data, TST becomes very RAM-inefficient.
Patricia Tree could be considered as an improvement of TST.(https://en.wikipedia.org/wiki/Radix_tree)
However, note that the build time for TST is much faster. (If just play around with concept, it is a good
idea to start with TST)
3.  Store the grown tree in a pickle file and load the tree in the completer object to response the incoming query.
4. use FLASK libraries to handle api requests,( parsing,error handling etc).
5. use POSTMAN to test.
### About the algo and features
give a slightly more weights to larger cities, as they might be more popular.
have an additional api parameter called radius,(unit is KM)
it takes a positive float and must be used with latitude and longitude.
If this parameter is present, will only show the result within this radius.

## Requirements

Design an API endpoint that provides auto-complete suggestions for large cities.

- The endpoint is exposed at `/suggestions`
- The partial (or complete) search term is passed as a querystring parameter `q`
- The caller's location can optionally be supplied via querystring parameters `latitude` and `longitude` to help improve relative scores
- The endpoint returns a JSON response with an array of scored suggested matches
    - The suggestions are sorted by descending score
    - Each suggestion has a score between 0 and 1 (inclusive) indicating confidence in the suggestion (1 is most confident)
    - Each suggestion has a name which can be used to disambiguate between similarly named locations
    - Each suggestion has a latitude and longitude

## "The rules"

- *You can use the language and technology of your choosing.* It's OK to try something new (tell us if you do), but feel free to use something you're comfortable with. We don't care if you use something we don't; the goal here is not to validate your knowledge of a particular technology.
- End result should be deployed on a public Cloud (Heroku, AWS etc. all have free tiers you can use).

## Advices

- **Try to design and implement your solution as you would do for real production code**. Show us how you create clean, maintainable code that does awesome stuff. Build something that we'd be happy to contribute to. This is not a programming contest where dirty hacks win the game.
- Feel free to add more features! Really, we're curious about what you can think of. We'd expect the same if you worked with us.
- Documentation and maintainability is a plus.
- Don't you forget those unit tests.
- We don’t want to know if you can do exactly as asked (or everybody would have the same result). We want to know what **you** bring to the table when working on a project, what is your secret sauce. More features? Best solution? Thinking outside the box?

## Sample responses

These responses are meant to provide guidance. The exact values can vary based on the data source and scoring algorithm

**Near match**

    GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163

```json
{
  "suggestions": [
    {
      "name": "London, ON, Canada",
      "latitude": "42.98339",
      "longitude": "-81.23304",
      "score": 0.9
    },
    {
      "name": "London, OH, USA",
      "latitude": "39.88645",
      "longitude": "-83.44825",
      "score": 0.5
    },
    {
      "name": "London, KY, USA",
      "latitude": "37.12898",
      "longitude": "-84.08326",
      "score": 0.5
    },
    {
      "name": "Londontowne, MD, USA",
      "latitude": "38.93345",
      "longitude": "-76.54941",
      "score": 0.3
    }
  ]
}
```

**No match**

    GET /suggestions?q=SomeRandomCityInTheMiddleOfNowhere

```json
{
  "suggestions": []
}
```

## References

- Geonames provides city lists Canada and the USA http://download.geonames.org/export/dump/readme.txt

## Getting Started

Begin by forking this repo and cloning your fork. GitHub has apps for [Mac](http://mac.github.com/) and
[Windows](http://windows.github.com/) that make this easier.



