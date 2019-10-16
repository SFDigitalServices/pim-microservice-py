"""Record model"""
import os
from .datasf import DataSF

class Record():
    """Record class"""
    data = {}
    # possible field options
    field_options = ['year_built', 'building_area']

    def __init__(self, parcel):
        self.data = {'parcel': parcel}

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
        return self.data

    def get_asr_tax_roll(self):
        """ Get data from Assessor Property Tax Roll"""
        response = DataSF().filter(
            os.environ.get('DATASF_ASR_TAX_ROLL'),
            {'parcel_number': self.data['parcel'], '$order':'closed_roll_year DESC'})
        if response and isinstance(response, list):
            return response[0]
        else:
            return {}
        