"""Records module"""
import json
import falcon
import jsend
from ..models.record import Record

class Records():
    """ Records class """
    def on_get(self, req, resp, parcel):
        """ Handles GET requests
        If `parcel` number is passed, do a look up on data available on the parcel record

        Parcel (Block/Lot) can be found online via https://sfplanninggis.org/pim/
        """
        if parcel:
            self.on_get_records(req, resp, parcel)
        else:
            msg = {'message': falcon.HTTP_200}
            resp.body = json.dumps(jsend.success(msg))
            resp.status = falcon.HTTP_200

    #pylint: disable=no-self-use
    def on_get_records(self, req, resp, parcel):
        """ Look up record for `parcel`
        multiple `fields` names can be passed using comma delimiter
        """
        fields = []
        if 'fields' in req.params:
            fields_string = req.params['fields'] or None
            if fields_string:
                fields = fields_string.split(',')
        msg = Record(parcel).get(fields)
        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200
