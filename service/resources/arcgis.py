"""ArcGIS module"""
import os
import json
import falcon
import jsend
from sf_arcgis_sdk.sf_arcgis import SfArcgis

class Arcgis():
    """Welcome class"""
    def on_get(self, req, resp, name=None):
        """on get request
        return Arcgis message
        """
        if not name:
            name = req.path.strip('/')
        if name in dir(self):
            return getattr(self, name)(req, resp)
        msg = {'message': 'Welcome'}
        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200

    def parcels(self, req, resp):
        """ get parcels """

        missing_env = self.has_missing_env(['PLN_ARCGIS_PARCEL'])
        if missing_env:
            resp.status = falcon.HTTP_404
            msg_error = jsend.error(
                'Missing or invalid environment variable(s): '+", ".join(missing_env))
            resp.body = json.dumps(msg_error)
            return

        response = {'message': 'parcels'}
        if 'address' in req.params:
            address = req.params['address']
            options = {
                'returnGeometry':False, 'returnSuggestions':False,
                'outFields':'blklot,block_num,lot_num,ADDRESS'}
            if 'returnSuggestions' in req.params and req.params['returnSuggestions'] == 'true':
                options['returnSuggestions'] = True
            if 'returnGeometry' in req.params:
                options['returnGeometry'] = req.params['returnGeometry']
            if 'outFields' in req.params:
                options['outFields'] = req.params['outFields']

            sfarcgis = SfArcgis()
            sfarcgis.set_layer('parcel', os.environ.get('PLN_ARCGIS_PARCEL'))
            parcels = sfarcgis.get_fields_by_address(address, options)
            response = {'parcels': parcels}
        resp.body = json.dumps(jsend.success(response))
        resp.status = falcon.HTTP_200

    @staticmethod
    def has_missing_env(env_list):
        """ Check if variables are set """
        missing = []
        for var in env_list:
            if not os.environ.get(var):
                missing.append(var)
        return missing
