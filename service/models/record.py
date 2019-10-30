"""Record model"""
import os
from sodapy import Socrata
from sf_arcgis_sdk.sf_arcgis import SfArcgis

class Record():
    """Record class"""
    # possible field options from DataSF
    field_datasf_options = {
        'year_built' : {'source': 'datasf_asr_tax_roll', 'field': 'year_property_built'},
        'building_area' : {'source': 'datasf_asr_tax_roll', 'field': 'property_area'},
        'ceqacode' : {'source': 'datasf_historic_ceqa', 'field': 'ceqacode'}
    }
    datasf_source_opts = {
        'datasf_asr_tax_roll' : {
            'parcel_field_name': 'parcel_number',
            'order':'closed_roll_year DESC'
            },
        'datasf_historic_ceqa' : {
            'parcel_field_name': 'APN'
            }
    }
    # possible parcel field options
    field_parcel_options = ['blklot', 'block_num', 'lot_num', 'address']


    def __init__(self, parcel_num):
        # parcel number associated with this record
        self.parcel_num = parcel_num
        # data object associated with this record
        self.data = {}

    def get(self, fields_array):
        """ Get method """

        # Retrieving for DataSF fields
        datasf_sources = {}
        for field in set(self.field_datasf_options.keys()) & set(fields_array):
            # setting default null values for possible field options
            self.data[field] = None
            # build DataSF sources array
            field_opt = self.field_datasf_options[field]
            if field_opt['source'] not in datasf_sources.keys():
                datasf_sources[field_opt['source']] = {}
            datasf_sources[field_opt['source']][field] = field_opt

        for (source_name, fields) in datasf_sources.items():
            self.data.update(self.get_datasf_data(source_name, fields))

        # Retrieving for parcel fields
        field_parcel_request = set(self.field_parcel_options) & set(fields_array)
        if field_parcel_request:
            self.data['parcels'] = []
            sfarcgis = SfArcgis()
            sfarcgis.set_layer('parcel', os.environ.get('PLN_ARCGIS_PARCEL'))
            options = {'outFields' : ','.join(field_parcel_request)}
            parcels = sfarcgis.get_fields_by_parcel(self.parcel_num, options)
            if parcels:
                parcels = [(self.normalize_parcel_field_names(p)) for p in parcels]
                self.data['parcels'] = parcels

        return self.data

    def get_datasf_data(self, source_name, fields):
        """ Get data from DataSF """
        data = {}
        client = Socrata(os.environ.get('DATASF_DOMAIN'), None)
        source_id = os.environ.get(source_name.upper()+'_ID')
        if source_id:
            datasf_source_opt = self.datasf_source_opts[source_name]
            order = datasf_source_opt.get('order', '')
            where = datasf_source_opt.get('parcel_field_name') + "='"+self.parcel_num+"'"
            response = client.get(source_id, where=where, order=order)
            if response and isinstance(response, list):
                row = response[0]
                for (field, field_opt) in fields.items():
                    data[field] = row.get(field_opt['field'], None)
        return data

    @staticmethod
    def normalize_parcel_field_names(parcel_object):
        """ normalize parcel field names """
        if 'attributes' in parcel_object:
            for key, _val in parcel_object['attributes'].items():
                if not key.islower():
                    parcel_object['attributes'][key.lower()] = parcel_object['attributes'].pop(key)
        return parcel_object
