from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        #   if the object to decode is the same class as what's in the
        #   model property, then
        #     * create an empty dictionary that will hold the property names
        #       as keys and the property values as values
        #     * for each name in the properties list
        #         * get the value of that property from the model instance
        #           given just the property name
        #         * put it into the dictionary with that property name as
        #           the key
        #     * return the dictionary
        #   otherwise,
        #       return super().default(o)  # From the documentation
        if isinstance(o, self.model):
            d = {}
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            # iterate over all the properties
            for property in self.properties:
                # assign the attribute of the current property to value variable
                value = getattr(o, property)
                # if the current property is in encoders (location)
                if property in self.encoders:
                    # assign value of encoders (linked to Location) property (name) to encoder variable
                    encoder = self.encoders[property]
                    # new value is the json.dumps JSON of encoder (or name)
                    value = encoder.default(value)
                # create property key with value
                d.update(self.get_extra_data(o))
                d[property] = value
            return d
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}
