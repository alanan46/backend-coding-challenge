#!usr/bin/env python
import cPickle
import math
from CA_CODE import *


class completer(object):
    def __init__(self, fName):
        self.tree = self.loadTree(fName)

    def loadTree(self, fName):
        try:
            with open(fName, "rb") as g:
                unpickler = cPickle.Unpickler(g)
                tree = unpickler.load()
                return tree
        except IOError:
            print "file IO error"
            return None

    def getSigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    # here we use a rather simple distance score function
    def getStringScore(self, queryKey, resKey):
        d = (len(resKey) - len(queryKey)) / 8.0
        return 1-self.getSigmoid(d)

    def getGeoDistance(self, origin, destination):
        """
        Calculate the Haversine distance.

        Parameters
        ----------
        origin : tuple of float
            (lat, long)
        destination : tuple of float
            (lat, long)

        Returns
        -------
        distance_in_km : float

        """
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371  # earth radius in km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return abs(round(d, 1))

    def getGeoScore(self, origin, destination):
            d = self.getGeoDistance(origin, destination)
            if d < 100:
                score = 2.5
            elif d >= 100 and d < 200:
                score = 1.0
            elif d >= 200 and d < 500:
                score = -0.5
            else:
                score = -2.0
            return score

    # higher score for bigger city
    def getPopulationScore(self, population):
        if population > 5000 and population < 15000:
            score = 0.1
        elif population > 15000 and population < 50000:
            score = 0.2
        elif population > 50000:
            score = 0.4
        else:
            score = 0.0
        return score

    # # a wrapper to provide the required funciton
    # def predict(self, qString=None, lat=None, lng=None, radius=None):
    #     return self.complete(qString, lat, lng, radius)

    def complete(self, qString, latitude=None, longitude=None, radius=None):
        if(not self.tree or len(qString) < 1):
            return {}
        # incase user input not capitalized
        qString.capitalize()
        raw = self.tree.findSuffix(qString)
        temp = []
        for name in raw.keys():
            for data in raw[name]:
                # if radius is used we filter out the out of range places
                if (radius and self.getGeoDistance(
                                (latitude, longitude),
                                (float(data[0]),
                                    float(data[1]))
                                        ) > radius):
                    continue
                cName = "Canada" if data[2] in CA_PROVINCE_CODE.values()\
                        else "USA"
                uniqueName = name + ", " + data[2]+", "+cName
                score = 0
                if(latitude and longitude):
                    score = self.getGeoScore(
                                    (latitude, longitude),
                                    (float(data[0]),
                                        float(data[1]))
                                             )
                score += self.getStringScore(qString, name)
                score += self.getPopulationScore(int(data[-1]))
                # ensure score is positive
                score = max(round(self.getSigmoid(score), 2), 0)
                i = 0
                # insertion while maintain desc order on score
                while (i < len(temp)):
                    if temp[i]["score"] < score:
                        break
                    i += 1
                temp.insert(i,
                            {"name": uniqueName,
                             "latitude": data[0],
                             "longitude": data[1],
                             "score": score
                             }
                            )
        return temp
