#!usr/bin/env python
from urllib2 import unquote
from flask import Flask
from flask_restful import Api, Resource, reqparse
from auto_complete import completer
app = Flask("cityName")
api = Api(app)

"""
Exception class
"""
class ProcessException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(ProcessException, self).__init__(message)
        self.errors = errors


class ModelSuggest(Resource):
    """Suggest values using model."""
    def __init__(self):


        # see http://flask-restful.readthedocs.io/en/0.3.5/reqparse.html
        # all errors are bundled, if any and returned
        self.reqparser = reqparse.RequestParser(bundle_errors=True)
        self.reqparser.add_argument('q',
                                    required=True,
                                    type=str
                                    )
        self.reqparser.add_argument('latitude',
                                    type=float
                                    )
        self.reqparser.add_argument('longitude',
                                    type=float
                                    )
        self.reqparser.add_argument('radius',
                                    type=float
                                    )

        """Initialize model class to be used."""
        self.model = completer("./pickle_data/geoPT.pkl")

        super(ModelSuggest, self).__init__()

    def get(self):
        """Parse out required inputs for model and pass them to your model."""

        args = self.reqparser.parse_args()

        try:
            # ensure the input is correct

            qstr = unquote(args['q'])
            
            # qstr = args['q']

            lat = None
            lng = None
            radius = None
            if args["latitude"] and not args["longitude"]:
                raise ProcessException(
                                          'only latitude given',
                                          422
                                         )
            if args["longitude"] and not args["latitude"]:
                raise ProcessException(
                                          'only longitude given',
                                          422
                                         )
            # now we know if latitude is here so will be longitude
            if args["latitude"]:
                lat = args["latitude"]
                if (lat < -90 or lat > 90):
                    raise ProcessException(
                                              'latitude out of range',
                                              412
                                             )
                lng = args["longitude"]
                if (lng < -90 or lng > 90):
                    raise ProcessException(
                                              'longitude out of range',
                                              412
                                             )
                # only deal with radius in the presense of lat and lng
                if args["radius"]:
                    radius = abs(args["radius"])

            result = self.model.complete(qstr, lat, lng, radius)

        except ProcessException as e:
            # our API did not perform its task for some reason, therefore return
            # a 500 error with a relevant message
            return {'status': 'Failed:  %s' % str(e)}, e.errors

        else:
            # API Successfully completed task.  Return result and 200 status
            # code
            return {'suggestions': result}, 200

"""
Create endpoints for your classes. You should add a new resource
for every class you make. Your endpoints should follow some kind of structure.
"""


def run():
    api.add_resource(ModelSuggest, '/suggestions')
    app.run("0.0.0.0", port=5000)

if __name__ == "__main__":
    """Host service on port 5000."""
    run()
