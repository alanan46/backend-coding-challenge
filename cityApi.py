#!usr/bin/env python

from flask import Flask
from flask_restful import Api, Resource, reqparse
from autocomplete import completer
app = Flask("cityName")
api = Api(app)


class ProcessException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(ProcessException, self).__init__(message)
        self.errors = errors


# @app.route('/suggestions')
class ModelPredict(Resource):
    """Predict values using model."""
    def __init__(self):


        # see http://flask-restful.readthedocs.io/en/0.3.5/reqparse.html
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('q',
                                    required=True,
                                    type=str,
                                    action='append')
        self.reqparser.add_argument('latitude',
                                    type=float,
                                    action='append')
        self.reqparser.add_argument('longitude',
                                    type=float,
                                    action='append')
        self.reqparser.add_argument('radius',
                                    type=float,
                                    action='append')

        """Initialize model class to be used."""
        self.model = completer("geoPT.pkl")

        super(ModelPredict, self).__init__()

    def get(self):
        """Parse out required inputs for model and pass them to your model."""

        args = self.reqparser.parse_args()

        try:
            # ensure the input is correct
            qstr = args['q'][0]
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
                lat = args["latitude"][0]
                if (lat < -90 or lat > 90):
                    raise ProcessException(
                                              'latitude out of range',
                                              412
                                             )
                lng = args["longitude"][0]
                if (lng < -90 or lng > 90):
                    raise ProcessException(
                                              'longitude out of range',
                                              412
                                             )
                # only deal with radius in the presense of lat and lng
                if args["radius"]:
                    radius = abs(args["radius"][0])
            print args
            result = self.model.complete(qstr, lat, lng, radius)

        except ProcessException as e:
            # our API did not perform its task for some reason, therefore return
            # a 500 error with a relevant message
            return {'status': 'Failed:  %s'%str(e)}, e.errors

        else:
            # API Successfully completed task.  Return result and 200 status
            # code
            return {'suggestions': result}, 200

"""
Create endpoints for your classes. You should add a new resource
for every class you make. Your endpoints should follow some kind of structure.
"""



def run():
    api.add_resource(ModelPredict, '/suggestions')
    app.run("0.0.0.0", port=5000)

if __name__ == "__main__":
    """Host service on port 5000."""
    run()
