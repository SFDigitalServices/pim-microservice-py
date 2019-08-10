"""Records module"""
import json
import falcon
import jsend
from ..models.record import Record

class Records():
    """ Records class """
    def on_get(self, req, resp, parcel):
        """ on get request
        return Records data
        """
        if parcel:
            return self.on_get_records(req, resp, parcel)
        msg = {'message': 'Records'}
        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200

    def on_get_records(self, req, resp, parcel):
        """ on get records """
        fields = []
        if 'fields' in req.params:
            fields_string = req.params['fields'] or None
            if fields_string:
                fields = fields_string.split(',')
        msg = Record(parcel).get(fields)
        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200
