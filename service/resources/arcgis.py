"""ArcGIS module"""
import os
import math
import json
import urllib
import requests
import falcon
import jsend
import usaddress

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
            addr = usaddress.tag(req.params['address'])
            options = {'returnGeometry':False, 'returnSuggestions':False}
            if 'returnSuggestions' in req.params and req.params['returnSuggestions'] == 'true':
                options['returnSuggestions'] = True
            if 'returnGeometry' in req.params:
                options['returnGeometry'] = req.params['returnGeometry']
            parcels = self.pln_parcel(addr, options)
            response = {'parcels': parcels}
        resp.body = json.dumps(jsend.success(response))
        resp.status = falcon.HTTP_200

    def pln_parcel(self, addr, options=None):
        """ get parcels from Planning ArcGIS """
        parcels = {}
        url = urllib.parse.urljoin(os.environ.get('PLN_ARCGIS_PARCEL')+'/', 'query')
        params = {'outFields':'blklot,ADDRESS', 'returnGeometry':'false', 'f':'json'}
        if options['returnGeometry']:
            params['returnGeometry'] = options['returnGeometry']
        if 'AddressNumber' in addr[0] and 'StreetName' in addr[0]:
            where = "base_address_num="+ addr[0]['AddressNumber']
            where += " and street_name='"+addr[0]['StreetName'].upper()+"'"
            if 'OccupancyIdentifier' in addr[0]:
                where += " and unit_address='"+addr[0]['OccupancyIdentifier'].upper()+"'"
            params['where'] = where
            response = self.query(url, params)
            if response and 'features' in response and response['features']:
                parcels = response['features']
            elif response is not None and options['returnSuggestions']:
                # auto suggestions
                if 'OccupancyIdentifier' in addr[0]:
                    where = "base_address_num="+ addr[0]['AddressNumber']
                    where += " and street_name='"+addr[0]['StreetName'].upper()+"'"
                    params['where'] = where
                    response = self.query(url, params)
                    if response and 'features' in response and response['features']:
                        parcels = response['features']
                if not parcels:
                    base_num = math.floor(int(addr[0]['AddressNumber'])/100)*100
                    where = "base_address_num >=" + str(base_num)
                    where += " and base_address_num <"+str(base_num+100)
                    where += " and street_name='"+addr[0]['StreetName'].upper()+"'"
                    params['where'] = where
                    response = self.query(url, params)
                    if response and 'features' in response and response['features']:
                        parcels = response['features']
        return parcels

    @staticmethod
    def query(url, params):
        """ Queries an url """
        response = {}
        headers = {}
        try:
            request = requests.get(url, params=params, headers=headers)
            if request.status_code == 200:
                response = request.json()
            return response
        # pylint: disable=bare-except
        except:
            return None

    @staticmethod
    def has_missing_env(env_list):
        """ Check if variables are set """
        missing = []
        for var in env_list:
            if not os.environ.get(var):
                missing.append(var)
        return missing
