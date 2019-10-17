"""Record model"""
import os
from sf_arcgis_sdk.sf_arcgis import SfArcgis
from .datasf import DataSF

class Record():
    """Record class"""
    # possible field options
    field_options = ['year_built', 'building_area']
    # possible parcel field options
    field_parcel_options = ['blklot', 'block_num', 'lot_num', 'address']

    def __init__(self, parcel):
        self.data = {}
        self.parcel = parcel

    def get(self, fields_array):
        """ Get method """
        # setting default null values for possible field options
        for field in set(self.field_options) & set(fields_array):
            self.data[field] = None

        if 'year_built' in fields_array or 'building_area' in fields_array:
            tax_roll = self.get_asr_tax_roll()
            if 'year_built' in fields_array and 'year_property_built' in tax_roll:
                self.data['year_built'] = tax_roll['year_property_built']
            if 'building_area' in fields_array and 'property_area' in tax_roll:
                self.data['building_area'] = tax_roll['property_area']

        # if retrieving for parcel field ata
        field_parcel_request = set(self.field_parcel_options) & set(fields_array)
        if field_parcel_request:
            self.data['parcels'] = []
            sfarcgis = SfArcgis()
            sfarcgis.set_layer('parcel', os.environ.get('PLN_ARCGIS_PARCEL'))
            options = {'outFields' : ','.join(field_parcel_request)}
            parcels = sfarcgis.get_fields_by_parcel(self.parcel, options)
            if parcels:
                parcels = [(self.normalize_parcel_field_names(p)) for p in parcels]
                self.data['parcels'] = parcels

        return self.data

    def get_asr_tax_roll(self):
        """ Get data from Assessor Property Tax Roll"""
        response = DataSF().filter(
            os.environ.get('DATASF_ASR_TAX_ROLL'),
            {'parcel_number': self.parcel, '$order':'closed_roll_year DESC'})
        if response and isinstance(response, list):
            return response[0]
        else:
            return {}

    @staticmethod
    def normalize_parcel_field_names(parcel_object):
        """ normalize parcel field names """
        if 'attributes' in parcel_object:
            for key, _val in parcel_object['attributes'].items():
                if not key.islower():
                    parcel_object['attributes'][key.lower()] = parcel_object['attributes'].pop(key)
        return parcel_object
